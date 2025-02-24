import glob
import json
import os
import os.path

import project.dataset_generation.yt_dlp_download as yt_dlp_download
from project.models import YouTubeVideoInfo
from project.utils.ffmpeg_utils import extract_frames_at_times
from project.utils.json_utils import EnhancedJSONEncoder
from project.utils.sampling_utils import sample_fixed_interval, sample_heatmap, sample_random
from project.youtube.client import YouTubeClient

YT_DLP_INFO_JSON_FILENAME_FORMAT = "{}.info.json"
YT_DLP_THUMBNAIL_FILENAME_FORMAT = "{}.webp"
YT_DLP_VIDEO_FILENAME_FORMAT = "{}.mp4"
YT_DLP_SUBS_FILENAME_FORMAT = "{}.en.srt"
YT_DLP_AUTO_SUBS_FILENAME_FORMAT = "{}.auto-subs.en.srt"

DATASET_YT_DLP_DESTINATION_FOLDER = "{}/ytdlp-metadata"
DATASET_IMAGES_FOLDER = "{}/images"


def generate_dataset_entry_from_video_id(
	yt_client: YouTubeClient,
	video_id: str,
	destination_folder: str,
	frames_to_extract: int,
	delete_ytdlp_data_after: bool = True,
	working_folder: str | None = None,
) -> YouTubeVideoInfo:
	"""
	Download all the data for a single video.

	:param yt_client: The YouTubeClient to use to download the video's metadata when necessary.
	:param video_id: The id of the video.
	:param destination_folder: The extracted data (frames) will be moved to this folder under an /images folder.
	:param frames_to_extract: The number of frames to extract for each sampling technique.
	:param delete_ytdlp_data_after: Whether to delete the raw ytdlp data after having processed the video.
	:param working_folder: The folder to use for downloading and processing the raw data. This parameter can be used to process already downloaded data, without downloading it (at least the mp4) again.
	:return: The YouTubeVideoInfo objct containing all the info of the video, the extracted frames are in the destination_folder/images folder.
	"""
	ytdlp_metadata_destination_folder = DATASET_YT_DLP_DESTINATION_FOLDER.format(destination_folder)
	os.makedirs(ytdlp_metadata_destination_folder, exist_ok=True)

	if working_folder is None:
		working_folder = ytdlp_metadata_destination_folder

	# Download video, info, subs, auto-subs
	info_json = yt_dlp_download.download_video_and_metadata(video_id, working_folder, download_video=frames_to_extract > 0)

	# with open(
	# 	os.path.join(working_folder, YT_DLP_INFO_JSON_FILENAME_FORMAT.format(video_id)),
	# 	"r",
	# ) as info_file:
	# 	info_json = json.load(info_file)

	subs_filename = os.path.join(working_folder, YT_DLP_SUBS_FILENAME_FORMAT.format(video_id))
	subs = None
	if os.path.exists(subs_filename):
		with open(subs_filename, "r") as subs_file:
			subs = subs_file.read()

	auto_subs_filename = os.path.join(
		working_folder, YT_DLP_AUTO_SUBS_FILENAME_FORMAT.format(video_id)
	)
	auto_subs = None
	if os.path.exists(auto_subs_filename):
		with open(auto_subs_filename, "r") as auto_subs_file:
			auto_subs = auto_subs_file.read()

	# Check if video has location metadata
	location = None
	if info_json.get("location") and yt_client:
		data_api_video_data = yt_client.get_videos([video_id])[0]
		location = data_api_video_data.location

	# Create youtubevideoinfo object
	yt_video_info = YouTubeVideoInfo.from_data_sources(info_json, subs, auto_subs, location)

	# Move thumbnail to images
	dataset_images_folder = DATASET_IMAGES_FOLDER.format(destination_folder)
	os.makedirs(dataset_images_folder, exist_ok=True)
	for extension in ["webp", "jpg"]:
		thumbnail_file_path = os.path.join(working_folder, f"{video_id}.{extension}")
		if not os.path.isfile(thumbnail_file_path):
			continue
		os.rename(
			os.path.join(thumbnail_file_path),
			os.path.join(dataset_images_folder, f"{video_id}_thumbnail.{extension}"),
		)

	# Extract frames from video
	if frames_to_extract > 0:
		video_path = os.path.join(working_folder, f"{video_id}.mp4")
		extract_frames_at_times(
			video_path,
			sample_random(yt_video_info.duration_s, frames_to_extract),
			dataset_images_folder,
			f"{video_id}_rand",
		)
		if yt_video_info.heatmap:
			extract_frames_at_times(
				video_path,
				sample_heatmap(yt_video_info.heatmap, frames_to_extract),
				dataset_images_folder,
				f"{video_id}_hm",
			)
		extract_frames_at_times(
			video_path,
			sample_fixed_interval(yt_video_info.duration_s, frames_to_extract),
			dataset_images_folder,
			f"{video_id}_fi",
		)

	# Delete info, subs, video
	if delete_ytdlp_data_after:
		for filepath in glob.glob(os.path.join(working_folder, f"{video_id}.*")):
			os.remove(filepath)

	return yt_video_info


def generate_dataset_from_video_ids(
	yt_client: YouTubeClient,
	video_ids: list[str],
	destination_folder: str,
	frames_per_video: int,
	delete_ytdlp_data_after: bool = True,
	working_folder: str | None = None,
	save_every_n_videos: int = 100,
	resume_from_file: bool = False,
) -> list[YouTubeVideoInfo]:
	if working_folder is None:
		working_folder = destination_folder

	dataset_filename = os.path.join(destination_folder, "videos_infos.json")
	failed_filename = os.path.join(destination_folder, "failed.json")
	dataset_metadata = []
	failed = dict()
	if resume_from_file:
		with open(dataset_filename, "r") as dataset_file:
			dataset_metadata = json.load(dataset_file)
		with open(failed_filename, "r") as failed_file:
			failed = json.load(failed_file)
		
	already_processed_video_ids = set([video["id"] for video in dataset_metadata]).union(set(failed.keys()))

	def save_metadata(d, f):
		with open(dataset_filename, "w") as dataset_file:
			json.dump(d, dataset_file, cls=EnhancedJSONEncoder)
		with open(failed_filename, "w") as failed_file:
			json.dump(f, failed_file, cls=EnhancedJSONEncoder)

	for i, video_id in enumerate(video_ids):
		print(f"Processing video {i}/{len(video_ids)} ⚙️")
		if video_id in already_processed_video_ids:
			print(f"Skipping video {video_id} as it has already been processed.")
			continue
		try:
			dataset_metadata.append(
				generate_dataset_entry_from_video_id(
					yt_client,
					video_id,
					destination_folder,
					frames_per_video,
					delete_ytdlp_data_after,
					working_folder,
				)
			)
		except Exception as exception:
			print(f"Error while processing {video_id}")
			print(exception)
			failed[video_id] = str(exception)
			continue
		if (i + 1) % save_every_n_videos == 0:
			save_metadata(dataset_metadata, failed)

	save_metadata(dataset_metadata, failed)
	return dataset_metadata


if __name__ == "__main__":
	import random

	random.seed(42)
	generate_dataset_from_video_ids(
		None, ["dQw4w9WgXcQ", "csdXyd3B2EQ"], "data/mydataset-test", 0, False
	)

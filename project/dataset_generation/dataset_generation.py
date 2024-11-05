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
	delete_ytdlp_metadata: bool = True,
) -> YouTubeVideoInfo:
	"""
	Download all the data for a single video.
	"""
	ytdlp_metadata_destination_folder = DATASET_YT_DLP_DESTINATION_FOLDER.format(destination_folder)
	os.makedirs(ytdlp_metadata_destination_folder, exist_ok=True)

	# Download video, info, subs, auto-subs
	yt_dlp_download.download_video_and_metadata(video_id, ytdlp_metadata_destination_folder)

	with open(
		os.path.join(
			ytdlp_metadata_destination_folder, YT_DLP_INFO_JSON_FILENAME_FORMAT.format(video_id)
		),
		"r",
	) as info_file:
		info_json = json.load(info_file)

	subs_filename = os.path.join(
		ytdlp_metadata_destination_folder, YT_DLP_SUBS_FILENAME_FORMAT.format(video_id)
	)
	subs = None
	if os.path.exists(subs_filename):
		with open(subs_filename, "r") as subs_file:
			subs = subs_file.read()

	auto_subs_filename = os.path.join(
		ytdlp_metadata_destination_folder, YT_DLP_AUTO_SUBS_FILENAME_FORMAT.format(video_id)
	)
	auto_subs = None
	if os.path.exists(auto_subs_filename):
		with open(auto_subs_filename, "r") as auto_subs_file:
			auto_subs = auto_subs_file.read()

	# Check if video has location metadata
	location = None
	if info_json.get("location"):
		data_api_video_data = yt_client.get_videos([video_id])[0]
		location = data_api_video_data.location

	# Create youtubevideoinfo object
	yt_video_info = YouTubeVideoInfo.from_data_sources(info_json, subs, auto_subs, location)

	# Move thumbnail to images
	dataset_images_folder = DATASET_IMAGES_FOLDER.format(destination_folder)
	os.makedirs(dataset_images_folder, exist_ok=True)
	os.rename(
		os.path.join(ytdlp_metadata_destination_folder, f"{video_id}.webp"),
		os.path.join(dataset_images_folder, f"{video_id}_thumbnail.webp"),
	)

	# Extract frames from video
	video_path = os.path.join(ytdlp_metadata_destination_folder, f"{video_id}.mp4")
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

	# Delete: video
	# TODO: implement after testing to avoid downloading the same video 1000 times

	# Delete info, subs, video
	if delete_ytdlp_metadata:
		for filepath in glob.glob(os.path.join(ytdlp_metadata_destination_folder, f"{video_id}.*")):
			os.remove(filepath)

	return yt_video_info


def generate_dataset_from_video_ids(
	yt_client: YouTubeClient,
	video_ids: list[str],
	destination_folder: str,
	frames_per_video: int,
	delete_ytdlp_metadata: bool = True,
) -> list[YouTubeVideoInfo]:
	dataset_metadata = []
	failed_ids = []
	for video_id in video_ids:
		try:
			dataset_metadata.append(
				generate_dataset_entry_from_video_id(
					yt_client,
					video_id,
					destination_folder,
					frames_per_video,
					delete_ytdlp_metadata,
				)
			)
		except Exception as exception:
			print(f"Error while processing {video_id}")
			print(exception)
			failed_ids.append(video_id)
			continue

	dataset_filename = os.path.join(destination_folder, "videos_infos.json")
	with open(dataset_filename, "w") as dataset_file:
		json.dump(dataset_metadata, dataset_file, cls=EnhancedJSONEncoder)
	failed_filename = os.path.join(destination_folder, "failed.json")
	with open(failed_filename, "w") as failed_file:
		json.dump(failed_ids, failed_file, cls=EnhancedJSONEncoder)
	return dataset_metadata


if __name__ == "__main__":
	import random

	random.seed(42)
	generate_dataset_from_video_ids(
		None, ["dQw4w9WgXcQ", "csdXyd3B2EQ"], "data/mydataset-test", 3, False
	)

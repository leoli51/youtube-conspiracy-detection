import glob

import yt_dlp

import project.utils.yt_dlp_utils as yt_dlp_utils
from project.models import YouTubeVideoInfo

YOUTUBE_VIDEO_URL_FORMAT = "https://www.youtube.com/watch?v={}"


def download_video_and_metadata(video_id: str, download_folder: str) -> YouTubeVideoInfo:
	# Configure yt-dlp options
	ydl_opts = {
		"extractor_args": {
			"youtube": {"comment_sort": "top", "max_comments": ["all", "20", "all", "5"]}
		},
		"outtmpl": f"{download_folder}/%(id)s.%(ext)s",  # Save video in the specified folder
		"getcomments": True,
		"writeinfojson": True,  # Save video metadata as JSON
		"writethumbnail": True,  # Download thumbnail
		"writesubtitles": True,  # Download subtitles if available
		"subtitlesformat": "srt",  # Download subtitles in SRT format
		"subtitleslangs": ["en"],  # Choose the language of subtitles
		"format": "best",  # Download best quality video
		"postprocessors": [
			{  # Convert subtitles to SRT format
				"key": "FFmpegSubtitlesConvertor",
				"format": "srt",
			}
		],
	}

	# Download video, thumbnail, and metadata
	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		info = ydl.extract_info(YOUTUBE_VIDEO_URL_FORMAT.format(video_id), download=True)

	# Automatic subs
	auto_subs_opts = {
		"outtmpl": f"{download_folder}/%(id)s.auto-subs.%(ext)s",  # Save video in the specified folder
		"writesubtitles": True,
		"writeautomaticsub": True,
		"subtitleslangs": ["en"],
		"skip_download": True,
		"subtitlesformat": "srt",  # Download subtitles in SRT format
		"postprocessors": [
			{  # Convert subtitles to SRT format
				"key": "FFmpegSubtitlesConvertor",
				"format": "srt",
			}
		],
	}

	with yt_dlp.YoutubeDL(auto_subs_opts) as ydl:
		ydl.process_ie_result(info)
		# Postprocessors are not invoked by that method so this is a workaround
		auto_subs_paths = glob.glob(f"{download_folder}/{video_id}.auto-subs.en.*")
		if auto_subs_paths:
			# ydl.post_process(auto_subs_paths[0], info) # TODO: make this work and remove line below
			yt_dlp_utils.convert_subtitles_to_srt(
				auto_subs_paths[0], f"{download_folder}/{video_id}.auto-subs.en.srt"
			)


if __name__ == "__main__":
	download_video_and_metadata("dQw4w9WgXcQ", ".")
	# download_video("csdXyd3B2EQ", ".")

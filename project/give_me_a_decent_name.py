from datetime import datetime
from typing import Any

import yt_dlp
from models import HeatMapItem, YouTubeVideo

YOUTUBE_VIDEO_URL_FORMAT = "https://www.youtube.com/watch?v={}"


def download_video(video_id: str, download_folder: str) -> YouTubeVideo:
	# Configure yt-dlp options
	ydl_opts = {
		"outtmpl": f"{download_folder}/%(id)s.%(ext)s",  # Save video in the specified folder
		"writeinfojson": True,  # Save video metadata as JSON
		"writethumbnail": True,  # Download thumbnail
		"writeautomaticsub": True,  # Download automatic subtitles if available
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
		video_filename = f"{download_folder}/{video_id}.mp4"
		thumbnail_filename = f"{download_folder}/{video_id}.jpg"
		print(f"Video downloaded as: {video_filename}")
		print(f"Thumbnail downloaded as: {thumbnail_filename}")


def extract_info_from_json(json_data: Any) -> YouTubeVideo:
	categories = json_data["categories"]
	channel_id = json_data["channel_id"]
	channel_title = json_data["channel"]
	channel_subscribers = json_data["channel_follower_count"]
	comment_count = json_data.get("comment_count", 0)
	# comments: list[YouTubeComment] | None
	description = json_data["description"]
	duration_s = json_data["duration"]
	has_timed_transcript = ...  # TODO: retrieve from somewhere
	heat_map = (
		[
			HeatMapItem(
				start_s=hm_item_raw["start_time"],
				end_s=hm_item_raw["end_time"],
				intensity=hm_item_raw["value"],
			)
			for hm_item_raw in json_data["heatmap"]
		]
		if json_data.get("heatmap")
		else None
	)
	id = json_data["id"]
	like_count = json_data["like_count"]
	# Location: if yt-dlp has location we can retrieve description and location from YoutubeAPI
	location_description = ...  # TODO retrieve from YouTube API
	location = ...  # TODO: retrieve from YouTube API
	publish_date = datetime(
		year=int(json_data["upload_date"][:4]),
		month=int(json_data["upload_date"][4:6]),
		day=int(json_data["upload_date"][6:]),
	)
	tags = json_data["tags"]
	title = json_data["title"]
	transcript = ...  # TODO: retrieve from somewhere
	view_count = json_data["view_count"]


def download_frames_and_thumbnail(video: YouTubeVideo, destination: str) -> None:
	raise NotImplementedError


if __name__ == "__main__":
	# download_video("dQw4w9WgXcQ", ".")
	download_video("csdXyd3B2EQ", ".")

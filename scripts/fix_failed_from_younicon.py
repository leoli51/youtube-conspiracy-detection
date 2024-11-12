import os
import random
from datetime import datetime, timezone

import google.auth
import google.auth.transport.requests

from project.dataset_generation.dataset_generation import generate_dataset_from_video_ids
from project.youtube.client import YouTubeClient

credentials, project = google.auth.default(
	scopes=[
		"https://www.googleapis.com/auth/cloud-platform",
		"https://www.googleapis.com/auth/youtube",
	]
)
yt_client = YouTubeClient(credentials=credentials)

failed_younicon_video_ids = set(
	file_name.split(".")[0] for file_name in os.listdir("data/myyounicon-01/ytdlp-metadata")
)

random.seed(42)

generate_dataset_from_video_ids(
	yt_client,
	failed_younicon_video_ids,
	f"data/fix-myyounicon-{datetime.now(timezone.utc)}",
	3,
	True,
	"data/myyounicon-01/ytdlp-metadata",
)

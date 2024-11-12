import random
from datetime import datetime, timezone

import google.auth
import google.auth.transport.requests
import pandas as pd

from project.dataset_generation.dataset_generation import generate_dataset_from_video_ids
from project.youtube.client import YouTubeClient

credentials, project = google.auth.default(
	scopes=[
		"https://www.googleapis.com/auth/cloud-platform",
		"https://www.googleapis.com/auth/youtube",
	]
)
yt_client = YouTubeClient(credentials=credentials)

younicon_video_ids = pd.read_csv("data/YouNiCon/conspiracy_label.csv")["video_id"].to_list()

random.seed(42)

generate_dataset_from_video_ids(
	yt_client, younicon_video_ids, f"data/myyounicon-{datetime.now(timezone.utc)}", 3, True
)

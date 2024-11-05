import random
import pandas as pd

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

younicon_video_ids = pd.read_csv("data/YouNiCon/conspiracy_label.csv")["video_id"].to_list()

random.seed(42)
generate_dataset_from_video_ids(
	yt_client, younicon_video_ids, "data/myyounicon-01", 3, True
)
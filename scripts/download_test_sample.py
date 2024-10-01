import json
from datetime import datetime

import google.auth
import google.auth.transport.requests

from project.utils.json import EnhancedJSONEncoder
from project.youtube.client import YouTubeClient

credentials, project = google.auth.default(
	scopes=[
		"https://www.googleapis.com/auth/cloud-platform",
		"https://www.googleapis.com/auth/youtube",
	]
)

yt_client = YouTubeClient(credentials=credentials)

from_date = datetime(2024, 9, 1)
to_date = datetime(2024, 10, 1)
sample_size = (
	1000  # each api call retrieves 50 videos (max) thus, this will result in 1000 api calls
)


search_results = []

while len(search_results) < sample_size:
	search_results += yt_client.search_videos(
		max_results=sample_size,
		published_after=from_date,
		published_before=to_date,
		region_code="US",
		relevance_language="EN",
	)

with open(f"data/random_sample_{sample_size}.json", "w") as serialize_file:
	json.dump(search_results, serialize_file, cls=EnhancedJSONEncoder)

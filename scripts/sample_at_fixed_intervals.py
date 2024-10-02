# TODO: Youtube Data API limits results to 500 per request
# Plus, requests are limited to 100 per day :ush: find workarounds
# Best workaround so far: fiddle with published before/after.

import json
from datetime import datetime, timedelta

import google.auth
import google.auth.transport.requests

from project.utils.json import EnhancedJSONEncoder
from project.youtube.client import YouTubeClient

sample_interval = timedelta(minutes=10)
sample_size_per_interval = (
	50  # Youtube API is very unreliable, sampling more than 100 leads to inconsistent results
)
from_date = datetime(2024, 9, 1)
to_date = datetime(2024, 9, 8)


credentials, project = google.auth.default(
	scopes=[
		"https://www.googleapis.com/auth/cloud-platform",
		"https://www.googleapis.com/auth/youtube",
	]
)

yt_client = YouTubeClient(credentials=credentials)

search_results = []
sample_datetime = from_date

while sample_datetime < to_date:
	try:
		print(f"Sampling from {sample_datetime} to {sample_datetime + sample_interval}...")
		tmp_results = yt_client.search_videos(
			max_results=sample_size_per_interval,
			published_after=sample_datetime,
			published_before=sample_datetime + sample_interval,
			region_code="US",
			relevance_language="EN",
		)
		search_results += tmp_results
		sample_datetime += sample_interval
		print(f"Retrieved {len(tmp_results)} videos! Total retrieved so far {len(search_results)}.")
	except Exception as e:
		print(
			f"Exception encountered while sampling from {sample_datetime} to {sample_datetime + sample_interval}!"
		)
		print(e)
		break  # lets try to save what we gathered so far

with open(
	f"data/random_sample_{len(search_results)}_from_{from_date.date()}_to_{sample_datetime.date()}_interval_{sample_interval}.json",
	"w",
) as serialize_file:
	json.dump(search_results, serialize_file, cls=EnhancedJSONEncoder)

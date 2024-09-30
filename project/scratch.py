# Scratch file to do random tests
import google.auth
import google.auth.transport.requests
from project.youtube.client import YouTubeClient

credentials, project = google.auth.default(
	scopes=[
		"https://www.googleapis.com/auth/cloud-platform",
		"https://www.googleapis.com/auth/youtube",
	]
)

yt_client = YouTubeClient(credentials=credentials)
response = yt_client.search_videos(max_results=100)
for item in response:
	print(item)

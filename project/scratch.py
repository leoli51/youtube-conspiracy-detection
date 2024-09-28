# Scratch file to do random tests
import google.auth
import google.auth.transport.requests
from youtube.client import YouTubeClient

credentials, project = google.auth.default(
	scopes=[
		"https://www.googleapis.com/auth/cloud-platform",
		"https://www.googleapis.com/auth/youtube",
		"https://www.googleapis.com/auth/youtube.force-ssl",
		"https://www.googleapis.com/auth/youtube.readonly",
	]
)

# auth_request = google.auth.transport.requests.Request()
# credentials.refresh(auth_request)

# print(credentials)
# print(project)

yt_client = YouTubeClient(credentials=credentials)
response = yt_client.search(max_results=100)
for item in response:
	print(item)

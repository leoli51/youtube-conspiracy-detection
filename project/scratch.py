# Scratch file to do random tests
import google.auth
from youtube.client import YouTubeClient
import google.auth.transport.requests

credentials, project = google.auth.default(
	scopes=[
		"https://www.googleapis.com/auth/cloud-platform",
		"https://www.googleapis.com/auth/youtube",
		"https://www.googleapis.com/auth/youtube.force-ssl",
		"https://www.googleapis.com/auth/youtube.readonly",
	]
)

auth_request = google.auth.transport.requests.Request()
credentials.refresh(auth_request)

print(credentials)
print(project)

yt_client = YouTubeClient(credentials=credentials)
yt_client.search()

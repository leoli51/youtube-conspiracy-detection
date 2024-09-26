import googleapiclient.discovery
from google.auth.credentials import Credentials

from youtube.models import SearchResultItem


class YouTubeClient:
	"""Client to access YouTube's APIs."""

	YOUTUBE_API_SERVICE_NAME: str = "youtube"
	YOUTUBE_API_VERSION: str = "v3"

	def __init__(self, credentials: Credentials) -> None:
		# TODO: the service opens persistent sockets that need to be closed explicitly.
		# This is not a problem if the program has a "function-like" behaviour (call function and
		# terminate). Do not use this client as-is in continuously running applications. source:
		# https://github.com/googleapis/google-api-python-client/blob/main/docs/start.md#build-the-service-object
		self.service = googleapiclient.discovery.build(
			YouTubeClient.YOUTUBE_API_SERVICE_NAME,
			YouTubeClient.YOUTUBE_API_VERSION,
			credentials=credentials,
		)

	def search(self) -> list[SearchResultItem]:
		request = self.service.search().list(part="snippet", channelId="UC-lHJZR3Gqxm24_Vd_AJ5Yw")
		response = request.execute()
		print(response)

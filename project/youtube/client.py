from datetime import datetime
from typing import Literal

import googleapiclient.discovery
from google.auth.credentials import Credentials

from project.youtube.models import SearchResult, Video


class YouTubeClient:
	"""Client to access YouTube's APIs."""

	# TODO: get information about videos via the videos API
	# TODO: get information about comments via the commentsThread API

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

	def search_videos(
		self,
		max_results: int,
		duration: Literal["any", "long", "medium", "short"] = "any",
		order: Literal["date", "rating", "relevance", "title", "viewCount"] = "relevance",
		published_after: datetime | None = None,
		published_before: datetime | None = None,
		query: str | None = None,
		region_code: str | None = None,
		relevance_language: str | None = None,
		safe_search: Literal["moderate", "none", "strict"] = "none",
		topic_id: str | None = None,
	) -> list[SearchResult]:
		"""
		Full documentation of API available at https://developers.google.com/youtube/v3/docs/search/list.

		:param max_results: retrieve up to this number of results, set to -1 to retrive all the results, use with care.
		:param duration: filters search results based on their duration. long 20m<, medium 4m<..<20m, short <4m
		:param order: method that will be used to order resources in the API response.
		:param published_after: return resources created after this time.
		:param published_before: return resources created before this time.
		:param query: specifies the query term to search for. Your request can also use the Boolean NOT (-) and OR (|) operators to exclude videos or to find videos that are associated with one of several search terms.
		:param region_code: return search results for videos that can be viewed in the specified country. The parameter value is an ISO 3166-1 alpha-2 country code.
		:param relevance_language: return search results that are most relevant to the specified language. The parameter value is typically an ISO 639-1 two-letter language code. However, you should use the values zh-Hans for simplified Chinese and zh-Hant for traditional Chinese. Please note that results in other languages will still be returned if they are highly relevant to the search query term.
		:param safe_search: whether the search results should include restricted content as well as standard content.
		:param topic_id: response should only contain resources associated with the specified topic. List of available topics at: https://developers.google.com/youtube/v3/docs/search/list
		"""
		request = self.service.search().list(
			maxResults=50,  # maximum value accepted, why should it be less if we are not worried about bandwidth/data consumption?
			order=order,
			part="snippet",
			publishedAfter=published_after.isoformat(timespec="seconds") + "Z"
			if published_after
			else None,
			publishedBefore=published_before.isoformat(timespec="seconds") + "Z"
			if published_before
			else None,
			q=query,
			regionCode=region_code,
			relevanceLanguage=relevance_language,
			safeSearch=safe_search,
			topicId=topic_id,
			type="video",
			videoDuration=duration,
		)

		search_result_items = []
		while request is not None and (len(search_result_items) < max_results or max_results == -1):
			response = request.execute()
			search_result_items += [
				SearchResult.from_api_response(item_raw) for item_raw in response["items"]
			]
			request = self.service.search().list_next(request, response)
		return search_result_items

	def get_videos(self, ids: list[str]) -> list[Video]:
		request = self.service.videos().list(
			part="contentDetails,id,localizations,paidProductPlacementDetails,snippet,statistics,topicDetails,recordingDetails",
			id=",".join(ids),
		)
		response = request.execute()
		return [Video.from_api_response(item_raw) for item_raw in response["items"]]

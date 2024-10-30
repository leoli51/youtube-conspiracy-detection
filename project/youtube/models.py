from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal

import dateutil

from project.utils.json import EnhancedJSONEncoder


@dataclass(frozen=True)
class Thumbnail:
	height: int
	url: str
	width: int

	@classmethod
	def from_api_response(cls, api_response) -> Thumbnail:
		return cls(**api_response)


@dataclass(frozen=True)
class SearchResult:
	"""
	Check https://developers.google.com/youtube/v3/docs/search for detailed documentation of these fields.
	"""

	channel_id: str
	channel_title: str
	description: str
	id: str
	kind: str
	live_broadcast_content: Literal["upcoming", "live", "none"]
	published_at: datetime
	thumbnails: dict[str, Thumbnail]
	title: str

	@classmethod
	def from_api_response(cls, api_response: Any) -> SearchResult:
		return cls(
			channel_id=api_response["snippet"]["channelId"],
			channel_title=api_response["snippet"]["channelTitle"],
			description=api_response["snippet"]["description"],
			id=api_response["id"].get("videoId")
			or api_response["id"].get("channelId")
			or api_response["id"].get("playlistId"),
			kind=api_response["id"]["kind"],
			live_broadcast_content=api_response["snippet"]["liveBroadcastContent"],
			published_at=dateutil.parser.parse(api_response["snippet"]["publishedAt"]),
			thumbnails={
				thumbnail_key: Thumbnail.from_api_response(thumbnail_api_response)
				for thumbnail_key, thumbnail_api_response in api_response["snippet"][
					"thumbnails"
				].items()
			},
			title=api_response["snippet"]["title"],
		)

	@classmethod
	def from_dict(cls, dic: dict[str, Any]) -> SearchResult:
		override_dict = {
			"published_at": dateutil.parser.parse(dic["published_at"]),
			"thumbnails": {
				thumbnail_key: Thumbnail(**thumbnail_dict)
				for thumbnail_key, thumbnail_dict in dic["thumbnails"].items()
			},
		}
		return cls(**(dic | override_dict))


@dataclass(frozen=True)
class Localization:
	"""Localized title and description for a video"""

	title: str
	description: str

	@classmethod
	def from_api_response(cls, api_response: Any) -> Localization:
		return cls(**api_response)


@dataclass(frozen=True)
class Video:
	"""
	Check https://developers.google.com/youtube/v3/docs/videos for a detailed documentation of these fields.
	"""

	allowed_regions: list[str] | None
	blocked_regions: list[str] | None
	captions_available: bool
	category_id: str
	channel_id: str
	channel_title: str
	comment_count: int
	default_audio_language: str
	default_language: str
	description: str
	dislike_count: int
	duration: str
	has_custom_thumbnail: bool
	has_paid_product_placement: bool
	id: str
	like_count: int
	localizations: dict[str, Localization]
	location_description: str | None
	location: tuple[float, float, float] | None
	projection: str  # 360 or rectangular
	published_at: datetime
	tags: list[str]
	thumbnails: dict[str, Thumbnail]
	title: str
	topic_categories: list[str]  # Wikipedia URLs 🤔
	view_count: int

	@classmethod
	def from_api_response(cls, api_response: Any):
		content_details = api_response.get("contentDetails", {})
		recording_details = api_response.get("recordingDetails", {})
		snippet = api_response.get("snippet", {})
		statistics = api_response.get("statistics", {})
		location = recording_details.get("location", {})
		lat = location.get("latitude")
		long = location.get("longitude")
		alt = location.get("altitude")
		location = (lat, long, alt) if lat or long else None

		return cls(
			allowed_regions=content_details.get("regionRestriction", {}).get("allowed"),
			blocked_regions=content_details.get("regionRestriction", {}).get("blocked"),
			captions_available=content_details.get("caption") == "true",
			category_id=snippet.get("categoryId"),
			channel_id=snippet.get("channelId"),
			channel_title=snippet.get("channelTitle"),
			comment_count=statistics.get("commentCount"),
			default_audio_language=snippet.get("defaultAudioLanguage"),
			default_language=snippet.get("deafaultLanguage"),
			description=snippet.get("description"),
			dislike_count=statistics.get("dislikeCount"),
			duration=content_details.get("duration"),
			has_custom_thumbnail=content_details.get("hasCustomThumbnail"),
			has_paid_product_placement=api_response.get("paidProductPlacementDetails", {}).get(
				"hasPaidProductPlacement"
			),
			id=api_response.get("id"),
			like_count=statistics.get("likeCount"),
			localizations={
				country_code: Localization.from_api_response(localization_data)
				for country_code, localization_data in api_response.get("localizations", {}).items()
			},
			location_description=recording_details.get("locationDescription"),
			location=location,
			projection=content_details.get("projection"),
			published_at=dateutil.parser.parse(snippet.get("publishedAt")),
			tags=snippet.get("tags"),
			thumbnails={
				thumbnail_key: Thumbnail.from_api_response(thumbnail_api_response)
				for thumbnail_key, thumbnail_api_response in snippet.get("thumbnails", {}).items()
			},
			title=snippet.get("title"),
			topic_categories=api_response.get("topicDetails", {}).get("topicCategories"),
			view_count=statistics.get("viewCount"),
		)


if __name__ == "__main__":
	import json

	with open("project/youtube/response_example.json") as response_file:
		response = json.load(response_file)
		models = [SearchResult.from_api_response(item_raw) for item_raw in response["items"]]

	with open("project/youtube/serialized_searchresult.json", "w") as serialize_file:
		json.dump(models, serialize_file, cls=EnhancedJSONEncoder)

	with open("project/youtube/serialized_searchresult.json") as serialize_file:
		raw_samples = json.load(serialize_file)
		print(SearchResult.from_dict(raw_samples[0]))

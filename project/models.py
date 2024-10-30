from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HeatMapItem:
	end_s: float
	intensity: float
	start_s: float


@dataclass(frozen=True)
class TimedTranscriptItem:
	text: str
	start: float
	duration: float


@dataclass(frozen=True)
class YouTubeComment:
	id: str
	author_id: str
	text: str


@dataclass(frozen=True)
class YouTubeVideo:
	"""Youtube video dataclass holding the informations that will be persisted in the final dataset"""

	categories: list[str]
	channel_id: str
	channel_subscribers: int
	channel_title: str
	comment_count: int
	comments: list[YouTubeComment] | None
	description: str
	duration_s: int
	has_timed_transcript: bool
	heat_map: list[HeatMapItem] | None
	id: str
	like_count: int
	location_description: str | None
	location: tuple[float, float, float] | None
	publish_date: datetime
	tags: list[str]
	title: str
	transcript: list[TimedTranscriptItem] | str
	view_count: int

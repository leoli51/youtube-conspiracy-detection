from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class HeatmapItem:
	end_s: float
	intensity: float
	start_s: float

	@classmethod
	def from_yt_dlp_heatmap_item(cls, heatmap_item: dict[str, float]) -> HeatmapItem:
		return cls(
			end_s=heatmap_item["end_time"],
			intensity=heatmap_item["value"],
			start_s=heatmap_item["start_time"],
		)

	@classmethod
	def from_yt_dlp_heatmap(cls, heatmap_data: list[dict[str, float]]) -> list[HeatmapItem]:
		return [HeatmapItem.from_yt_dlp_heatmap_item(hm_item) for hm_item in heatmap_data]


@dataclass
class YouTubeComment:
	author_id: str
	author_is_uploader: bool
	author_name: str
	id: str
	is_favorited: bool
	is_pinned: bool
	like_count: int
	parent_id: str
	publish_date: datetime
	replies: list[YouTubeComment]
	text: str

	@classmethod
	def from_yt_dlp_comment(cls, comment_data: dict[str, Any]) -> YouTubeComment:
		return cls(
			author_id=comment_data["author_id"],
			author_is_uploader=comment_data["author_is_uploader"],
			author_name=comment_data["author"],
			id=comment_data["id"],
			is_favorited=comment_data["is_favorited"],
			is_pinned=comment_data["is_pinned"],
			like_count=comment_data["like_count"],
			parent_id=comment_data["parent"],
			publish_date=datetime.fromtimestamp(comment_data["timestamp"]),
			replies=[],
			text=comment_data["text"],
		)

	@classmethod
	def from_yt_dlp_comments(cls, comments_data: list[dict[str, Any]]) -> list[YouTubeComment]:
		# Comments are retrieved in reply order so we could leverage this order to parse replies
		# I don't like this method so much, it's not very robus imho.
		# Replies have an ID format that is parent_id.reply_id, I will leverage this to parse the
		# replies.
		# Not optimized at all, but do we really need to optimize this?
		all_comments = [
			YouTubeComment.from_yt_dlp_comment(comment_data) for comment_data in comments_data
		]
		root_comments = [comment for comment in all_comments if comment.parent_id == "root"]
		for root_comment in root_comments:
			replies = [comment for comment in all_comments if comment.parent_id == root_comment.id]
			root_comment.replies = replies
		return root_comments


@dataclass(frozen=True)
class YouTubeVideoInfo:
	"""Youtube video dataclass holding the informations that will be persisted in the final dataset"""

	auto_subtitles: str | None
	categories: list[str]
	channel_id: str
	channel_subscribers: int
	channel_title: str
	comment_count: int
	comments: list[YouTubeComment] | None
	description: str
	duration_s: int
	heatmap: list[HeatmapItem] | None
	id: str
	like_count: int
	location_description: str | None
	location: tuple[float, float, float] | None
	publish_date: datetime
	subtitles: str | None
	tags: list[str]
	title: str
	view_count: int

	@classmethod
	def from_data_sources(
		cls,
		yt_dlp_info: Any,
		subs: str | None,
		auto_subs: str | None,
		location: tuple[float, float, float] | None,
	) -> YouTubeVideoInfo:
		"""
		Create a YouTubeVideoInfo object merging information from multiple data sources.
		"""
		return cls(
			auto_subtitles=auto_subs,
			categories=yt_dlp_info["categories"],
			channel_id=yt_dlp_info["channel_id"],
			channel_title=yt_dlp_info["channel"],
			channel_subscribers=yt_dlp_info["channel_follower_count"],
			comment_count=yt_dlp_info.get("comment_count", 0),
			comments=YouTubeComment.from_yt_dlp_comments(yt_dlp_info.get("comments"))
			if yt_dlp_info.get("comments")
			else None,
			description=yt_dlp_info["description"],
			duration_s=yt_dlp_info["duration"],
			heatmap=(
				HeatmapItem.from_yt_dlp_heatmap(yt_dlp_info.get("heatmap"))
				if yt_dlp_info.get("heatmap")
				else None
			),
			id=yt_dlp_info["id"],
			like_count=yt_dlp_info["like_count"],
			location_description=yt_dlp_info.get("location"),
			location=location,
			publish_date=datetime(
				year=int(yt_dlp_info["upload_date"][:4]),
				month=int(yt_dlp_info["upload_date"][4:6]),
				day=int(yt_dlp_info["upload_date"][6:]),
			),
			subtitles=subs,
			tags=yt_dlp_info["tags"],
			title=yt_dlp_info["title"],
			view_count=yt_dlp_info["view_count"],
		)

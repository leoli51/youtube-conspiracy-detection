from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from project.utils.json_utils import EnhancedJSONEncoder
from project.utils.subtitles_utils import text_from_subtitles


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
		# I don't like this method so much, it's not very robust imho.
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

	@classmethod
	def from_json(cls, json_data: Any) -> YouTubeComment:
		replies = (
			[YouTubeComment(**reply_data) for reply_data in json_data["replies"]]
			if json_data.get("replies")
			else []
		)
		json_data |= {"replies": replies}
		return cls(**json_data)

	def to_string_for_model_input(self, include_replies: bool, leading_tabs: int = 0):
		tabs = "\t" * leading_tabs
		sanitized_text = self.text.replace("\n", "\\n")
		string_parts = [f"{tabs}{self.author_name}: {sanitized_text}"]
		if include_replies and self.replies:
			string_parts.append(f"\t{tabs}replies:")
			string_parts += [
				f"\t\t{tabs}{reply.to_string_for_model_input(False)}" for reply in self.replies
			]
		return "\n".join(string_parts)


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
			comment_count=yt_dlp_info.get("comment_count", -1),
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
			like_count=yt_dlp_info.get("like_count", -1),
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

	@classmethod
	def from_json(cls, json_data: Any) -> YouTubeVideoInfo:
		heatmap = (
			[HeatmapItem(**hmi) for hmi in json_data["heatmap"]]
			if json_data.get("heatmap")
			else None
		)
		comments = (
			[YouTubeComment.from_json(comment) for comment in json_data["comments"]]
			if json_data["comments"]
			else None
		)
		json_data |= {"heatmap": heatmap, "comments": comments}
		return cls(**json_data)

	def __str__(self) -> str:
		return json.dumps(self, cls=EnhancedJSONEncoder)

	def to_string_for_model_input(
		self,
		attributes_to_include: list[str],
		max_description_length: int = -1,
		max_subtitles_length: int = -1,
		max_comments: int = -1,
		include_comments_replies: bool = True,
	) -> str:
		str_parts = []
		for attribute in attributes_to_include:
			if attribute in ["subtitles", "auto_subtitles"]:
				if self.__getattribute__(attribute) is None:  # CHeck if the subs are available
					str_parts.append(f"**{attribute}**: (not available)")
					continue
				pretty_subs = text_from_subtitles(self.__getattribute__(attribute))
				pretty_subs = (
					pretty_subs[:max_subtitles_length] if max_subtitles_length > 0 else pretty_subs
				)
				str_parts.append(f"**{attribute}**: {pretty_subs}")
			elif attribute == "comments":
				if self.__getattribute__(attribute) is None:  # CHeck if the comments are available
					str_parts.append(f"**{attribute}**: (not available)")
					continue
				comments = self.comments if max_comments == -1 else self.comments[:min([len(self.comments), max_comments])]
				comments_strings = [
					c.to_string_for_model_input(include_comments_replies, 1) for c in comments
				]
				comments_string = "\n".join(comments_strings)
				str_parts.append(f"**{attribute}**:\n{comments_string}")
			elif attribute == "description":
				cropped_description = self.description[:max_description_length] if max_description_length > -1 else self.description
				str_parts.append(f"**{attribute}**: {cropped_description}")
			else:
				str_parts.append(f"**{attribute}**: {self.__getattribute__(attribute)}")
		return "\n\n".join(str_parts)

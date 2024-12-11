from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Experiment:
	attributes_settings: dict[str, Any]
	attributes: list[str]
	completions_by_model_and_video_id: dict[str, dict[str, Any]]
	end_time: datetime
	id: str
	models: list[str]
	predicted_labels_by_model_and_video_id: dict[str, dict[str, Any]]
	start_time: datetime
	system_prompt: str

	@classmethod
	def from_completions(
		cls,
		*,
		attributes_settings: list[str],
		attributes: list[str],
		completions_by_model: dict[str, dict[str, Any]],
		end_time: datetime,
		id: str,
		models: list[str],
		start_time: datetime,
		system_prompt: str,
	) -> Experiment:
		predicted_labels_by_model = {}
		for model, completions in completions_by_model.items():
			predicted_labels_by_model[model] = {}
			for vid, completion in completions.items():
				try:
					is_conspiracy = "1" in completion.choices[0].message.content
					correct_output_format = completion.choices[0].message.content in ["0", "1"]
					predicted_labels_by_model[model][vid] = {
						"is_conspiracy": is_conspiracy,
						"correct_output_format": correct_output_format,
						"output": completion.choices[0].message.content,
					}
				except Exception as exception:
					predicted_labels_by_model[model][vid] = str(exception)

		return cls(
			attributes_settings=attributes_settings,
			attributes=attributes,
			completions_by_model_and_video_id=completions_by_model,
			end_time=end_time,
			id=id,
			models=models,
			predicted_labels_by_model_and_video_id=predicted_labels_by_model,
			start_time=start_time,
			system_prompt=system_prompt,
		)

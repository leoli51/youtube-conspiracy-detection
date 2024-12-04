from enum import Enum

import ollama


class OllamaModel(str, Enum):
	LLAMA_3_2 = "llama3.2"
	LLAMA_3_2_VISION = "llama3.2-vision"
	LLAVA = "llava"


def generate(model_name: OllamaModel, system_prompt: str, user_prompt: str) -> dict[str, str]:
	return ollama.generate(
		model=model_name,
		system=system_prompt,
		prompt=user_prompt,
	)


def generate_multimodal(
	model_name: OllamaModel, system_prompt: str, user_prompt: str, images_paths: list[str]
) -> dict[str, str]:
	response = ollama.generate(
		model=model_name,
		prompt=user_prompt,
		system=system_prompt,
		images=images_paths,
	)

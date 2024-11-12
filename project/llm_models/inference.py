import ollama


def chat(model_name: str, prompt: str) -> dict[str, str]:
	return ollama.chat(
		model=model_name,
		messages=[
			{
				"role": "user",
				"content": prompt,
			}
		],
	)


def chat_multimodal(model_name: str, prompt: str, images_paths: list[str]) -> dict[str][str]:
	response = ollama.chat(
		model=model_name,
		messages=[
			{
				"role": "user",
				"content": prompt,
				"images": images_paths,
			}
		],
	)

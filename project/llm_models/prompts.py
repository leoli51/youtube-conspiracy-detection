from project.models import YouTubeVideoInfo


def generate_prompt_input_full_text_output_binary_version_01(video_info: YouTubeVideoInfo) -> str:
	return f"""
You are an AI model tasked with classifying videos as either containing conspiracy content or not. For each video, you will receive a JSON-formatted input containing information such as:
- `view_count`: Number of views on the video.
- `title`: Title of the video.
- `description`: Description provided by the video's uploader.
- `channel`: Name of the channel that uploaded the video.
- `comments`: List of top comments on the video.
- `subtitles`: Subtitles or transcripts of the video, if available.

Your task is to analyze the information provided and determine if the video promotes, discusses, or spreads conspiracy theories or conspiratorial content. Conspiratorial content may include, but is not limited to, topics that lack factual basis, promote misinformation, or suggest secret, hidden plots by groups or institutions. 

If the video contains conspiracy content, respond with `1`. If it does not contain conspiracy content, respond with `0`. 

Important:
- Consider cues such as references to widely debunked theories, phrases suggesting secrecy, and terms commonly associated with conspiracy theories.
- Remain neutral and focus on the content rather than view counts or popularity alone.
- Only respond with `1` or `0` based on the classification.

Video info:
{video_info}"""


def generate_prompt_input_full_text_and_images_output_binary_version_01(
	video_info: YouTubeVideoInfo,
) -> str:
	pass

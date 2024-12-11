def input_full_text_output_binary_version_01() -> str:
	return """
You are an AI model tasked with classifying videos as either containing conspiracy content or not. For each video, you will receive a JSON-formatted input containing information about the video.
Your task is to analyze the information provided and determine if the video promotes, discusses, or spreads conspiracy theories or conspiratorial content. Conspiratorial content may include, but is not limited to, topics that lack factual basis, promote misinformation, or suggest secret, hidden plots by groups or institutions. 

If the video contains conspiracy content, respond with `1`. If it does not contain conspiracy content, respond with `0`. 

Important:
- Consider cues such as references to widely debunked theories, phrases suggesting secrecy, and terms commonly associated with conspiracy theories.
- Remain neutral and focus on the content rather than view counts or popularity alone.
- Only respond with `1` or `0` based on the classification.
"""


def input_full_text_and_images_output_binary_version_01() -> str:
	return """You are an AI model tasked with classifying videos as either containing conspiracy content or not. For each video, you will receive information about the video, including details about its content and frames extracted from the video.

Your task is to analyze the provided information and determine whether the video promotes, discusses, or spreads conspiracy theories or conspiratorial content. Conspiratorial content may include, but is not limited to, topics that lack factual basis, promote misinformation, or suggest secret, hidden plots by groups or institutions.

Guidelines:
	- Content Analysis: Use the provided information to identify themes, language, or visuals commonly associated with conspiracy theories, such as references to widely debunked claims, phrases suggesting secrecy, or suggestive imagery.
	- Holistic Approach: Consider both textual and visual elements to make your classification. Focus on the content itself rather than peripheral factors like popularity or engagement.

If the video contains conspiracy content, respond with 1. If it does not contain conspiracy content, respond with 0.

Important:
	- Only respond with 1 or 0 based on your analysis.
	- Avoid biases and focus purely on the content of the video and the frames provided.
"""


def tiktok_paper_simple_prompt() -> str:
	return "Decide whether the following transcription of a video talks about a conspiracy theory or not (if yes output = 1/else output=0). Provide just your output, no justification."

def tiktok_paper_prompt_with_definition() -> str:
	return "A conspiracy theory is a belief that two or more actors have coordinated in secret to achieve an outcome and that their conspiracy is of public interest but not public knowledge. Conspiracy theories (a) are oppositional, which means they oppose publicly accepted understandings of events; (b) describe malevolent or forbidden acts; (c) ascribe agency to individuals and groups rather than to impersonal or systemic forces; (d) are epistemically risky, meaning that though they are not necessarily false or implausible, taken collectively they are more prone to falsity than other types of belief; and (e) are social constructs that are not merely adopted by individuals but are shared with social objectives in mind, and they have the potential not only to represent and interpret reality but also to fashion new social realities. Given this definition of conspiracy theory: " + tiktok_paper_simple_prompt() 

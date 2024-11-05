import os.path

from yt_dlp.postprocessor.ffmpeg import FFmpegSubtitlesConvertorPP


def convert_subtitles_to_srt(old_file_path: str, new_file_path: str) -> None:
	if os.path.exists(new_file_path):
		return
	pp = FFmpegSubtitlesConvertorPP()
	pp.run_ffmpeg(old_file_path, new_file_path, ["-f", "srt"])


if __name__ == "__main__":
	convert_subtitles_to_srt("dQw4w9WgXcQ.auto-subs.en.vtt", "test.srt")

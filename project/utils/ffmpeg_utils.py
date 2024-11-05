import os

import ffmpeg


def extract_frames_at_times(
	video_path: str, timestamps_s: list[float], output_folder: str, frame_prefix: str
) -> None:
	# Ensure the output folder exists
	os.makedirs(output_folder, exist_ok=True)
	# Extract each frame at the specified timestamp
	for i, timestamp in enumerate(timestamps_s):
		# Format the timestamp in seconds for the filename
		timestamp = round(timestamp, 1)
		frame_filename = f"{frame_prefix}_{i:02}_{timestamp}s.jpg"
		frame_path = os.path.join(output_folder, frame_filename)

		# Run ffmpeg to extract the frame at the specified timestamp
		try:
			(
				ffmpeg.input(video_path, ss=timestamp)  # Seek to the timestamp
				.output(frame_path, vframes=1, qscale=2)  # Extract a single frame
				.overwrite_output()
				.run(capture_stdout=True, capture_stderr=True)
			)
			print(f"Extracted frame at {timestamp}s to {frame_path}")
		except ffmpeg.Error as e:
			print(f"Error extracting frame at {timestamp}s: {e.stderr.decode()}")


if __name__ == "__main__":
	extract_frames_at_times("dQw4w9WgXcQ.mp4", [1.0235093405, 4.4, 5.5], "frames", "manual_test")

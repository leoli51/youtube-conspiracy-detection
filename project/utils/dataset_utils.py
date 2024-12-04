from glob import glob
from os import path


def generate_images_path_from_video_id(video_id: str, dataset_path: str) -> list[str]:
	dataset_path = path.abspath(dataset_path)
	glob_pattern = path.join(dataset_path, f"images/{video_id}*.jpg")
	return glob(glob_pattern)


def generate_thumbnail_path_from_video_id(video_id: str, dataset_path: str) -> list[str]:
	dataset_path = path.abspath(dataset_path)
	glob_pattern = path.join(dataset_path, f"images/{video_id}_thumbnail.jpg")
	return glob(glob_pattern)

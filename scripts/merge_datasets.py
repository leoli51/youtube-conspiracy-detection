import glob
import json
import os
from typing import Any


def load_json(file_path: str) -> Any:
	with open(file_path, "r") as json_file:
		return json.load(json_file)


def write_json(json_data: Any, file_path: str) -> None:
	with open(file_path, "w") as json_file:
		json.dump(json_data, json_file)


datasets_to_merge: list[str] = glob.glob("data/fix-myyounicon-*")
destination_dataset_path: str = "data/myyounicon-01"
destination_images_path: str = os.path.join(destination_dataset_path, "images")

main_video_infos = load_json(os.path.join(destination_dataset_path, "videos_infos.json"))

for dataset_path in datasets_to_merge:
	# load json video info and merge it into main_video_info
	video_infos = load_json(os.path.join(dataset_path, "videos_infos.json"))
	main_video_infos += video_infos

	# move all images
	images_path = dataset_path + "/images"
	for image_path in os.listdir(images_path):
		os.rename(
			os.path.join(images_path, image_path), os.path.join(destination_images_path, image_path)
		)

write_json(main_video_infos, os.path.join(destination_dataset_path, "merged_videos_infos.json"))

import json
from project.utils.json_utils import EnhancedJSONEncoder
from project.experiments.models import Experiment
from datetime import datetime

experiments_to_merge = [
    "/home/leoli/Uni/Polimi/Thesis/master-thesis/notebooks/experiment-1733827485.json",
    "/home/leoli/Uni/Polimi/Thesis/master-thesis/notebooks/experiment-1733837706.json",
    ]
experiments: list[Experiment] = []

for experiment_file_name in experiments_to_merge:
    with open(experiment_file_name, "r") as f:
        experiment_json = json.load(f)
        experiments.append(Experiment.from_json(experiment_json))

experiment = experiments[0]
start_time = experiment.start_time
end_time = experiment.end_time
for experiment_to_merge in experiments[1:]:
    for model in experiment.models:
        experiment.completions_by_model_and_video_id[model] |= experiment_to_merge.completions_by_model_and_video_id[model]
        experiment.predicted_labels_by_model_and_video_id[model] |= experiment_to_merge.predicted_labels_by_model_and_video_id[model]
        start_time = min(start_time, experiment_to_merge.start_time)
        end_time = max(end_time, experiment_to_merge.end_time)

with open(f"notebooks/experiment-{'+'.join([e.id for e in experiments])}.json", "w") as f:
        json.dump(experiment, f, cls=EnhancedJSONEncoder)
    



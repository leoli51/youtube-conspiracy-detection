import random

from project.models import HeatmapItem


def sample_heatmap(heatmap: list[HeatmapItem], samples: int) -> list[float]:
	return [
		hmi.start_s for hmi in sorted(heatmap, key=lambda e: e.intensity, reverse=True)[:samples]
	]


def sample_fixed_interval(duration_s: float, samples: int) -> list[float]:
	# + 0.1 to avoid the first black frame that is there sometimes
	return [i * duration_s / samples + 0.1 for i in range(samples)]


def sample_random(duration_s: float, samples: int) -> list[float]:
	return [random.random() * duration_s for _ in range(samples)]

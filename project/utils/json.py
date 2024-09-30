import dataclasses
import json
from datetime import date, datetime


class EnhancedJSONEncoder(json.JSONEncoder):
	def default(self, obj):
		if dataclasses.is_dataclass(obj):
			return dataclasses.asdict(obj)
		if isinstance(obj, (datetime, date)):
			return obj.isoformat()
		return super().default(obj)

from enum import Enum
import re

class CronInterval(Enum):
	MIN={"name":"minute","min":0,"max":59}
	HOU={"name":"hour","min":0,"max":23}
	DAY={"name":"day","min":1,"max":31}
	MON={"name":"month","min":1,"max":12}
	WEE={"name":"week","min":0,"max":6}

class CronTypeError(TypeError):
	pass
class CronValueError(ValueError):
	pass

class Cron:
	def __init__(
		self,
		interval,
		interval_mode=CronInterval.HOU.value["name"],
	):
		if not isinstance(interval,int):
			raise CronTypeError("interval must be int type.")
		self._interval = interval
		if not isinstance(interval_mode,str):
			raise CronTypeError("interval_mode must be str type.")

		if len([x.value['name'] for x in CronInterval if re.match(rf'^{x.value["name"]}$',f'{interval_mode}',flags=re.IGNORECASE) is not None]) == 0:
			raise CronValueError(f"interval_mode is invalid value. valid value ({[x.value['name'] for x in CronInterval]})")
		self._interval_mode = [x for x in CronInterval if re.match(rf'^{x.value["name"]}$',f'{interval_mode}',flags=re.IGNORECASE) is not None][0]

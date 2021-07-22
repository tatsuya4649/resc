from enum import Enum
import re

class CronScale(Enum):
	MIN={"name":"minute","min":0,"max":59}
	HOU={"name":"hour","min":0,"max":23}
	DAY={"name":"day","min":1,"max":31}
	MON={"name":"month","min":1,"max":12}
	WEE={"name":"week","min":0,"max":6}
class CronMode(Enum):
	INTERVAL="interval"
	SCHEDULE="schedule"

class CronTypeError(TypeError):
	pass
class CronAttributeError(AttributeError):
	pass
class CronValueError(ValueError):
	pass
class CronRegularExpressionError(ValueError):
	pass

class Cron:
	def __init__(
		self,
		command,
		interval_str,
	):
		if not isinstance(command,str):
			raise CronTypeError("command must be str type.")
		self._command = command

		if interval_str is None:
			raise CronValueError("interval_str must be not None.")
#		if interval_str is not None and intervals is not None:
#			raise CronValueError("intervals or interval_str either one must be None.")

		if interval_str is not None:
			self._interval_str = interval_str
#			self._intervals = None
			self._str_to_lists()
			return

#		self._interval_str = None
#		if not isinstance(intervals,list):
#			raise CronTypeError("intervals must be list type.")
#		if len(intervals) == 0:
#			raise CronValueError("intervals must have one or more interval elem")
#
#
#		self._intervals = list()
#		for elem in intervals:
#			if not isinstance(elem,dict):
#				raise CronTypeError("intervals element must be dict type.")
#			if "scale" not in elem.keys() or "interval" not in elem.keys() or "mode" not in elem.keys():
#				raise CronValueError("interval element type must have \"scale\",\"interval\",\"mode\" keys.")
#			
#			interval = elem["interval"]
#			interval_mode = elem["mode"]
#			interval_scale = elem["scale"]
#
#			_crdict = dict()
#			if not isinstance(interval,int):
#				raise CronTypeError("interval must be int type.")
##			self._interval = interval
#			_crdict["interval"] = interval
#			if not isinstance(interval_mode,str):
#				raise CronTypeError("interval_mode must be str type.")
#
#			if len([x.value['name'] for x in CronScale if re.match(rf'^{x.value["name"]}$',f'{interval_scale}',flags=re.IGNORECASE) is not None]) == 0:
#				raise CronValueError(f"interval_scale is invalid value. valid value ({[x.value['name'] for x in CronScale]})")
##			self._interval_scale = [x for x in CronScale if re.match(rf'^{x.value["name"]}$',f'{interval_scale}',flags=re.IGNORECASE) is not None][0]
#			_crdict["scale"] = [x for x in CronScale if re.match(rf'^{x.value["name"]}$',f'{interval_scale}',flags=re.IGNORECASE) is not None][0]
#
#			if len([x.value for x in CronMode if re.match(rf'^{x.value}$',f'{interval_mode}',flags=re.IGNORECASE) is not None]) == 0:
#				raise CronValueError(f"interval_mode is invalid value. valid value ({[x.value for x in CronMode]})")
#			_crdict["mode"] = [x for x in CronMode if re.match(rf'^{x.value}$',f'{interval_mode}',flags=re.IGNORECASE) is not None][0]
##			self._interval_mode = [x for x in CronMode if re.match(rf'^{x.value}$',f'{interval_mode}',flags=re.IGNORECASE) is not None][0]
#			
#			self._intervals.append(_crdict)
#			self._lists_to_str()
#	@property
#	def intervals(self):
#		return self._intervals
	@property
	def interval_str(self):
		return self._interval_str

#	def _lists_to_str(self):
#		if not hasattr(self,"_intervals") or self._intervals is None or len(self._intervals)==0:
#			raise CronAttributeError("_intervals must be not None.")
#		self._interval_str = str()
#		for scale in list(CronScale):
#			scales = [x for x in self._intervals if x["scale"] is scale]
#			if len(scales) == 0:
#				self._interval_str += "* "
#				continue
#			before = [x for x in scales if x["mode"] == CronMode.SCHEDULE]
#			if len(before) == 0:
#				self._interval_str += f"*"
#			else:
#				if len(x for x in before if isinstance(x["interval"],str)) > 0:
#					raise CronValueError("cron time interval is invalid valid.")
#				for schedule in before:
#					if isinstance(schedule["interval"],str) and schedule["interval"] == "*":
#						self._interval_str += f"*"
#						break
#					self._interval_str += f"{schedule["interval"]}"
#				self._interval_str.rstrip(",")
#
#			after = [x for x in scales if x["mode"] == CronMode.INTERVAL]
#			if len(after) > 0:
#				if len(after) > 1:
#					raise CronValueError(f"interval mode of {scale.value["name"]} must have only one.")
#				self._interval_str += f"/{after["interval"] if isinstance(after["interval"],int) else "*"}"
#			self._interval_str += " "
#			
#		self._interval_str = self._interval_str.rstrip(' ')
#		print(self._interval_str)


	def _str_to_lists(self):
		self._intervals = list()
		template = r'(([0-6]?[0-9]-[0-6]?[0-9])|((,?[0-6]?[0-9])+)|(\*))(/[0-6]?[0-9])?'

		results = re.finditer(template,self._interval_str)
		results = [i for i in results]
		if len(results) != 5:
			raise CronRegularExpressionError("invalid cron string")
		for res in results:
			# */10
			deleteblank = re.match(r"^\S+",res.group())
			if deleteblank is None:
				raise CronRegularExpressionError("invalid cron string")
			before_slash = deleteblank.group().split('/')[0]

			index = results.index(res)
			if len(before_slash.split('-'))>1:
				self._intervals.append({
					"interval":-1,
					"scale":CronMode.SCHEDULE,
					"mode":list(CronScale)[index],
					"from":before_slash.split('-')[0],
					"to":before_slash.split('-')[1],
				})
			else:
				self._intervals.append({
					"interval":int(before_slash) if before_slash != '*' else "*",
					"scale":CronMode.SCHEDULE,
					"mode":list(CronScale)[index],
				})
				

			if len(deleteblank.group().split('/')) > 1:
				after_slash = deleteblank.group().split('/')[1]
				self._intervals.append({
					"interval":int(after_slash),
					"scale":CronMode.INTERVAL,
					"mode":list(CronScale)[index],
				})
				

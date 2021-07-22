import psutil
import re
from enum import Enum
from .logical import Logic
from .detect import DetectBase

class CPUTypeError(TypeError):
	pass
class CPUValueError(ValueError):
	pass

class CPUDetectMode(Enum):
	PERCENT={"name":"percent","logic":Logic.GT}
	LOADAVG={"name":"loadavg","logic":Logic.GT}

class CPUDetect(DetectBase):
	"""
	Detect CPU threshold by percent(%) or load average.
	"""
	_CPU_INTERVAL_DEFAULT=10
	def __init__(
		self,
		threshold,
		mode=CPUDetectMode.PERCENT.value["name"],
		interval=_CPU_INTERVAL_DEFAULT,
	):
		if not isinstance(threshold,int) and not isinstance(threshold,float):
			raise CPUTypeError("threshold must be int or float type.")
		self._threshold = threshold

		if not isinstance(mode,str):
			raise CPUTypeError(f"mode must be string type.({[x.value['name'] for x in CPUDetectMode]})")
		if len([x for x in CPUDetectMode if re.match(rf'^{x.value["name"]}$',f'{mode}',flags=re.IGNORECASE) is not None]) == 0:
			raise CPUValueError(f"{mode} is invalid.(valid value:{[x.value['name'] for x in CPUDetectMode]})")
		self._mode = [x for x in CPUDetectMode if re.match(rf'^{x.value["name"]}$',f'{mode}',flags=re.IGNORECASE)][0]

		if not isinstance(interval,int) and not isinstance(interval,float):
			raise CPUTypeError("interval must be int or float type.")
		self._interval = interval
	@property
	def resource(self):
		return "cpu"
	@property
	def mode(self):
		return self._mode

	@property
	def check(self):
		"""
		Check over CPU threshold.
		over threshold: return False
		within threshold: return True
		"""
		res = eval(f"self.{self._mode.value['name']}({self._interval})")
		if eval(f"{res} {self._mode.value['logic'].value} {self.threshold}"):
			return False
		else:
			return True

	@property
	def threshold(self):
		return self._threshold

	@staticmethod
	def percent(interval):
		if not isinstance(interval,float) and not isinstance(interval,int):
			raise TypeError("interval must by float or int type.")
		return psutil.cpu_percent(interval=float(interval),percpu=False)

	@staticmethod
	def percent_percpu(interval):
		if not isinstance(interval,float) and not isinstance(interval,int):
			raise TypeError("interval must by float or int type.")
		return psutil.cpu_percent(interval=float(interval),percpu=True)

	@staticmethod
	def loadavg():
		return psutil.getloadavg()

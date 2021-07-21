import psutil
from enum import Enum
from .logical import Logic

class MemoryTypeError(TypeError):
	pass
class MemoryValueError(ValueError):
	pass

class MemoryDetectMode(Enum):
	PERCENT={"name":"percent","logic":Logic.GT}
	USED={"name":"used","logic":Logic.GT}
	AVAILABLE={"name":"available","logic":Logic.LT}

class MemoryDetect:
	"""
	"""
	def __init__(
		self,
		threshold,
		mode=MemoryDetectMode.PERCENT.value["name"],
	):
		if not isinstance(threshold,int) and not isinstance(threshold,float):
			raise MemoryTypeError("threshold must be int or float type.")
		self._threshold = threshold

		if not isinstance(mode,str):
			raise MemoryTypeError("mode most be string type.")
		if mode not in [x.value["name"] for x in MemoryDetectMode if x.value["name"] == mode]:
			raise MemoryValueError(f"{mode} is invalid. valid value: {[x.value['name'] for x in MemoryDetectMode]}")
		self._mode = [x for x in MemoryDetectMode if x.value["name"] == mode][0]
	
	@property
	def mode(self):
		return self._mode

	@property
	def check(self):
		"""
		Check over Memory threshold.
		over threshold: return False
		within threshold: return True
                """
		res = eval(f"self.{self._mode.value['name']}()")
		if res is None:
			raise MemoryValueError("memory value must be not None.")
		if eval(f'{res} {self._mode.value["logic"].value} {self._threshold}'):
			return True
		else:
			return False
	
	@property
	def threshold(self):
		return self._threshold
	@staticmethod
	def percent():
		return psutil.virtual_memory().percent

	@staticmethod
	def used():
		return psutil.virtual_memory().used

	@staticmethod
	def available():
		return psutil.virtual_memory().available

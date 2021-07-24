from ctypes import *
import io
from enum import Enum
import re

#from resclog import RescLog
from .rformat import RescLogFormat

class RescLogFlag(Enum):
    DATE=1<<0
    OVER=1<<1
    FUNC=1<<2
    FILE=1<<3
    REMO=1<<4
    SOUR=1<<5

class RescLogHeaderTypeError(TypeError):
	pass

class RescLogHeader(LittleEndianStructure):
	_IDENTIFY_DEFAULT="resc"
	_fields_ = (
		('identify',c_char*4),
		('headlen',c_uint16),
		('bodylen',c_uint32),
		('stdoutlen',c_uint32),
		('stderrlen',c_uint32),
		(f'{RescLogFormat.DATE.value}len',c_uint16),
		(f'{RescLogFormat.OVER.value}len',c_uint16),
		(f'{RescLogFormat.FUNC.value}len',c_uint16),
		(f'{RescLogFormat.REMO.value}len',c_uint16),
		(f'{RescLogFormat.SOUR.value}len',c_uint16),
		('flag',c_uint32),
	)
	
	def __init__(
		self,
		bodylen,
		stdoutlen,
		stderrlen,
		flaglist,
		lendict,
	):
		self._identify = self._IDENTIFY_DEFAULT.encode()
		super().__init__(
			identify=self._identify,
			headlen=RescLogHeader.length(),
			bodylen=bodylen,
			stdoutlen=stdoutlen,
			stderrlen=stderrlen,
			datelen=lendict["date"],
			overlen=lendict["over"],
			funclen=lendict["date"],
			filelen=lendict["file"],
			remolen=lendict["remo"],
			sourlen=lendict["sour"],
			flags=self._flag(flaglist),
		)

	def _flag(self,flaglist):
		if not isinstance(flaglist,list):
			raise RescLogHeaderTypeError("flagslist must be list type.")
		if len([x for x in flaglist if not isinstance(x,RescLogFlag)]) != 0:
			raise RescLogHeaderTypeError("flagslist element must be list RescLogFlag.")
		flaglist = list(set(flaglist))
		result = int(0)
		for flag in flaglist:
			if not isinstance(flag.value,int):
				raise RescLogHeaderTypeError("RescLogFlag value must be int.")
			result |= flag.value
		return result
	@classmethod
	def convert(self,formatlist):
		res = list()
		for f in formatlist:
			str(f)
			res.append(eval(f"{re.sub('^RescLogFormat','RescLogFlag',str(f))}"))
		return res

	@staticmethod
	def length():
		return sizeof(RescLogHeader)
	@property
	def bytes(self):
		buffer = io.BytesIO()
		buffer.write(self)
		return buffer.getvalue()

__all__ = [
		RescLogFlag.__name__,
		RescLogHeader.__name__,
]
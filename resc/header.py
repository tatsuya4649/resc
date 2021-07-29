from ctypes import *
import io
from enum import Enum

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
	_fields_ = (
		('identify',c_char*4),
		('headlen',c_uint16),
		('bodylen',c_uint32),
		('flag',c_uint32),
	)
	
	def __init__(
		self,
		identify,
		headlen,
		bodylen,
		flaglist,
	):
		super().__init__(
			identify,
			headlen,
			bodylen,
			self._flag(flaglist),
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

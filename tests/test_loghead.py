from resc.header import RescLogHeader,RescLogFlag
from ctypes import *

_IDENTIFY=b"resc"
_HEADERLEN=10
_BODYLEN=200
_FORMAT=[RescLogFlag.DATE,RescLogFlag.FUNC]
def test_logheader():
	header = RescLogHeader(
		_IDENTIFY,
		_HEADERLEN,
		_BODYLEN,
		_FORMAT,
	)
	print(header)
	print(header.identify)

def test_flag():
	header = RescLogHeader(
		_IDENTIFY,
		_HEADERLEN,
		_BODYLEN,
		_FORMAT,
	)
	res = header.flag
	assert res is not None
	assert isinstance(res,int)
	print(f"FLAG: {res}")

def test_byte():
	header = RescLogHeader(
		_IDENTIFY,
		_HEADERLEN,
		_BODYLEN,
		_FORMAT,
	)
	res = header.bytes
	assert res is not None
	assert isinstance(res,bytes)
	print(f"HEADER: {res}")

def test_headlen():
	header = RescLogHeader(
		_IDENTIFY,
		_HEADERLEN,
		_BODYLEN,
		_FORMAT,
	)
	res = header.headlen
	assert res is not None
	assert isinstance(res,int)
	print(f"HEADERLEN: {res}")

def test_bodylen():
	header = RescLogHeader(
		_IDENTIFY,
		_HEADERLEN,
		_BODYLEN,
		_FORMAT,
	)
	res = header.bodylen
	assert res is not None
	assert isinstance(res,int)
	print(f"BODYLEN: {res}")

def test_len():
	header = RescLogHeader(
		_IDENTIFY,
		_HEADERLEN,
		_BODYLEN,
		_FORMAT,
	)
	res = header.length()
	assert res is not None
	assert isinstance(res,int)
	print(f"LENGTH: {res}")

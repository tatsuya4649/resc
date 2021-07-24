import unittest
from resc.header import RescLogHeader,RescLogFlag
from ctypes import *

class TestRescLogHeader(unittest.TestCase):
	_IDENTIFY=b"resc"
	_HEADERLEN=10
	_BODYLEN=200
	_FLAG=[RescLogFlag.DATE,RescLogFlag.FUNC]
	def test_logheader(self):
		header = RescLogHeader(
			self._IDENTIFY,
			self._HEADERLEN,
			self._BODYLEN,
			self._FLAG,
		)
		print(header)
		print(header.identify)

	def test_flag(self):
		header = RescLogHeader(
			self._IDENTIFY,
			self._HEADERLEN,
			self._BODYLEN,
			self._FLAG,
		)
		res = header.flag
		self.assertIsNotNone(res)
		self.assertIsInstance(res,int)
		print(f"FLAG: {res}")

	def test_byte(self):
		header = RescLogHeader(
			self._IDENTIFY,
			self._HEADERLEN,
			self._BODYLEN,
			self._FLAG,
		)
		res = header.bytes
		self.assertIsNotNone(res)
		self.assertIsInstance(res,bytes)
		print(f"HEADER: {res}")

	def test_headlen(self):
		header = RescLogHeader(
			self._IDENTIFY,
			self._HEADERLEN,
			self._BODYLEN,
			self._FLAG,
		)
		res = header.headlen
		self.assertIsNotNone(res)
		self.assertIsInstance(res,int)
		print(f"HEADERLEN: {res}")

	def test_bodylen(self):
		header = RescLogHeader(
			self._IDENTIFY,
			self._HEADERLEN,
			self._BODYLEN,
			self._FLAG,
		)
		res = header.bodylen
		self.assertIsNotNone(res)
		self.assertIsInstance(res,int)
		print(f"BODYLEN: {res}")

	def test_len(self):
		header = RescLogHeader(
			self._IDENTIFY,
			self._HEADERLEN,
			self._BODYLEN,
			self._FLAG,
		)
		res = header.length()
		self.assertIsNotNone(res)
		self.assertIsInstance(res,int)
		print(f"LENGTH: {res}")

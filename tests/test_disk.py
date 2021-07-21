import unittest
from resc.disk import *

_DISK_THRESHOLD=80
_DISK_PATH="/"

class TestDisk(unittest.TestCase):
	def test_disk(self):
		disk = DiskDetect(
			_DISK_PATH,
			_DISK_THRESHOLD,
			mode="percent",
		)
		res = disk.percent("/")
		self.assertIsNotNone(res)
		self.assertIsInstance(res,float)
		self.assertGreaterEqual(res,0.0)
		print(f'DIST PERCENT {res}% ({type(res)})')

		res = disk.free("/")
		self.assertIsNotNone(res)
		self.assertIsInstance(res,int)
		self.assertGreaterEqual(res,0)
		print(f'DIST FREE {res} bytes [ {round(res/(1024*1024),1)}MB , {round(res/(1024*1024*1024),1)}GB ] ({type(res)})')
		
		res = disk.check
		self.assertIsNotNone(res)
		self.assertIsInstance(res,bool)
		print(f'DISK CHECK {res} ({type(res)})')

if __name__ == "__main__":
	unittest.main()

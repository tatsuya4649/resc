import unittest
from resc.disk import *

class TestDisk(unittest.TestCase):
	def test_disk(self):
		res = disk_percent("/")
		self.assertIsNotNone(res)
		self.assertIsInstance(res,float)
		self.assertGreaterEqual(res,0.0)
		print(f'DIST PERCENT {res}% ({type(res)})')

		res = disk_free("/")
		self.assertIsNotNone(res)
		self.assertIsInstance(res,int)
		self.assertGreaterEqual(res,0)
		print(f'DIST FREE {res} bytes [ {round(res/(1024*1024),1)}MB , {round(res/(1024*1024*1024),1)}GB ] ({type(res)})')

if __name__ == "__main__":
	unittest.main()

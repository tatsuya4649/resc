import unittest
from resc.memory import *

class TestMemory(unittest.TestCase):
	def test_memory(self):
		res = memory_percent()
		self.assertIsNotNone(res)
		self.assertIsInstance(res,float)
		self.assertGreaterEqual(res,0.0)

		print(f'MEMORY USAGE PERCENT {res}% ({type(res)})')

		res = memory_used()
		self.assertIsNotNone(res)
		self.assertIsInstance(res,int)
		self.assertGreaterEqual(res,0)

		print(f'MEMORY USED {res}bytes [ {round(res/(1024*1024),1)}MB , {round(res/(1024*1024*1024),1)}GB ] ({type(res)})')

		res = memory_available()
		self.assertIsNotNone(res)
		self.assertIsInstance(res,int)
		self.assertGreaterEqual(res,0)

		print(f'MEMORY AVAILABLE {res}bytes [ {round(res/(1024*1024),1)}MB , {round(res/(1024*1024*1024),1)}GB ] ({type(res)})')


if __name__ == "__main__":
	unittest.main()

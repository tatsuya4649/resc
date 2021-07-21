import unittest
from resc.cpu import *

_CPU_WAIT_TIME = 1

class TestCPU(unittest.TestCase):
	def test_cpu(self):
		res = ave_cpu_percent(_CPU_WAIT_TIME)
		self.assertIsNotNone(res)
		self.assertIsInstance(res,float)
		print(f'CPU AVERAGE RATIO: {res}%(float)')
		self.assertGreaterEqual(res,0.0)

		res = cpu_percent(_CPU_WAIT_TIME)
		self.assertIsNotNone(res)
		self.assertIsInstance(res,list)
		print(f'CPU RATIO PER CPU: (list of float)')
		for cpu_number in range(len(res)):
			print(f'CPU AVERAGE RATIO[{cpu_number}]: {res[cpu_number]}%({type(res[cpu_number])})')
			self.assertIsInstance(res[cpu_number],float)
			self.assertGreaterEqual(res[cpu_number],0.0)

		res = cpuloadavg()
		self.assertIsNotNone(res)
		self.assertIsInstance(res,tuple)
		print(f'CPU LOAD AVG PER CPU: (list of float)')
		for cpu_number in range(len(res)):
			print(f'CPU LOAD AVG[{cpu_number}]: {res[cpu_number]}({type(res[cpu_number])})')
			self.assertIsInstance(res[cpu_number],float)
			self.assertGreaterEqual(res[cpu_number],0.0)


if __name__ == "__main__":
	unittest.main()

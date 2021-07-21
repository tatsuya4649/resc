import unittest
from resc.cpu import *

_CPU_WAIT_TIME = 1
_CPU_MODE = "percent"

class TestCPU(unittest.TestCase):
	def test_cpu(self):
		cpu = CPUDetect(
			80,
			mode=_CPU_MODE,
			interval=_CPU_WAIT_TIME
		)
		res = cpu.percent(_CPU_WAIT_TIME,)
		self.assertIsNotNone(res)
		self.assertIsInstance(res,float)
		print(f'CPU AVERAGE RATIO: {res}%({type(res)})')
		self.assertGreaterEqual(res,0.0)

		res = cpu.percent_percpu(_CPU_WAIT_TIME)
		self.assertIsNotNone(res)
		self.assertIsInstance(res,list)
		print(f'CPU RATIO PER CPU: (list of float)')
		for cpu_number in range(len(res)):
			print(f'CPU AVERAGE RATIO[{cpu_number}]: {res[cpu_number]}%({type(res[cpu_number])})')
			self.assertIsInstance(res[cpu_number],float)
			self.assertGreaterEqual(res[cpu_number],0.0)

		res = cpu.loadavg()
		self.assertIsNotNone(res)
		self.assertIsInstance(res,tuple)
		print(f'CPU LOAD AVG PER CPU: (list of float)')
		for cpu_number in range(len(res)):
			print(f'CPU LOAD AVG[{cpu_number}]: {res[cpu_number]}({type(res[cpu_number])})')
			self.assertIsInstance(res[cpu_number],float)
			self.assertGreaterEqual(res[cpu_number],0.0)

		res = cpu.check
		self.assertIsNotNone(res)
		self.assertIsInstance(res,bool)
		print(f'CPU THRESHOLD CHECK: {res} (type(res))')


if __name__ == "__main__":
	unittest.main()

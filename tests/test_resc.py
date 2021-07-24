import unittest
import os

from resc._resc import Resc
_INTERVAL=0

class TestResc(unittest.TestCase):
	def test_resc(self):
		resc = Resc(
			cpu={"threshold":80,"interval":_INTERVAL},
			memory={"threshold":80},
			disk={"threshold":80,"path":"/"},
		)
		res = resc.thresholds
		self.assertIsNotNone(res)
		self.assertIsInstance(res,dict)
		print(f'RESC THRESHOLDS {res}')

		res = resc.checks
		self.assertIsNotNone(res)
		self.assertIsInstance(res,dict)
		print(f'RESC CHECKS {res}')

		res = resc.over_one
		self.assertIsNotNone(res)
		self.assertIsInstance(res,bool)
		print(f'RESC OVER ONE {res}')

		res = resc.overs
		self.assertIsNotNone(res)
		self.assertIsInstance(res,list)
		print(f'RESC OVERS {res}')


class TestRegister(unittest.TestCase):
	def test_register(self):
		resc = Resc(
			cpu={"threshold":80,"interval":_INTERVAL},
			memory={"threshold":80},
			disk={"threshold":80,"path":"/"},
		)
		@resc.register("*/1 * * * *",rescdir=".")
		def hello():
			print("hello resc!!!")

		os.environ["RESCPATH"] = "."	
		os.environ["RESCOUTPUT"] = "./rescoutput.txt"	
		@resc.register("*/1 * * * *")
		def world(a,b):
			print("hello world")
			import time
			print(a,b)
			print(time.time())

		world(1,b="resc test script")
	
class TestRemote(unittest.TestCase):
	def test_remote(self):
		resc = Resc(
			cpu={"threshold":0.0,"interval":_INTERVAL},
			memory={"threshold":80},
			disk={"threshold":80,"path":"/"},
		)
		@resc.register(
			trigger="* * * * *",
			rescdir="rescs",
			outputfile="output",
			ip="13.231.122.182",
			username="ubuntu",
			key_path="~/.aws/TestKeyPair.pem",
		)
		def hello():
			print("hello resc!!!")
		hello()

if __name__ == "__main__":
	unittest.main()

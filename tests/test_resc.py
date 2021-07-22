import unittest
from resc._resc import Resc


_INTERVAL=0

class TestResc(unittest.TestCase):
#	def test_resc(self):
#		resc = Resc(
#			cpu={"threshold":80,"interval":_INTERVAL},
#			memory={"threshold":80},
#			disk={"threshold":80,"path":"/"},
#		)
#		res = resc.thresholds
#		self.assertIsNotNone(res)
#		self.assertIsInstance(res,dict)
#		print(f'RESC THRESHOLDS {res}')
#
#		res = resc.checks
#		self.assertIsNotNone(res)
#		self.assertIsInstance(res,dict)
#		print(f'RESC CHECKS {res}')
#
#		res = resc.over_one
#		self.assertIsNotNone(res)
#		self.assertIsInstance(res,bool)
#		print(f'RESC OVER ONE {res}')
#
#		res = resc.overs
#		self.assertIsNotNone(res)
#		self.assertIsInstance(res,list)
#		print(f'RESC OVERS {res}')

	def test_register(self):
		resc = Resc(
			cpu={"threshold":80,"interval":_INTERVAL},
			memory={"threshold":80},
			disk={"threshold":80,"path":"/"},
		)
		@resc.register("*/1 * * * *")
		def hello():
			print("hello resc!!!")

		hello()
if __name__ == "__main__":
	unittest.main()

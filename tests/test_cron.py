import unittest
from resc.cron import *

_INTERVAL=10
_INTERVAL_MODE="interval"
_INTERVAL_SCALE="day"

class TestCron(unittest.TestCase):
	def test_cron(self):
#		cron = Cron(
#			command='echo "Hello world"',
#			intervals=[{"interval":_INTERVAL,"scale":_INTERVAL_SCALE,"mode":_INTERVAL_MODE}]
#		)
#
#		res = cron.intervals
#		self.assertIsNotNone(res)
#		self.assertIsInstance(res,list)
#
#		print(f'CRON INTERVAL LISTS {res}')

		cron = Cron(
			command='echo "Hello world"',
			interval_str="*/1 0-3 * * *",
		)
		print(cron._intervals)

#		res = cron.interval_str
#		self.assertIsNotNone(res)
#		self.assertIsInstance(res,str)
#		print(f'CRON INTERVAL STRING {res}')
#		res = cron.intervals
#		self.assertIsNotNone(res)
#		self.assertIsInstance(res,list)
#		print(f'CRON INTERVAL LISTS {res}')

if __name__ == "__main__":
	unittest.main()

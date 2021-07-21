import unittest
from resc.cron import *

_INTERVAL=10
_INTERVAL_MODE="day"

class TestCron(unittest.TestCase):
	def test_cron(self):
		cron = Cron(_INTERVAL,_INTERVAL_MODE)

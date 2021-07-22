import unittest
import unittest.mock
from resc.cron import *
import subprocess

_INTERVAL=10
_INTERVAL_MODE="interval"
_INTERVAL_SCALE="day"

class TestCron(unittest.TestCase):
	def test_cron(self):
		cron = Cron(
			command='echo "Hello world"',
			interval_str="*/1 0-3 * * *",
		)
		res = cron.interval_str
		self.assertIsNotNone(res)
		self.assertIsInstance(res,str)
		print(f"CRON INTERVAL STRING \"{res}\"")

		res = cron.totalline
		self.assertIsNotNone(res)
		self.assertIsInstance(res,str)
		print(f"CRON TOTAL LINE \"{res}\"")

		res = cron.register()
		self.assertIsNotNone(res)
		self.assertIsInstance(res,int)
		print(f"CRON REGISTER END STATUS \"{res}\"")
		res = cron.list
		self.assertIsNotNone(res)
		self.assertIsInstance(res,list)
		print(f"CRON LISTS {res}")
		res = cron.count
		self.assertIsNotNone(res)
		self.assertIsInstance(res,int)
		print(f"CRON COUNT {res}")

		res = cron.delete()
		self.assertIsNotNone(res)
		self.assertIsInstance(res,int)
		print(f"CRON DELETE END STATUS \"{res}\"")
	
#	def test_register(self):
#		cron = Cron(
#			command='echo "Hello world"',
#			interval_str="*/1 0-3 * * *",
#		)
#
#		m = unittest.mock.MagicMock()
#		subprocess.run = m
#		cron.register()
#		m.assert_called_with(["crontab"],input=f'{cron.totalline}\n',encoding="utf-8")
#
#		m = unittest.mock.MagicMock()
#		subprocess.run = m
#		cron.list()
#		m.assert_called_with(["crontab","-l"],encoding="utf-8")

if __name__ == "__main__":
	unittest.main()

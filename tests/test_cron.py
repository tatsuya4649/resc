from resc.cron import *
import subprocess

_INTERVAL=10
_INTERVAL_MODE="interval"
_INTERVAL_SCALE="day"

def test_cron():
	cron = Cron(
		command='echo "Hello world"',
		interval_str="*/1 0-3 * * *",
	)
	res = cron.interval_str
	assert res is not None
	assert isinstance(res,str)
	print(f"CRON INTERVAL STRING \"{res}\"")

	res = cron.totalline
	assert res is not None
	assert isinstance(res,str)
	print(f"CRON TOTAL LINE \"{res}\"")

	res = cron.register()
	assert res is not None
	assert isinstance(res,int)
	print(f"CRON REGISTER END STATUS \"{res}\"")
	res = cron.list
	assert res is not None
	assert isinstance(res,list)
	print(f"CRON LISTS {res}")
	res = cron.count
	assert res is not None
	assert isinstance(res,int)
	print(f"CRON COUNT {res}")

	res = cron.delete()
	assert res is not None
	assert isinstance(res,int)
	print(f"CRON DELETE END STATUS \"{res}\"")


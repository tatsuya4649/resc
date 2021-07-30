from resc.resclog import RescLog,RescLogFormat

def test_resclog():
	resclog = RescLog(logfile="resclog")

	assert resclog is not None
	assert isinstance(resclog,RescLog)

	log = resclog.log
	assert log is not None
	assert isinstance(log,bool)
	assert log is True
	print(f"RESCLOG LOG {log}")

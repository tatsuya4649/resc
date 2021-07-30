import os
from resc import RescLogAnalyze
from resc.resclog.dump import RescDump
    
LOGPATH=os.path.normpath(f"{__file__}/../test_data/output")
def test_analyze():
	ana = RescLogAnalyze(LOGPATH)
	log = ana.getlog()
	assert isinstance(log,bytes)
	logres = ana.analyze(log)

	assert isinstance(logres,list)
	for res in logres:
		assert isinstance(res,dict)

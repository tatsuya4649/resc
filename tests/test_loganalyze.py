import unittest
from resc import RescLogAnalyze
from resc.resclog.dump import RescDump

class TestAnalyze(unittest.TestCase):
    LOGPATH="~/.resc/log/output"
    def test_analyze(self):
        ana = RescLogAnalyze(self.LOGPATH)
        log = ana.getlog()
        logres = ana.analyze(log)

        for res in logres:
            print(res)

    def test_dump(self):
       pass 


if __name__ == "__main__":
    unittest.main()
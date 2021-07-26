import unittest
from resc import RescLogAnalyze
from resc.resclog.dump import RescDump

class TestAnalyze(unittest.TestCase):
    LOGPATH="~/.resc/log/output"
    def test_analyze(self):
        ana = RescLogAnalyze(self.LOGPATH)
        ana.analyze()
#    def test_header(self):
#        ana = RescLogAnalyze(self.LOGPATH)



if __name__ == "__main__":
    unittest.main()
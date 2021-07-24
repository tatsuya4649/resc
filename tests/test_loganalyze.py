import unittest
from resc import RescLogAnalyze

class TestAnalyze(unittest.TestCase):
    LOGPATH="~/.resc/log/output"
    def test_analyze(self):
        ana = RescLogAnalyze(self.LOGPATH)
        ana.analyze()

if __name__ == "__main__":
    unittest.main(g)
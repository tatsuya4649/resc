import unittest
from resc.resclog import RescLog,RescLogFormat

class TestRescLog(unittest.TestCase):
    def test_resclog(self):
        resclog = RescLog(logfile="resclog")
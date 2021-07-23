import unittest
from resc.resclog import RescLog,RescLogFormat

class TestRescLog(unittest.TestCase):
    def test_resclog(self):
        resclog = RescLog("resclog")
        
    def test_resclog_default(self):
        resclog = RescLog(logfile="resclog")
        res = resclog.default_directory()
        self.assertIsNotNone(res)
        self.assertIsInstance(res,str)
        self.assertEqual(res,resclog._LOGPATH_DEFAULT)
    def test_resclog_default_format(self):
        resclog = RescLog("resclog")
        res = resclog._default_format([RescLogFormat.DATE])
        self.assertIsNotNone(res)
        self.assertIsInstance(res,list)
    def test_resclog_format(self):
        resclog = RescLog(logfile="resclog")
        res = resclog.format_str
        self.assertIsNotNone(res)
        self.assertIsInstance(res,str)
        print(res)
    def test_define(self):
        resclog = RescLog(logfile="resclog")
        res = resclog._define_resclog(resclog)
        self.assertIsNotNone(res)
        self.assertIsInstance(res,str)
        print(res)
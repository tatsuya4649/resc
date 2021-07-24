import unittest
import datetime
from resc.resclog.header import RescLogFlag
from resc.resclog.header import RescLogHeader
from resc.resclog.rformat import RescLogFormat, RescLogOver

class TestHeader(unittest.TestCase):
    _BODYLEN=200
    def test_header(self):
        header = RescLogHeader(
            bodylen=self._BODYLEN,
            flaglist=[RescLogFlag.DATE,RescLogFlag.FUNC],
            lendict={
                "date":21,
                "over":1324,
                "file":3121,
                "remo":23,
                "sour":34,
            }
        )
        print(header)
    def test_convert(self):
        format = [
                RescLogFormat.DATE,
                RescLogFormat.FUNC,
                RescLogFormat.SOUR,
        ]
        res = RescLogHeader.convert(format)
        
        self.assertIsNotNone(res)
        self.assertIsInstance(res,list)
        for f in res:
            print(type(f))
            self.assertIn(f,RescLogFlag)
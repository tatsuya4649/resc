import datetime
from resc.resclog.header import RescLogFlag
from resc.resclog.header import RescLogHeader
from resc.resclog.rformat import RescLogFormat, RescLogOver

_BODYLEN=200
def test_header():
	header = RescLogHeader(
	    bodylen=_BODYLEN,
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
	assert header is not None
	assert isinstance(header,RescLogHeader)
def test_convert():
	format = [
		RescLogFormat.DATE,
		RescLogFormat.FUNC,
		RescLogFormat.SOUR,
	]
	res = RescLogHeader.convert(format)

	assert res is not None
	assert isinstance(res,list)
	for f in res:
	    print(type(f))
	    assert f in RescLogFlag

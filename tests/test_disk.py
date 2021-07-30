from resc.disk import *

_DISK_THRESHOLD=80
_DISK_PATH="/"

def test_disk():
	disk = DiskDetect(
		_DISK_PATH,
		_DISK_THRESHOLD,
		mode="percent",
	)
	res = disk.percent("/")
	assert res is not None
	assert isinstance(res,float)
	assert res >= 0.0
	print(f'DIST PERCENT {res}% ({type(res)})')

	res = disk.free("/")
	assert res is not None
	assert isinstance(res,int)
	assert res >= 0
	print(f'DIST FREE {res} bytes [ {round(res/(1024*1024),1)}MB , {round(res/(1024*1024*1024),1)}GB ] ({type(res)})')
	
	res = disk.check
	assert res is not None
	assert isinstance(res,bool)
	print(f'DISK CHECK {res} ({type(res)})')

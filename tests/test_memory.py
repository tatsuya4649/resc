from resc.memory import *

def test_memory():
	memory = MemoryDetect(80)
	res = memory.percent()
	assert res is not None
	assert isinstance(res,float)
	assert res >= 0.0

	print(f'MEMORY USAGE PERCENT {res}% ({type(res)})')

	res = memory.used()
	assert res is not None
	assert isinstance(res,int)
	assert res >= 0

	print(f'MEMORY USED {res}bytes [ {round(res/(1024*1024),1)}MB , {round(res/(1024*1024*1024),1)}GB ] ({type(res)})')

	res = memory.available()
	assert res is not None
	assert isinstance(res,int)
	assert res >= 0

	print(f'MEMORY AVAILABLE {res}bytes [ {round(res/(1024*1024),1)}MB , {round(res/(1024*1024*1024),1)}GB ] ({type(res)})')

	res = memory.check
	assert res is not None
	assert isinstance(res,bool)
	print(f'MEMORY CHECK {res} (type(res))')

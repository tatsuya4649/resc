from resc.cpu import *

_CPU_WAIT_TIME = 1
_CPU_MODE = "percent"

def test_cpu():
	cpu = CPUDetect(
		80,
		mode=_CPU_MODE,
		interval=_CPU_WAIT_TIME
	)
	res = cpu.percent(_CPU_WAIT_TIME,)
	assert res is not None
	assert isinstance(res,float)
	print(f'CPU AVERAGE RATIO: {res}%({type(res)})')
	assert res >= 0.0

	res = cpu.percent_percpu(_CPU_WAIT_TIME)
	assert res is not None
	assert isinstance(res,list)
	print(f'CPU RATIO PER CPU: (list of float)')
	for cpu_number in range(len(res)):
		print(f'CPU AVERAGE RATIO[{cpu_number}]: {res[cpu_number]}%({type(res[cpu_number])})')
		assert isinstance(res[cpu_number],float)
		assert res[cpu_number] >= 0.0

	res = cpu.loadavg()
	assert res is not None
	assert isinstance(res,tuple)
	print(f'CPU LOAD AVG PER CPU: (list of float)')
	for cpu_number in range(len(res)):
		print(f'CPU LOAD AVG[{cpu_number}]: {res[cpu_number]}({type(res[cpu_number])})')
		assert isinstance(res[cpu_number],float)
		assert res[cpu_number] >= 0.0

	res = cpu.check
	assert res is not None
	assert isinstance(res,bool)
	print(f'CPU THRESHOLD CHECK: {res} (type(res))')

import pytest
from unittest import mock
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

@pytest.mark.parametrize(
    "threshold",[
    "1",
    "1.0",
    [1],
    {"threshold": 1}
])
def test_memory_init_type_error(threshold):
    with pytest.raises(
        MemoryTypeError
    ) as raiseinfo:
        memory = MemoryDetect(threshold)

@pytest.mark.parametrize(
    "mode",[
    1,
    1.0,
    ["percent"],
    {"mode": "percent"}
])
def test_memory_init_mode_type_error(mode):
    with pytest.raises(
        MemoryTypeError
    ) as raiseinfo:
        memory = MemoryDetect(
            threshold=80.0,
            mode=mode
        )

def test_memory_check_false():
    with mock.patch(
        "resc.memory.MemoryDetect.percent",
        return_value = 90.0
    ):
        memory = MemoryDetect(
            threshold=80.0
        )
        assert memory.check is False

def test_memory_check_none():
    with mock.patch(
        "resc.memory.MemoryDetect.percent",
        return_value = None
    ):
        memory = MemoryDetect(
            threshold=80.0
        )
        with pytest.raises(
            MemoryValueError
        ) as raiseinfo:
            memory.check

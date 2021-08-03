from resc.cpu import *
import pytest

_CPU_INTERVAL_DEFAULT = 1
_CPU_MODE_PERCENT = "percent"
_CPU_MODE_LOADAVG = "loadavg"
_CPU_THRESHOLD_PERCENT = 80.0
_CPU_THRESHOLD_LOADAVG = 1.0
_CPU_OVER_PERCENT = 120.0
_CPU_OVER_LOADAVG = 10.0

@pytest.fixture(scope="module",autouse=True)
def setup_cpu_percent():
    print("setup cpu (percent)")
    cpu = CPUDetect(
        _CPU_THRESHOLD_PERCENT,
        mode=_CPU_MODE_PERCENT,
        interval=_CPU_INTERVAL_DEFAULT
    )
    yield cpu
@pytest.fixture(scope="module",autouse=True)
def setup_cpu_loadavg():
    print("setup cpu (loadavg)")
    cpu = CPUDetect(
        _CPU_THRESHOLD_LOADAVG,
        mode=_CPU_MODE_LOADAVG,
        interval=_CPU_INTERVAL_DEFAULT
    )
    yield cpu

def test_cpu_threshold_type_fail():
    with pytest.raises(
        CPUTypeError,
        match=r"^.*int or float type.*$",
    ) as raiseinfo:
        cpu = CPUDetect(
            threshold="80.0",
            mode=_CPU_MODE_PERCENT,
            interval=_CPU_INTERVAL_DEFAULT
        )
    print(f"CPU THRESHOLD TYPE ERROR OUTPUT: {raiseinfo.value}")

def test_cpu_mode_type_fail():
    with pytest.raises(
        CPUTypeError,
        match=r"^.*string type.*$",
    ) as raiseinfo:
        cpu = CPUDetect(
            threshold=80.0,
            mode=10.0,
            interval=_CPU_INTERVAL_DEFAULT,
        )
    print(f"CPU MODE TYPE ERROR OUTPUT: {raiseinfo.value}")

def test_cpu_mode_value_fail():
    _FAIL_MODE = "mode"
    with pytest.raises(
        CPUValueError,
        match=r"^.*invalid.*$",
    ) as raiseinfo:
        cpu = CPUDetect(
            threshold=80.0,
            mode=_FAIL_MODE,
            interval=_CPU_INTERVAL_DEFAULT,
        )
    print(f"CPU MODE VALUE ERROR OUTPUT: {raiseinfo.value}")

def test_cpu_interval_type_fail():
    _FAIL_INTERVAL_TYPE = "10.0"
    with pytest.raises(
        CPUTypeError,
        match=r"^.*int or float type.*$",
    ) as raiseinfo:
        cpu = CPUDetect(
            threshold=80.0,
            mode=_CPU_MODE_PERCENT,
            interval=_FAIL_INTERVAL_TYPE,
        )
    print(f"CPU INTERVAL TYPE ERROR OUTPUT: {raiseinfo.value}")

def test_average(setup_cpu_percent):
    res = setup_cpu_percent.percent(_CPU_INTERVAL_DEFAULT,)
    assert res is not None
    assert isinstance(res,float)
    print(f'CPU AVERAGE RATIO: {res}%({type(res)})')
    assert res >= 0.0

def test_percent(setup_cpu_percent):
    res = setup_cpu_percent.percent(_CPU_INTERVAL_DEFAULT)
    assert res is not None
    assert isinstance(res,float)
    print(f'CPU PERCENT: {res}')

def test_percent_type_fail():
    _FAILE_INTERVAL_TYPE = "10.0"
    with pytest.raises(
        CPUTypeError,
        match=r"^.*int or float type.*$",
    ) as raiseinfo:
        CPUDetect.percent(interval=_FAILE_INTERVAL_TYPE)
    print(f"CPU PERCENT TYPE FAIL: {raiseinfo.value}")

def test_percpu(setup_cpu_percent):
    res = setup_cpu_percent.percent_percpu(_CPU_INTERVAL_DEFAULT)
    assert res is not None
    assert isinstance(res,list)
    print(f'CPU RATIO PER CPU: (list of float)')
    for cpu_number in range(len(res)):
        print(f'\tCPU AVERAGE RATIO[{cpu_number}]: {res[cpu_number]}%({type(res[cpu_number])})')
        assert isinstance(res[cpu_number],float)
        assert res[cpu_number] >= 0.0

def test_percent_percpu_type_fail():
    _FAILE_INTERVAL_TYPE = "10.0"
    with pytest.raises(
        CPUTypeError,
        match=r"^.*int or float type.*$",
    ) as raiseinfo:
        CPUDetect.percent_percpu(interval=_FAILE_INTERVAL_TYPE)
    print(f"CPU PERCENT TYPE FAIL: {raiseinfo.value}")

def test_loadavg(setup_cpu_percent):
    res = setup_cpu_percent.loadavg()
    assert res is not None
    assert isinstance(res,tuple)
    print(f'CPU LOAD AVG PER CPU: (list of float)')
    for cpu_number in range(len(res)):
        print(f'\tCPU LOAD AVG[{cpu_number}]: {res[cpu_number]}({type(res[cpu_number])})')
        assert isinstance(res[cpu_number],float)
        assert res[cpu_number] >= 0.0

def test_check_percent_true(setup_cpu_percent,mocker):
    permock = mocker.patch("resc.cpu.CPUDetect.percent")
    permock.return_value = 0.0
    res = setup_cpu_percent.check
    assert res is not None
    assert isinstance(res,bool)
    assert res is True
    assert permock.call_count == 1
    print(f'CPU TEST CPU PERCENT: {setup_cpu_percent.percent(0.0)}')
    print(f'CPU THRESHOLD PERCENT: {setup_cpu_percent.threshold}')
    print(f'CPU THRESHOLD CHECK: {res} (type(res))')

def test_check_percent_false(setup_cpu_percent,mocker):
    permock = mocker.patch("resc.cpu.CPUDetect.percent")
    permock.return_value = _CPU_OVER_PERCENT
    res = setup_cpu_percent.check
    assert res is not None
    assert isinstance(res,bool)
    assert res is False
    assert permock.call_count == 1
    print(f'CPU TEST CPU LOADAVG: {setup_cpu_percent.percent(0.0)}')
    print(f'CPU THRESHOLD LOADAVG: {setup_cpu_percent.threshold}')
    print(f'CPU THRESHOLD CHECK: {res} (type(res))')

def test_check_loadavg_true(setup_cpu_loadavg,mocker):
    permock = mocker.patch("resc.cpu.CPUDetect.loadavg")
    permock.return_value = 0.0
    res = setup_cpu_loadavg.check
    assert res is not None
    assert isinstance(res,bool)
    assert res is True
    assert permock.call_count == 1
    print(f'CPU TEST CPU LOADAVG: {setup_cpu_loadavg.loadavg(0.0)}')
    print(f'CPU THRESHOLD LOADAVG: {setup_cpu_loadavg.threshold}')
    print(f'CPU THRESHOLD CHECK: {res} (type(res))')

def test_check_loadavg_false(setup_cpu_loadavg,mocker):
    permock = mocker.patch("resc.cpu.CPUDetect.loadavg")
    permock.return_value = _CPU_OVER_LOADAVG
    res = setup_cpu_loadavg.check
    assert res is not None
    assert isinstance(res,bool)
    assert res is False
    assert permock.call_count == 1
    print(f'CPU TEST CPU LOADAVG: {setup_cpu_loadavg.loadavg(0.0)}')
    print(f'CPU THRESHOLD LOADAVG: {setup_cpu_loadavg.threshold}')
    print(f'CPU THRESHOLD CHECK: {res} (type(res))')


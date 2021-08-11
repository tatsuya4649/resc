import pytest
from unittest import mock
from resc.ps import *

@pytest.fixture(scope="function", autouse=False)
def ps_init():
    ps = PSDetect(
        threshold=1000,
        mode=PSDetectMode.NUMBER.value["name"],
        limits=PSDetectLimits.SOFT.value,
    )
    yield ps

@pytest.mark.parametrize(
    "threshold",[
    "80",
    b"80",
    [80],
    {"ps": 80},
])
def test_init_type_error(threshold):
    with pytest.raises(
        PSDetectTypeError
    ):
        ps = PSDetect(
            threshold=threshold
        )

@pytest.mark.parametrize(
     "mode",[
     90,
     90.0,
     b"mode",
     [PSDetectMode.PERCENT.value["name"]],
     {"mode":PSDetectMode.PERCENT.value["name"]},
])
def test_init_mode_error(mode):
    with pytest.raises(
        PSDetectTypeError
    ):
        ps = PSDetect(
            threshold=10.0,
            mode=mode,
        )

@pytest.mark.parametrize(
     "limits",[
     90,
     90.0,
     b"limits",
     [PSDetectLimits.SOFT.value],
     {"limits": PSDetectLimits.SOFT.value},
])
def test_init_limits_error(limits):
    with pytest.raises(
        PSDetectTypeError
    ):
        ps = PSDetect(
            threshold=10.0,
            limits=limits
        )

def test_maxps(ps_init):
    result = ps_init.maxps

    assert result is not None
    assert isinstance(result, tuple)

def test_percent(ps_init):
    result = ps_init.percent

    assert result is not None
    assert isinstance(result, float)
    print(f"PSDETECT PERCENT: {result}")

def test_resource(ps_init):
    result = ps_init.resource

    assert result is not None
    assert isinstance(result,str)

def test_check(ps_init):
    with mock.patch(
        "psutil.pids",
        return_value=[],
    ):
        result = ps_init.check
    assert result is True

    with mock.patch(
        "psutil.pids",
        return_value=[x for x in range(1000000)],
    ):
        result = ps_init.check
    assert result is False


import pytest
from unittest import mock
from resc.net import *


@pytest.fixture(scope="function")
def net_init():
    net = NetDetect(
        threshold=1000
    )
    yield net

@pytest.mark.parametrize(
    "threshold",[
    1000.0,
    "10000",
    b"1000",
    [1000],
    {"treshold": 1000},
])
def test_threshold_type_error(threshold):
    with pytest.raises(
        NetDetectTypeError
    ):
        net = NetDetect(
            threshold=threshold
        )


@pytest.mark.parametrize(
    "kind",[
    1000.0,
    10000,
    b"inet",
    ["inet"],
    {"kind": "inet"},
    True
])
def test_kind_type_error(kind):
    with pytest.raises(
        NetDetectTypeError
    ):
        net = NetDetect(
            threshold=1000,
            kind=kind
        )

def test_kind_value_error():
    with pytest.raises(
        NetDetectValueError
    ):
        net = NetDetect(
            threshold=1000,
            kind="a"
        )

def test_check(net_init):
    with mock.patch(
        "psutil.net_connections",
        return_value=[]
    ):
        result = net_init.check
    assert result is True
    with mock.patch(
        "psutil.net_connections",
        return_value=[x for x in range(100000)]
    ):
        result = net_init.check
    assert result is False

def test_resouece(net_init):
    result = net_init.resource
    assert result is not None
    assert isinstance(result, str)

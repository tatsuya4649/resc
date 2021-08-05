import pytest
from unittest.mock import Mock
import re
from resc.resclog.header import *
from resc.resclog.cons import *

@pytest.fixture(scope="module",autouse=True)
def header():
    header = RescLogHeader(
        identify=b"resc",
        sflags=0,
        headlen=0,
        bodylen=0,
        stdoutlen=0,
        stderrlen=0,
        datelen=0,
        overlen=0,
        funclen=0,
        filelen=0,
        remolen=0,
        sourlen=0,
        flag=0
    )
    yield header

@pytest.mark.parametrize(
    "flaglist",[
    ("Hello World"),
    (1),
    ({"flags":1}),
    (1.0),
])
def test_flag_type_failure(flaglist):
    with pytest.raises(
        RescLogHeaderTypeError
    ) as raiseinfo:
        RescLogHeader._flag(
            flaglist=flaglist
        )
    assert re.match(
        r'^flaglist must',
        raiseinfo.value.args[0],
    ) is not None

@pytest.mark.parametrize(
    "flaglist",[
    (["hello","world"]),
    ([1,23]),
    (["hello",RescLogFlag.DATE]),
])
def test_flag_element_type_failure(
    flaglist
):
    with pytest.raises(
        RescLogHeaderTypeError
    ) as raiseinfo:
        RescLogHeader._flag(
            flaglist=flaglist
        )
    assert re.match(
        r'^flaglist element must',
        raiseinfo.value.args[0],
    ) is not None

def test_flag():
    result = RescLogHeader._flag(
        [ x for x in RescLogFlag ]
    )
    assert result is not None
    assert isinstance(result, int)

def test_length():
    result = RescLogHeader.length()
    assert result is not None
    assert isinstance(result,int)
    assert result > 0

    print(f"RESCLOG HEADER SIZE: {result}")

def test_bytes(header):
    result = header.bytes

    assert result is not None
    assert isinstance(result,bytes)
    assert len(result) > 0

def test_flag_type():
    flags = [ x for x in RescLogFlag ]
    for flag in flags:
        print(f"RESC LOG FLAG TYPE: {flag} {type(flag.value)}")
        assert isinstance(flag.value,int)

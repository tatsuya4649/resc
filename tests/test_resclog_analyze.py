import pytest
import datetime
import io
from resc.resclog.analyze import *
from resc.resclog.header import *
from .conftest import _TEST_LOGFILE

@pytest.fixture(scope="module",autouse=True)
def analyzer():
    analyze = RescLogAnalyze(_TEST_LOGFILE)
    yield analyze

def test_path(analyzer):
    result = analyzer.path

    assert result is not None
    assert isinstance(result, str)
    print(f"ROG ANALYZE PATH: {result}")

@pytest.mark.parametrize(
    "logcontent",[
    "log",
    1,
    [b"log"],
    {"log",12}
])
def test_analyze_dict_type_error(
    analyzer,
    logcontent
):
    with pytest.raises(
        RescLogTypeError
    ) as raiseinfo:
        analyzer._analyze_dict(
            log=logcontent
        )

_DATE_CONTENT = \
    str(datetime.datetime.now()) \
    .encode("utf-8")
def test_analyze_dict_emergency(
    analyzer,
):
    _ERR_CONTENT = b"error content."
    _SFLAG = ( \
        RescLogSFlag.EME.value["flag"] | \
        RescLogSFlag.ERR.value["flag"]
    )

    emheader = RescLogEmergeHeader(
        identify = b"resc",
        sflag = _SFLAG,
        errlen = len(_ERR_CONTENT),
        datelen = len(_DATE_CONTENT),
    )

    buffer = io.BytesIO()
    buffer.write(emheader)
    buffer.write(_ERR_CONTENT)
    buffer.write(_DATE_CONTENT)

    result, log, resdict = analyzer._analyze_dict(
        buffer.getvalue()
    )
    print(emheader.identify == COMMONMAGIC.IDENTIFY)

    assert result is not None
    assert result is True
    assert log is not None
    assert isinstance(log, bytes)
    assert resdict is not None
    assert isinstance(resdict, dict)

def test_analyze_dict_normal(
    analyzer,
):
    _OVER_CONTENT = b"False"
    _FUNC_CONTENT = b"function"
    _FILE_CONTENT = b"file"
    _REMO_CONTENT = b"127.0.0.1"
    _SOUR_CONTENT = b"def hello()\n    ..."

    _BODY_LEN = \
        len(_DATE_CONTENT) + \
        len(_OVER_CONTENT) + \
        len(_FUNC_CONTENT) + \
        len(_FILE_CONTENT) + \
        len(_REMO_CONTENT) + \
        len(_SOUR_CONTENT)

    header = RescLogHeader(
        identify = b"resc",
        sflag = 0,
        headlen = RescLogHeader.length(),
        bodylen = _BODY_LEN,
        stdoutlen = 0,
        stderrlen = 0,
        datelen = len(_DATE_CONTENT),
        overlen = len(_OVER_CONTENT),
        funclen = len(_FUNC_CONTENT),
        filelen = len(_FILE_CONTENT),
        remolen = len(_REMO_CONTENT),
        sourlen = len(_SOUR_CONTENT),
        flag = (
            RescLogFlag.DATE.value | \
            RescLogFlag.OVER.value | \
            RescLogFlag.FUNC.value | \
            RescLogFlag.FILE.value | \
            RescLogFlag.REMO.value | \
            RescLogFlag.SOUR.value
        ),
    )

    buffer = io.BytesIO()
    buffer.write(header)
    buffer.write(_DATE_CONTENT)
    buffer.write(_OVER_CONTENT)
    buffer.write(_FUNC_CONTENT)
    buffer.write(_FILE_CONTENT)
    buffer.write(_REMO_CONTENT)
    buffer.write(_SOUR_CONTENT)

    print(f"RESC LOG NORMAL HEADER: {buffer.getvalue()}")

    res, log, resdict = analyzer._analyze_dict(
        log = buffer.getvalue()
    )

def test_analyze_dict_normal_unmatchlength(
    analyzer,
):
    _OVER_CONTENT = b"False"
    header = RescLogHeader(
        identify = b"resc",
        sflag = 0,
        headlen = RescLogHeader.length(),
        bodylen = 0,
        stdoutlen = 0,
        stderrlen = 0,
        datelen = len(_DATE_CONTENT),
        overlen = len(_OVER_CONTENT),
        funclen = 0,
        remolen = 0,
        sourlen = 0,
        flag = 0,
    )

    buffer = io.BytesIO()
    buffer.write(header)
    buffer.write(_DATE_CONTENT)
    buffer.write(_OVER_CONTENT)

    print(f"RESC LOG NORMAL HEADER: {buffer.getvalue()}")

    with pytest.raises(
        RescLogUnMatchError
    ) as raiseinfo:
        analyzer._analyze_dict(
            log = buffer.getvalue()
        )
    print(f"RESC LOG UNMATCH NORMAL HEADER: {raiseinfo.value}")

import pytest
import sys
import os
import datetime
from resc.resclog.resclog import *

_LOGPATH_DEFAULT = f"{os.path.expanduser('~')}/.resc/log/"

def _getlogpath(path):
    result = os.path.join(
        _LOGPATH_DEFAULT,
        path
    )
    return result

def _logpath_verify(logpath):
    dirs = os.path.join(
        os.path.dirname(logpath)
    ).split('/')
    paths = list()
    for path in dirs:
        paths.append(path)
        path = os.path.join(
            _LOGPATH_DEFAULT,
            "/".join(paths)
        )
        if os.path.isdir(path):
            sys.exit(1)

def _logpath_delete(logpath):
    dirs = os.path.join(
        os.path.dirname(logpath)
    ).split('/')
    paths = list()
    rmpaths = list()
    for path in dirs:
        paths.append(path)
        path = os.path.join(
            _LOGPATH_DEFAULT,
            "/".join(paths)
        )
        rmpaths.append(path)
    rmpaths.reverse()
    for path in rmpaths:
        os.rmdir(path)

@pytest.fixture(scope="module",autouse=True)
def rescloger():
    _LOGPATH = "hello/output/log"
    _logpath_verify(_LOGPATH)

    resclog = RescLog(
        logfile = _LOGPATH,
        format = [
            x for x in RescLogFormat
        ]
    )
    yield resclog

    _logpath_delete(_LOGPATH)

@pytest.fixture(scope="function",autouse=False)
def rescloger_notdefine():
    _LOGPATH = "notdefine/output/log"
    _logpath_verify(_LOGPATH)
    yield _LOGPATH
    _logpath_delete(_LOGPATH)


def test_default_directory(rescloger):
    result = rescloger.default_directory()
    assert result is not None
    assert isinstance(result, str)

def test_date(rescloger):
    result = rescloger.date
    assert result is not None
    assert isinstance(result, bytes)

@pytest.mark.parametrize(
    "datetime",[
    (datetime.datetime.now()),
])
def test_date_set(rescloger,datetime):
    rescloger.date = datetime

@pytest.mark.parametrize(
    "datetime",[
    (1),
    (2031.0),
    ("2030"),
    ([datetime.datetime.now()]),
    ({"datetime": datetime.datetime.now()}),
    (None),
])
def test_date_set_type_error(rescloger,datetime):
    with pytest.raises(
        RescLogTypeError
    ) as raiseinfo:
        rescloger.date = datetime

def test_date(rescloger):
    result = rescloger.over
    assert result is not None
    assert isinstance(result, bytes)

@pytest.mark.parametrize(
    "over",[
    ("False"),
    ([RescLogOver.FALSE]),
    ([RescLogOver.TRUE]),
    (1),
    (1.0),
    ({"False": 1}),
    (None),
])
def test_over_set_type_error(
    rescloger,
    over
):
    with pytest.raises(
        RescLogTypeError
    ) as raiseinfo:
        rescloger.over = over

def test_over_no_set(rescloger_notdefine):
    resclog = RescLog(
        logfile = rescloger_notdefine,
        format = [
            RescLogFormat.DATE
        ]
    )
    result = resclog.over
    assert result is not None
    assert isinstance(result, bytes)

def test_func(rescloger):
    result = rescloger.func

    assert result is None

@pytest.mark.parametrize(
    "func",[
    (1),
    (1.0),
    (b"func"),
    (["func"]),
    ({"func": "tion"}),
    (None),
])
def test_func_set_type_error(
    rescloger,
    func,
):
    with pytest.raises(
        RescLogTypeError
    ) as raiseinfo:
        rescloger.func = func

@pytest.mark.parametrize(
    "func",[
    ("function"),
])
def test_func_set(
    rescloger,
    func
):
    rescloger.func = func

def test_remo(rescloger):
    result = rescloger.remo

    assert result is None

@pytest.mark.parametrize(
    "remo",[
    (b"remo"),
    (1),
    (1.0),
    (["remo"]),
    ({"remo": 1}),
    (None),
])
def test_remo_set_type_error(
    rescloger,
    remo
):
    with pytest.raises(
        RescLogTypeError
    ) as raiseinfo:
        rescloger.remo = remo

@pytest.mark.parametrize(
    "remo",[
    "remo"
])
def test_remo_set(
    rescloger,
    remo
):
    rescloger.remo = remo

def test_sour(
    rescloger,
):
    result = rescloger.sour

    assert result is None

@pytest.mark.parametrize(
    "sour",[
    "sour",
    1,
    1.0,
    ["sour"],
    {"sour": 1},
    (None),
])
def test_sour_set_type_error(
    rescloger,
    sour,
):
    with pytest.raises(
        RescLogTypeError
    ) as raiseinfo:
        rescloger.sour = sour

@pytest.mark.parametrize(
    "sour",[
    b"sour"
])
def test_sour_set(
    rescloger,
    sour
):
    rescloger.sour = sour

def test_file(
    rescloger,
):
    result = rescloger.file

    assert result is None

@pytest.mark.parametrize(
    "file",[
    1,
    1.0,
    ["file"],
    {"file": 1},
    b"file",
])
def test_file_set_type_error(
    rescloger,
    file
):
    with pytest.raises(
        RescLogTypeError
    ) as raiseinfo:
        rescloger.file = file

@pytest.mark.parametrize(
    "file",[
    "file"
])
def test_file_set(
    rescloger,
    file
):
    rescloger.file = file

def test_stdout(rescloger):
    result = rescloger.stdout

    assert result is not None
    assert isinstance(result, bytes)
    assert result == bytes()

@pytest.mark.parametrize(
    "stdout",[
    "stdout",
    ["stdout"],
    1,
    1.0,
    {"stdout": b"stdout"}
])
def test_stdout_set_type_error(
    rescloger,
    stdout
):
    with pytest.raises(
        RescLogTypeError
    ) as raiseinfo:
        rescloger.stdout = stdout

@pytest.mark.parametrize(
    "stdout",[
    b"stdout",
    [b"hello",b"world"],
])
def test_stdout_set(
    rescloger,
    stdout
):
    rescloger.stdout = stdout

def test_stderr(rescloger):
    result = rescloger.stderr

    assert result is not None
    assert isinstance(result, bytes)
    assert result == bytes()

@pytest.mark.parametrize(
    "stderr",[
    "stderr",
    ["stderr"],
    1,
    1.0,
    {"stderr": b"stderr"}
])
def test_stderr_set_type_error(
    rescloger,
    stderr
):
    with pytest.raises(
        RescLogTypeError
    ) as raiseinfo:
        rescloger.stderr = stderr

@pytest.mark.parametrize(
    "stderr",[
    b"stderr",
    [b"hello",b"world"],
])
def test_stderr_set(
    rescloger,
    stderr
):
    rescloger.stderr = stderr

def test_body(rescloger):
    result = rescloger.body

    assert result is not None
    assert isinstance(result, bytes)

def test_head(rescloger):
    result = rescloger.header()

    assert result is not None
    assert isinstance(result, bytes)

    print(f"RESCLOG HEADER: {result}")

def test_define_resclog(rescloger):
    result = rescloger.define_resclog

    assert result is not None
    assert isinstance(result, list)
    assert len([x for x in result if not isinstance(x, str)]) == 0

def test_format_meta(rescloger):
    result = rescloger.format_meta

    assert result is not None
    assert isinstance(result, str)

def test_not_found(rescloger_notdefine):
    _full_path = _getlogpath(rescloger_notdefine)
    resclog = RescLog(
        logfile = rescloger_notdefine
    )
    resclog._not_found(_full_path)

    if os.path.isfile(
        _full_path
    ):
        os.remove(_full_path)

def test_not_found_except(rescloger_notdefine):
    _full_path = _getlogpath(rescloger_notdefine)
    resclog = RescLog(
        logfile = rescloger_notdefine
    )
    with pytest.raises(
        SystemExit
    ) as raiseinfo:
        resclog._not_found(
            os.path.join(
                _full_path,
                "not/found/except/"
            )
        )

def test_write(rescloger):
    _full_path = _getlogpath(rescloger.pure_log)
    if os.path.isfile(_full_path):
        sys.exit(1)
    rescloger.write(
        over = RescLogOver.FALSE,
        sflag = 0,
    )
    if os.path.getsize(_full_path) == 0:
        sys.exit(1)
    with open(_full_path, "rb") as f:
        print(f'RESC LOG WRITE: {f.read()}')
    if os.path.isfile(
        _full_path
    ):
        os.remove(rescloger.logfile)

@pytest.mark.parametrize(
    "over, sflag",[
    ("hello", "world"),
    ("False", 1),
    (RescLogOver.TRUE, "1"),
    (RescLogOver.TRUE, RescLogSFlag.ERR),
])
def test_write_type_error(rescloger,over,sflag):
    _full_path = _getlogpath(rescloger.pure_log)
    if os.path.isfile(_full_path):
        sys.exit(1)
    with pytest.raises(
        RescLogTypeError
    ) as raiseinfo:
        rescloger.write(
            over = over,
            sflag = sflag,
        )

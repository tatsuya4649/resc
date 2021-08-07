"""
Common Definition of test
"""
import sys
import os
import re
import pytest
import subprocess
from .docker_setup import RemoteHost

class _RemoteSingleton:
    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self):
        ...
    def __call__(self):
        if self._instance is not None:
            self._instance = None
            return True
        else:
            return False

@pytest.fixture(scope="session",autouse=True)
def _remote_singleton():
    _rsingleton = _RemoteSingleton()
    yield _rsingleton

@pytest.fixture(scope="session",autouse=False)
def _remote_init():
    remote_host = RemoteHost()
    yield remote_host

    # If use remote host, shutdown at end of test
    if remote_host.use:
        remote_host.shutdown()

@pytest.fixture(scope="module",autouse=False)
def setup_remote_host(_remote_singleton,_remote_init):
    """
    setup and shutdown of Remote Host(made using Docker)
    """
    if _remote_singleton():
        _remote_init.startup()
        yield _remote_init
    else:
        yield

_KEY_PATH = \
    os.path.join(
        os.path.dirname(
            os.path.abspath(
                __file__
            )
        ),
        'test_data/test_resc'
    )

_TEST_LOGFILE = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "test_data/output"
    )
)

def _cronlist():
    process = subprocess.Popen(
        "command crontab -l",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        shell=True,
    )
    stderr = process.stderr.read()
    if process.wait() != 0 and \
        re.match(
            r"^no crontab",
            stderr,
        ) is None:
        sys.exit(1)
    return process

def _crondelete():
    process = subprocess.Popen(
        "command crontab -r",
        stderr=subprocess.PIPE,
        universal_newlines=True,
        shell=True,
    )
    stderr = process.stderr.read()
    if process.wait() != 0 and \
        re.match(
            r"^no crontab",
            stderr,
        ) is None:
        sys.exit(1)
    return process

def _cronregister(register):
    if len(register) == 0:
        return
    process = subprocess.Popen(
        "command crontab",
        stdin = subprocess.PIPE,
        shell=True,
    )
    process.communicate(
        input=register.encode("utf-8"),
        timeout=5,
    )
    if process.wait() != 0:
        sys.exit(1)
    return process


@pytest.fixture(scope="function",autouse=False)
def cron_empty():
    process = _cronlist()
    crontab_list = process.stdout.read()
    _crondelete()
    yield
    _crondelete()
    _cronregister(crontab_list)

@pytest.fixture(scope="function",autouse=False)
def cron_noempty():
    _LINE = "* * * * * echo 'Hello World'\n"
    process = _cronlist()
    crontab_list = process.stdout.read()
    _crondelete()
    _cronregister(_LINE)
    yield _LINE
    _crondelete()
    _cronregister(crontab_list)

_USER_PATH = os.path.expanduser("~")
_REGFILE = os.path.join(
    f"{_USER_PATH}",
    ".resc/register"
)
_EXREG = "* * * * * resc --help\n"

class _RegDir:
    def __init__(self, path):
        self._target = path
        self._paths = list()
        self._makepaths = list()
    def __enter__(
        self
    ):
        for path in os.path.dirname(
            self._target
        ).split('/'):
            self._paths.append(path)
            dire = "/".join(self._paths)
            if not os.path.isdir(dire) and \
            len(dire) > 0:
                os.mkdir(dire)
                self._makepaths.append(dire)
        return self
    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        for dire in reversed(self._makepaths):
            if os.path.isdir(dire) and \
        len(os.listdir(dire)) == 0:
                os.rmdir(dire)

@pytest.fixture(scope="function",autouse=False)
def register_empty():
    with _RegDir(_REGFILE):
        prereg = None
        if os.path.isfile(_REGFILE):
            with open(_REGFILE,"r") as f:
                prereg = f.read()
            with open(_REGFILE,"w") as f:
                f.truncate(0)
        yield

        if (prereg is None or len(prereg) == 0) and \
            os.path.isfile(_REGFILE):
            os.remove(_REGFILE)
        else:
            if (prereg is not None and len(prereg) > 0):
                with open(_REGFILE,"w") as f:
                    f.write(prereg)

@pytest.fixture(scope="function",autouse=False)
def register_noempty():
    with _RegDir(_REGFILE):
        prereg = None
        if os.path.isfile(_REGFILE):
            with open(_REGFILE,"r") as f:
                prereg = f.read()
            with open(_REGFILE,"w") as f:
                f.truncate(0)
        with open(_REGFILE,"w") as f:
            f.write(_EXREG)
        yield
        with open(_REGFILE,"w") as f:
            f.truncate(0)

        if (prereg is None or len(prereg) == 0) and \
            os.path.isfile(_REGFILE):
            os.remove(_REGFILE)
        else:
            if (prereg is not None and len(prereg) > 0):
                with open(_REGFILE,"w") as f:
                    f.write(prereg)

@pytest.fixture(scope="function",autouse=False)
def same_cron_register():
    with _RegDir(_REGFILE):
        # Register file only _EXREG
        prereg = None
        if os.path.isfile(_REGFILE):
            with open(_REGFILE,"r") as f:
                prereg = f.read()
            with open(_REGFILE,"w") as f:
                f.truncate(0)
        with open(_REGFILE,"w") as f:
            f.write(_EXREG)
        # Crontab only _EXREG
        process = _cronlist()
        crontab_list = process.stdout.read()
        _crondelete()
        _cronregister(_EXREG)
        yield
        # Undo
        _crondelete()
        _cronregister(crontab_list)

        with open(_REGFILE,"w") as f:
            f.truncate(0)
        if prereg is None or len(prereg) == 0 and \
            os.path.isfile(_REGFILE):
            os.remove(_REGFILE)
        else:
            with open(_REGFILE,"w") as f:
                f.write(prereg)

@pytest.fixture(scope="function",autouse=False)
def logfile_empty():
    with _RegDir(_TEST_LOGFILE):
        _logcontent = None
        if os.path.isfile(_TEST_LOGFILE):
            with open(_TEST_LOGFILE,"rb") as f:
                _logcontent = f.read()
            with open(_TEST_LOGFILE,"wb") as f:
                f.truncate(0)
        yield _TEST_LOGFILE

        if (_logcontent is None  is None or len(_logcontent) == 0) \
            and os.path.isfile(_TEST_LOGFILE):
            os.remove(_TEST_LOGFILE)
        else:
            with open(_TEST_LOGFILE,"wb") as f:
                f.write(_logcontent)

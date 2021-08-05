"""
Common Definition of test
"""
import sys
import os
import re
import pytest
import subprocess

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
    _cronregister(crontab_list)

@pytest.fixture(scope="function",autouse=False)
def cron_noempty():
    process = _cronlist()
    crontab_list = process.stdout.read()
    _crondelete()
    _cronregister("* * * * * echo 'Hello World'\n")
    yield
    _crondelete()
    _cronregister(crontab_list)

@pytest.fixture(scope="function",autouse=False)
def register_empty():
    _USER_PATH = os.path.expanduser("~")
    _FILE = os.path.join(
        f"{_USER_PATH}",
        ".resc/register"
    )
    with open(_FILE,"r") as f:
        prereg = f.read()
    with open(_FILE,"w") as f:
        f.truncate(0)
    yield
    with open(_FILE,"w") as f:
        f.write(prereg)

@pytest.fixture(scope="function",autouse=False)
def register_noempty():
    _USER_PATH = os.path.expanduser("~")
    _FILE = os.path.join(
        f"{_USER_PATH}",
        ".resc/register"
    )
    _EXREG = "* * * * * resc --help"
    with open(_FILE,"r") as f:
        prereg = f.read()
    with open(_FILE,"w") as f:
        f.truncate(0)
    with open(_FILE,"w") as f:
        f.write(_EXREG)
    yield
    with open(_FILE,"w") as f:
        f.truncate(0)
    with open(_FILE,"w") as f:
        f.write(prereg)

@pytest.fixture(scope="function",autouse=False)
def same_cron_register():
    _USER_PATH = os.path.expanduser("~")
    _FILE = os.path.join(
        f"{_USER_PATH}",
        ".resc/register"
    )
    _EXREG = "* * * * * resc --help\n"
    # Register file only _EXREG
    with open(_FILE,"r") as f:
        prereg = f.read()
    with open(_FILE,"w") as f:
        f.truncate(0)
    with open(_FILE,"w") as f:
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
    with open(_FILE,"w") as f:
        f.truncate(0)
    with open(_FILE,"w") as f:
        f.write(prereg)

@pytest.fixture(scope="function",autouse=False)
def logfile_empty():
    _TEST_LOGFILE = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "test_data/output"
        )
    )
    with open(_TEST_LOGFILE,"rb") as f:
        _logcontent = f.read()
    with open(_TEST_LOGFILE,"wb") as f:
        f.truncate(0)
    yield _TEST_LOGFILE
    with open(_TEST_LOGFILE,"wb") as f:
        f.write(_logcontent)

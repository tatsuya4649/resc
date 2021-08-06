import pytest
from unittest import mock
from unittest.mock import Mock
from resc.cron import *
import _io
import subprocess
_INTERVAL=10
_INTERVAL_MODE="interval"
_INTERVAL_SCALE="day"
_INTERVAL_COMMAND = "echo 'Hello World'"
_INTERVAL_STR="* * * * *"

def test_cron():
	cron = Cron(
		command='echo "Hello world"',
		interval_str="*/1 0-3 * * *",
	)
	res = cron.interval_str
	assert res is not None
	assert isinstance(res,str)
	print(f"CRON INTERVAL STRING \"{res}\"")

	res = cron.totalline
	assert res is not None
	assert isinstance(res,str)
	print(f"CRON TOTAL LINE \"{res}\"")

	res = cron.register()
	assert res is not None
	assert isinstance(res,int)
	print(f"CRON REGISTER END STATUS \"{res}\"")
	res = cron.list
	assert res is not None
	assert isinstance(res,list)
	print(f"CRON LISTS {res}")
	res = cron.count
	assert res is not None
	assert isinstance(res,int)
	print(f"CRON COUNT {res}")

	res = cron.delete()
	assert res is not None
	assert isinstance(res,int)
	print(f"CRON DELETE END STATUS \"{res}\"")

@pytest.mark.parametrize(
    "command",[
    1.0,
    1,
    ["command"],
    b"command",
    {"comand": 1}
])
def test_cron_init_command_type_error(command):
    with pytest.raises(
        CronTypeError
    ) as raiseinfo:
        cron = Cron(
            command=command,
            interval_str=_INTERVAL_STR
        )

@pytest.mark.parametrize(
    "interval_str",[
    1.0,
    1,
    ["interval_str"],
    b"interval_str",
    {"interval_str": 1}
])
def test_cron_init_interval_str_type_error(interval_str):
    with pytest.raises(
        CronTypeError
    ) as raiseinfo:
        cron = Cron(
            command=_INTERVAL_COMMAND,
            interval_str=interval_str
        )

def test_cron_init_command_none_error():
    with pytest.raises(
        CronValueError
    ) as raiseinfo:
        cron = Cron(
            command=_INTERVAL_COMMAND,
            interval_str=None
        )

def test_cron_init_available_error():
    with mock.patch(
        "resc.cron.Cron.available",
        return_value = False
    ):
        with pytest.raises(
            CronCommandError
        ) as raiseinfo:
            cron = Cron(
                command=_INTERVAL_COMMAND,
                interval_str=_INTERVAL_STR
            )

def test_cron_list_none(cron_empty):
    cron = Cron(
        command=_INTERVAL_COMMAND,
        interval_str=_INTERVAL_STR
    )
    result = cron._list
    assert result is None

def test_cron_register_none(cron_empty):
    cron = Cron(
        command=_INTERVAL_COMMAND,
        interval_str=_INTERVAL_STR
    )
    result = cron.register()

def test_cron_list_none2(cron_empty):
    cron = Cron(
        command=_INTERVAL_COMMAND,
        interval_str=_INTERVAL_STR
    )
    result = cron.list
    assert result is None

def test_cron_delete_none(cron_empty):
    cron = Cron(
        command=_INTERVAL_COMMAND,
        interval_str=_INTERVAL_STR
    )
    result = cron.delete()
    assert result is None

def test_available_false():
    with mock.patch(
        "subprocess.run",
    ) as popen:
        popen.configure_mock(**{
            "returncode.return_value": 1
        })
        result = Cron.available()
        assert result is False

import _io
def test_path_stderr():
    cron = Cron(
        command=_INTERVAL_COMMAND,
        interval_str=_INTERVAL_STR
    )
    with mock.patch(
        "subprocess.Popen"
    ) as popen:
        instance = popen.return_value
        instance.communicate.return_value = \
            (b"", b"Error")
        with pytest.raises(
            CronCommandError
        ) as raiseinfo:
            cron._path

def test_path_stdout():
    cron = Cron(
        command=_INTERVAL_COMMAND,
        interval_str=_INTERVAL_STR
    )
    with mock.patch(
        "subprocess.Popen"
    ) as popen:
        instance = popen.return_value
        instance.communicate.return_value = \
            (b"", b"")
        with pytest.raises(
            CronCommandError
        ) as raiseinfo:
            cron._path

def test_delete_cronlists_zero(cron_noempty):
    cron = Cron(
        command=_INTERVAL_COMMAND,
        interval_str=_INTERVAL_STR
    )
    cron._totalline = cron_noempty
    result = cron.delete()
    assert result == 0

from .conftest import _cronregister
def test_delete_cronlists_nonzero(cron_noempty):
    cron = Cron(
        command=_INTERVAL_COMMAND,
        interval_str=_INTERVAL_STR
    )
    cron._totalline = cron_noempty
    _cronregister(cron_noempty)
    result = cron.delete()
    assert result == 0

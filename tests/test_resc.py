import os
import sys
import pytest
from unittest import mock
import paramiko

from resc import Resc
from resc import *
from resc.rescerr import *
from resc.cpu import *
from resc.memory import *
from resc.disk import *
from resc.cron import *
import inspect
import subprocess
from .conftest import _KEY_PATH, _OUTPUT, _RESCDIR
from .test_resc_register import hello
from ._resc_common import _INTERVAL, setup_resc


"""

Basic Test

"""

def test_resc_threshold(setup_resc):
    res = setup_resc.thresholds
    assert res is not None
    assert isinstance(res,dict)
    print(f'RESC THRESHOLDS {res}')

def test_resc_checks(setup_resc):
    res = setup_resc.checks
    assert res is not None
    assert isinstance(res,dict)
    print(f'RESC CHECKS {res}')

def test_resc_over_one(setup_resc):
    res = setup_resc.over_one
    assert res is not None
    assert isinstance(res,bool)
    print(f'RESC OVER ONE {res}')

def test_resc_overs(setup_resc):
    res = setup_resc.overs
    assert res is not None
    assert isinstance(res,list)
    print(f'RESC OVERS {res}')

"""

Init Test

"""
def test_cpu_type_failure():
    _FAIL_CPU = 'cpu'

    with pytest.raises(
        RescTypeError,
        match=r"^.*None or dict.*$",
    ) as raiseinfo:
        resc = Resc(
            cpu=_FAIL_CPU,
        )
    print(f"RESC INIT CPU TYPE FAILURE: {raiseinfo.value}")

def test_cpu_dict_failure():
    _FAIL_CPU_DICT = {
        "threshold": 80.0, # Good
        "cpu": "cpu", # Bad
    }
    with pytest.raises(
        RescKeyError,
    ) as raiseinfo:
        resc = Resc(
            cpu=_FAIL_CPU_DICT,
        )
    print(f"RESC INIT CPU TYPE FAILURE: {raiseinfo.value}")

def test_cpu_init_dict_string():
    cpu_dict = {
            "threshold":80,
            "interval":_INTERVAL,
            "mode":"percent",
    }
    resc = Resc(
        cpu = cpu_dict,
    )
    cpu_detect = resc._cpu
    assert cpu_detect is not None
    assert isinstance(cpu_detect,CPUDetect)
    assert cpu_dict["threshold"] == cpu_detect._threshold
    assert cpu_dict["interval"] == cpu_detect._interval
    assert cpu_dict["mode"] == cpu_detect._mode.value["name"]

def test_cpu_init_none():
    """
        if cpu is not passed,
        _cpu and _cpu_dict must be none.
    """
    resc = Resc(
        memory={"threshold":80},
        disk={"threshold":80,"path":"/"},
    )
    assert resc._cpu is None
    assert resc._cpu_dict is None

def test_memory_type_failure():
    _FAIL_MEMORY = 'memory'

    with pytest.raises(
        RescTypeError,
        match=r"^.*None or dict.*$",
    ) as raiseinfo:
        resc = Resc(
            memory=_FAIL_MEMORY,
        )
    print(f"RESC INIT MEMORY TYPE FAILURE: {raiseinfo.value}")

def test_memory_dict_failure():
    _FAIL_MEMORY_DICT = {
        "threshold": 80.0, # Good
        "memory": "memory", # Bad
    }
    with pytest.raises(
        RescKeyError,
    ) as raiseinfo:
        resc = Resc(
            memory=_FAIL_MEMORY_DICT,
        )
    print(f"RESC INIT MEMORY TYPE FAILURE: {raiseinfo.value}")

def test_memory_init_dict_string():
    memory_dict = {
            "threshold":80,
            "mode":"percent",
    }
    resc = Resc(
        memory = memory_dict,
    )
    memory_detect = resc._memory
    assert memory_detect is not None
    assert isinstance(memory_detect,MemoryDetect)
    assert memory_dict["threshold"] == memory_detect._threshold
    assert memory_dict["mode"] == memory_detect._mode.value["name"]

def test_memory_init_none():
    """
        if cpu is not passed,
        _cpu and _cpu_dict must be none.
    """
    resc = Resc(
        cpu={"threshold":80},
        disk={"threshold":80,"path":"/"},
    )
    assert resc._memory is None
    assert resc._memory_dict is None

def test_disk_type_failure():
    _FAIL_DISK = 'disk'

    with pytest.raises(
        RescTypeError,
        match=r"^.*None or dict.*$",
    ) as raiseinfo:
        resc = Resc(
            disk=_FAIL_DISK,
        )
    print(f"RESC INIT DISK TYPE FAILURE: {raiseinfo.value}")

def test_disk_dict_failure():
    _FAIL_DISK_DICT = {
        "threshold": 80.0, # Good
        "disk": "disk", # Bad
    }
    with pytest.raises(
        RescKeyError,
    ) as raiseinfo:
        resc = Resc(
            disk=_FAIL_DISK_DICT,
        )
    print(f"RESC INIT DISK TYPE FAILURE: {raiseinfo.value}")

def test_disk_init_dict_string():
    disk_dict = {
            "threshold": 80,
            "mode": "percent",
            "path": "/",
    }
    resc = Resc(
        disk = disk_dict,
    )
    disk_detect = resc._disk
    assert disk_detect is not None
    assert isinstance(disk_detect,DiskDetect)
    assert disk_dict["threshold"] == disk_detect._threshold
    assert disk_dict["mode"] == disk_detect._mode.value["name"]
    assert disk_dict["path"] == disk_detect._path

def test_disk_init_none():
    """
        if cpu is not passed,
        _cpu and _cpu_dict must be none.
    """
    resc = Resc(
        cpu={"threshold":80},
        memory={"threshold":80},
    )
    assert resc._disk is None
    assert resc._disk_dict is None

"""

Cron Test

"""
def test_crontab_command_failure(setup_resc,mocker):
    cron_available = mocker.patch("resc.cron.Cron.available")
    cron_available.return_value = False

    with pytest.raises(
        CronCommandError,
        match=r"^not found crontab command.*$",
    ) as raiseinfo:
        setup_resc.register(
            trigger = "* * * * *",
        )
    print((
         f"RESC REGISTER CRONTAB NOT"
         f"FOUND OUTPUT: {raiseinfo.value}"
         ))

def test_register_command_failure(setup_resc,mocker):
    command_patch = mocker.patch(
        "resc._resc.Resc._check_command",
    )
    command_patch.return_value = 1
    print(command_patch.return_value)
    with pytest.raises(
        RescCronError,
    ) as raiseinfo:
        setup_resc.register(
            trigger = "* * * * *",
        )
    print((
         f"RESC REGISTER COMMAND NOT"
         f"FOUND OUTPUT: {raiseinfo.value}"
         ))

def test_crons_get(setup_resc):
    import hashlib
    import resc
    i = 0
    while True:
        number = f"{i}".encode("utf-8")
        _SCRIPT_PATH = f"script{hashlib.md5(number).hexdigest()}"
        if not os.path.isfile(_SCRIPT_PATH):
            break
        i += 1

    with open(_SCRIPT_PATH, "w") as fp:
            fp.write("Hello World")

    with mock.patch(
        "resc._resc.Resc._which_resc"
    ) as which_resc:
        which_resc.return_value = ""

        setup_resc._call_first = False
        with pytest.raises(
            SystemExit
        ) as raiseinfo:
            setup_resc._crons_get("* * * *", _SCRIPT_PATH)
    assert raiseinfo.value.args[0][0] == 1

    assert not os.path.isfile(_SCRIPT_PATH)

def test_source_write(setup_resc):
    _FILENAME = "filename"
    setup_resc._resclog = RescLog()
    filename = setup_resc._source_write(
        filename=_FILENAME,
        func_source="def hello():\n    ...",
        funcname="hello",
        func_args={
            "args": ["hello"],
            "kwargs": {
                "test": 1,
                "test2": 1.0,
                "test3": ["list"],
                "test4": {"dict": 1},
                "test5": "world",
                "test6": b"world",
            }
        },
    )
    assert filename is not None
    assert isinstance(filename, str)
    assert os.path.isfile(_FILENAME)

    os.remove(_FILENAME)


"""
Package Test
"""
import resc
def test_package_path_none(setup_resc,monkeypatch):
    monkeypatch.setattr(resc,'__path__',None)

    with pytest.raises(
        RescValueError
    ) as raiseinfo:
        setup_resc._package_path

    print(f"RESC PACKAGE IS NONE: {raiseinfo.value}")

def test_package_path_type_failure(setup_resc,monkeypatch):
    monkeypatch.setattr(resc,'__path__',"resc")

    with pytest.raises(
        RescTypeError
    ) as raiseinfo:
        setup_resc._package_path
    print(f"RESC PACKAGE TYPE ERROR: {raiseinfo.value}")

def test_package_path_length_failure(setup_resc,monkeypatch):
    monkeypatch.setattr(resc,'__path__',["resc","resc"])

    with pytest.raises(
        RescValueError
    ) as raiseinfo:
        setup_resc._package_path
    print(f"RESC PACKAGE LENGTH ERROR: {raiseinfo.value}")

"""
Remote Test
"""
@pytest.mark.usefixtures("setup_remote_host")
def test_remote_key(
    register_undos,
):
    resc = Resc(
        cpu={"threshold":0.0,"interval":_INTERVAL},
        memory={"threshold":80},
        disk={"threshold":80,"path":"/"},
    )
    @resc.register(
        trigger = "* * * * *",
        rescdir = _RESCDIR,
        outputfile = _OUTPUT,
        ip = "localhost",
        port = 20022,
        username="root",
        key_path = _KEY_PATH,
        call_first=True,
    )
    def hello():
        print("hello resc!!!")
    hello()

@pytest.mark.usefixtures("setup_remote_host")
def test_remote_password(
    register_undos,
):
    resc = Resc(
        cpu={"threshold":0.0,"interval":_INTERVAL},
        memory={"threshold":80},
        disk={"threshold":80,"path":"/"},
    )
    @resc.register(
        trigger = "* * * * *",
        rescdir = _RESCDIR,
        outputfile = _OUTPUT,
        ip = "localhost",
        port = 20022,
        username = "root",
        password = "test_resc",
        call_first=True,
    )
    def hello():
        print("hello resc!!!")
    hello()

@pytest.mark.usefixtures("setup_remote_host")
def test_over_one_ssh(
    register_undos,
    setup_resc
):
    setup_resc.register(
        trigger="* * * * *",
        ip="localhost",
        port=20022,
        username="root",
        key_path=_KEY_PATH,
    )(hello)()
    ssh = setup_resc._resclog._ssh
    result = setup_resc.over_one_ssh(ssh,setup_resc._resclog)
    print(f"RESC SSH OVER ONE SSH: {result}")

@pytest.mark.usefixtures("setup_remote_host")
def test_over_one_ssh_connect_error(
    setup_resc,
    register_undos,
    setup_remote_host,
    mocker,
):
    # To disable SSH ping of register
    mocker.patch(
        "resc.ssh.SSH.ssh_ping",
        side_effect = lambda : None,
    )
    # Key Path Error
    setup_resc.register(
        trigger="* * * * *",
        ip="localhost",
        port=20022,
        username="root",
        key_path="dummy_key",
    )(hello)()
    ssh = setup_resc._resclog._ssh
    assert len(setup_resc._resclog.stderr) == 0
    result = setup_resc.over_one_ssh(ssh,setup_resc._resclog)
    assert len(setup_resc._resclog.stderr) > 0

    with pytest.raises(
        RescSSHFileNotFoundError
    ) as raiseinfo:
        ssh._connect()
    assert str(raiseinfo.value).encode("utf-8") == \
        setup_resc._resclog.stderr
    print(f"RESC SSH FILE NOT FOUND: {str(raiseinfo.value).encode('utf-8')}")

    # Connection Error
    setup_resc.register(
        trigger="* * * * *",
        ip="localhost",
        port=20021,
        username="root",
        key_path=_KEY_PATH,
    )(hello)()
    ssh = setup_resc._resclog._ssh
    assert len(setup_resc._resclog.stderr) == 0
    result = setup_resc.over_one_ssh(ssh,setup_resc._resclog)
    assert len(setup_resc._resclog.stderr) > 0

    with pytest.raises(
        RescSSHConnectionError
    ) as raiseinfo:
        ssh._connect()
    assert str(raiseinfo.value).encode("utf-8") == \
        setup_resc._resclog.stderr

    print(f"RESC SSH CONNECTION ERROR: {str(raiseinfo.value).encode('utf-8')}")

    # Timeout Error
    setup_resc.register(
        trigger="* * * * *",
        ip="localhost",
        port=20022,
        username="root",
        key_path=_KEY_PATH,
        timeout=0,
    )(hello)()
    ssh = setup_resc._resclog._ssh
    assert len(setup_resc._resclog.stderr) == 0
    result = setup_resc.over_one_ssh(ssh,setup_resc._resclog)
    assert len(setup_resc._resclog.stderr) > 0

    with pytest.raises(
        RescSSHTimeoutError
    ) as raiseinfo:
        ssh._connect()
    assert str(raiseinfo.value).encode("utf-8") == \
        setup_resc._resclog.stderr

    print(f"RESC SSH TIMEOUT ERROR: {str(raiseinfo.value).encode('utf-8')}")

@pytest.mark.usefixtures("setup_remote_host")
def test_over_one_ssh_session_error(
    register_undos,
    setup_resc,
    mocker,
):
    # Session Error
    def raiseSSHException():
        return paramiko\
            .ssh_exception\
            .SSHException("Session Error")

    setup_resc.register(
        trigger="* * * * *",
        ip="localhost",
        port=20022,
        username="root",
        key_path=_KEY_PATH,
    )(hello)()
    ssh = setup_resc._resclog._ssh

    mocker.patch(
        "paramiko.SSHClient.connect",
        side_effect = raiseSSHException
    )
    assert len(setup_resc._resclog.stderr) == 0
    result = setup_resc.over_one_ssh(ssh,setup_resc._resclog)
    assert len(setup_resc._resclog.stderr) > 0

    with pytest.raises(
        RescSSHError
    ) as raiseinfo:
        ssh._connect()
    assert str(raiseinfo.value).encode("utf-8") == \
        setup_resc._resclog.stderr

    print(f"RESC SSH EXCEPTION: {str(raiseinfo.value).encode('utf-8')}")

@pytest.mark.usefixtures("setup_remote_host")
def test_send_script(
    register_undos,
    setup_resc,
):
    setup_resc.register(
        trigger = "* * * * *",
        ip = "localhost",
        port = 20022,
        username = "root",
        key_path = _KEY_PATH,
    )(hello)()
    ssh = setup_resc._resclog._ssh
    setup_resc._send_script(ssh,ssh._connect(),__file__,setup_resc._resclog)
    print(f"RESC SEND SCRIPT: \"{__file__}\" for test")

@pytest.mark.usefixtures("setup_remote_host")
def test_over_one_ssh(
    register_undos,
    setup_resc,
):
    setup_resc.register(
        trigger = "* * * * *",
        ip = "localhost",
        port = 20022,
        username = "root",
        key_path = _KEY_PATH,
    )(hello)()
    result = setup_resc.over_one_ssh(
        ssh = setup_resc._resclog._ssh,
        resclog = setup_resc._resclog
    )
    assert result is not None

@pytest.mark.usefixtures("setup_remote_host")
def test_over_one_ssh_scp_none(
    register_undos,
    setup_resc,
    mocker,
):
    setup_resc.register(
        trigger = "* * * * *",
        ip = "localhost",
        port = 20022,
        username = "root",
        key_path = _KEY_PATH,
    )(hello)()
    mocker.patch(
        "resc._resc.Resc._send_script",
        return_value = False
    )
    result = setup_resc.over_one_ssh(
        ssh = setup_resc._resclog._ssh,
        resclog = setup_resc._resclog
    )
    assert result is not None
    assert result is False

@pytest.mark.usefixtures("setup_remote_host")
def test_over_one_recv_exit_status(
    register_undos,
    setup_resc,
    mocker,
):
    setup_resc.register(
        trigger = "* * * * *",
        ip = "localhost",
        port = 20022,
        username = "root",
        key_path = _KEY_PATH,
    )(hello)()

    mocker.patch(
        "resc._resc.Resc._startup_script",
        return_value = (1,["hello world".encode("utf-8")]),
    )

    with pytest.raises(
        RescServerError
    ) as raiseinfo:
        setup_resc.over_one_ssh(
            setup_resc._resclog._ssh,
            setup_resc._resclog,
        )
    print(f"RESC OVER_ONE_SSH SERVER ERROR: {raiseinfo.value}")
    assert "hello world".encode("utf-8") == setup_resc._resclog.stderr

@pytest.mark.usefixtures("setup_remote_host")
def test_over_one_recv_q_status_1(
    register_undos,
    setup_resc,
    mocker,
):
    setup_resc.register(
        trigger = "* * * * *",
        ip = "localhost",
        port = 20022,
        username = "root",
        key_path = _KEY_PATH,
    )(hello)()

    mocker.patch(
        "resc._resc.Resc._resc_q",
        return_value = (1,["stdout".encode("utf-8")],["stderr".encode("utf-8")]),
    )

    result = setup_resc.over_one_ssh(
        setup_resc._resclog._ssh,
        setup_resc._resclog,
    )
    print(f"RESC OVER_ONE_SSH STATUS: {result}")
    assert result is False
    assert "stdout".encode("utf-8") == setup_resc._resclog.stdout
    assert "stderr".encode("utf-8") == setup_resc._resclog.stderr

@pytest.mark.usefixtures("setup_remote_host")
def test_over_one_recv_q_status_0(
    register_undos,
    setup_resc,
    mocker,
):
    setup_resc.register(
        trigger = "* * * * *",
        ip = "localhost",
        port = 20022,
        username = "root",
        key_path = _KEY_PATH,
    )(hello)()

    mocker.patch(
        "resc._resc.Resc._resc_q",
        return_value = (0,["stdout".encode("utf-8")],["stderr".encode("utf-8")]),
    )

    result = setup_resc.over_one_ssh(
        setup_resc._resclog._ssh,
        setup_resc._resclog,
    )
    print(f"RESC OVER_ONE_SSH STATUS: {result}")
    assert result is False
    assert "stdout".encode("utf-8") == setup_resc._resclog.stdout
    assert "stderr".encode("utf-8") == setup_resc._resclog.stderr

@pytest.mark.usefixtures("setup_remote_host")
def test_over_one_recv_q_status_255(
    register_undos,
    setup_resc,
    mocker,
):
    setup_resc.register(
        trigger = "* * * * *",
        ip = "localhost",
        port = 20022,
        username = "root",
        key_path = _KEY_PATH,
    )(hello)()

    mocker.patch(
        "resc._resc.Resc._resc_q",
        return_value = (255,["stdout".encode("utf-8")],["stderr".encode("utf-8")]),
    )

    result = setup_resc.over_one_ssh(
        setup_resc._resclog._ssh,
        setup_resc._resclog,
    )
    print(f"RESC OVER_ONE_SSH STATUS: {result}")
    assert result is True
    assert "stdout".encode("utf-8") == setup_resc._resclog.stdout
    assert "stderr".encode("utf-8") == setup_resc._resclog.stderr

"""
Type Test
"""
def test_ip_type(setup_resc):
    with pytest.raises(
        RescTypeError
    ) as raiseinfo:
        result = setup_resc._ip_type(100)
    print(f"RESC IP TYPE FAILURE: {raiseinfo.value}")
def test_port_type(setup_resc):
    with pytest.raises(
        RescTypeError
    ) as raiseinfo:
        result = setup_resc._port_type("100")
    print(f"RESC PORT TYPE FAILURE: {raiseinfo.value}")
def test_username_type(setup_resc):
    with pytest.raises(
        RescTypeError
    ) as raiseinfo:
        result = setup_resc._username_type(100)
    print(f"RESC USERNAME TYPE FAILURE: {raiseinfo.value}")
"""
Another Test
"""
def test_resc_arg():
    resc = Resc(
        cpu={
            "threshold":80,
            "interval":_INTERVAL,
            "mode": "percent",
        },
        memory={
            "threshold":80,
            "mode": "percent",
        },
        disk={
            "threshold":80,
            "mode": "percent",
            "path":"/",
        },
    )
    result = resc._resc_arg

    assert result is not None
    assert isinstance(result,str)

    print(f"RESC ARG: {result}")

@pytest.mark.parametrize(
    "threshold, mode, interval",[
    (80.0, "percent", 10.0),
    (80.0, None, 10.0),
    (80.0, "percent", None),
])
def test_resc_arg_cpu(
    threshold, mode, interval
):
    resc = Resc(
        cpu = {
            "threshold": threshold,
            "mode": mode,
            "interval": interval,
        }
    )
    result = resc._resc_arg

    assert result is not None
    assert isinstance(result, str)
    print(f"RESC ARG CPU: {result}")

@pytest.mark.parametrize(
    "threshold, mode",[
    (80.0, "percent"),
    (80.0, None),
])
def test_resc_arg_memory(
    threshold, mode
):
    resc = Resc(
        memory = {
            "threshold": threshold,
            "mode": mode,
        }
    )
    result = resc._resc_arg

    assert result is not None
    assert isinstance(result, str)
    print(f"RESC ARG MEMORY: {result}")

@pytest.mark.parametrize(
    "threshold, mode",[
    (80.0, "percent"),
    (80.0, None),
])
def test_resc_arg_memory(
    threshold, mode
):
    resc = Resc(
        memory = {
            "threshold": threshold,
            "mode": mode,
        }
    )
    result = resc._resc_arg

    assert result is not None
    assert isinstance(result, str)
    print(f"RESC ARG MEMORY: {result}")

@pytest.mark.parametrize(
    "threshold, path, mode",[
    (80.0, "/" , "percent"),
    (80.0, "/", None),
])
def test_resc_arg_disk(
    threshold, path, mode
):
    resc = Resc(
        disk = {
            "threshold": threshold,
            "path": path,
            "mode": mode,
        }
    )
    result = resc._resc_arg

    assert result is not None
    assert isinstance(result, str)
    print(f"RESC ARG DISK: {result}")

def test_check(setup_resc):
    result = setup_resc.checks
    assert result is not None
    assert isinstance(result, dict)
    result = setup_resc.checks
    assert result is not None
    assert isinstance(result, dict)


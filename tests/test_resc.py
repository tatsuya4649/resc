import os
import sys
import pytest

from resc import Resc
from resc import *
from resc.rescerr import *
from resc.cpu import *
from resc.memory import *
from resc.disk import *
from resc.cron import *
import inspect
import subprocess

_INTERVAL=0

"""

Basic Test

"""
@pytest.fixture(scope="module",autouse=False)
def setup_resc():
    resc = Resc(
        cpu={"threshold":80,"interval":_INTERVAL},
        memory={"threshold":80},
        disk={"threshold":80,"path":"/"},
    )
    yield resc

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

def test_register_trigger_str_failure(setup_resc):
    with pytest.raises(
        RescTypeError
    ) as raiseinfo:
        setup_resc.register(
            trigger = ["* * * * *"],
        )
    print(
        f"RESC REGISTER TRIGGER TYPE FAILURE:"
        f"{raiseinfo.value}"
    )
def test_register_rescdir_type_failure(setup_resc):
    with pytest.raises(
        RescTypeError,
    ) as raiseinfo:
        setup_resc.register(
            trigger="* * * * *",
            rescdir = 10,
        )
    print(
        "RESC REGISTER RESCDIR TYPE OUTPUT: "
        f"{raiseinfo.value}"
    )

def test_register_rescdir(setup_resc):
    os.environ.pop(setup_resc._RESCPATH_ENV,None)
    setup_resc.register(
        trigger="* * * * *",
    )
    assert os.getenv(setup_resc._RESCPATH_ENV) is not None
    print(
        "RESC REGISTER DEFAULT RESC PATH: "
        f"{os.getenv(setup_resc._RESCPATH_ENV)}"
    )

def test_register_rescdir2(setup_resc):
    os.environ.pop(setup_resc._RESCPATH_ENV,None)
    os.environ[setup_resc._RESCPATH_ENV] = \
        "rescs"
    setup_resc.register(
        trigger="* * * * *",
    )
    assert os.getenv(setup_resc._RESCPATH_ENV) is not None
    print(
        "RESC REGISTER DEFAULT RESC PATH: "
        f"{os.getenv(setup_resc._RESCPATH_ENV)}"
    )

def test_register_rescdir3(setup_resc):
    os.environ.pop(setup_resc._RESCPATH_ENV,None)
    setup_resc.register(
        trigger="* * * * *",
        rescdir="rescs",
    )
    assert os.getenv(setup_resc._RESCPATH_ENV) is not None
    print(
        "RESC REGISTER DEFAULT RESC PATH: "
        f"{os.getenv(setup_resc._RESCPATH_ENV)}"
    )


def test_register_outputfile_type_failure(setup_resc):
    with pytest.raises(
        RescTypeError,
    ) as raiseinfo:
        setup_resc.register(
            trigger="* * * * *",
            outputfile=10,
        )
    print(
        "RESC REGISTER OUTPUTFILE TYPE OUTPUT: "
        f"{raiseinfo.value}"
    )

def test_register_outputfile_env(setup_resc):
    setup_resc.register(
        trigger="* * * * *",
    )
    assert setup_resc._resclog is not None
    assert setup_resc._resclog.log is False
    assert setup_resc._resclog.pure_log is None
    assert setup_resc._resclog.logfile is None
    print(
        "RESC OUTPUTFILE IS NONE:\n"
        f"\tRESCLOG LOG: {setup_resc._resclog.log}\n"
        f"\tRESCLOG PURE_LOG: {setup_resc._resclog.pure_log}\n"
        f"\tRESCLOG LOGFILE: {setup_resc._resclog.logfile}"
    )

def test_register_outputfile_env2(setup_resc):
    os.environ.pop(setup_resc._RESCOUTPUT_ENV,None)

    os.environ[setup_resc._RESCOUTPUT_ENV] = "output"
    setup_resc.register(
        trigger = "* * * * *",
    )
    assert setup_resc._resclog is not None
    assert setup_resc._resclog.log is True
    assert setup_resc._resclog.pure_log is not None
    assert setup_resc._resclog.logfile is not None
    print(
        "RESC OUTPUTFILE IS NONE:\n"
        f"\tRESCLOG LOG: {setup_resc._resclog.log}\n"
        f"\tRESCLOG PURE_LOG: {setup_resc._resclog.pure_log}\n"
        f"\tRESCLOG LOGFILE: {setup_resc._resclog.logfile}"
    )

    assert os.environ[setup_resc._RESCOUTPUT_ENV] is not None

def test_register_local_ssh(setup_resc):
    setup_resc.register(
        trigger = "* * * * *",
    )
    assert setup_resc._resclog.remo is None

# Dummy function
def hello(): ...

def test_register_remote_ssh(setup_resc):
    setup_resc.register(
        trigger = "* * * * *",
        ip="128.0.0.1", # No username and password(keypath file)
    )(hello)()
    assert setup_resc._resclog.remo is not None
    assert setup_resc._resclog._ssh is None

    setup_resc.register(
        trigger = "* * * * *",
        ip="128.0.0.1",
        username="tatsuya", # No password(keypath file)
    )(hello)()
    assert setup_resc._resclog.remo is not None
    assert setup_resc._resclog._ssh is None

    setup_resc.register(
        trigger = "* * * * *",
        ip="128.0.0.1",
        username="tatsuya",
        password="example",
    )(hello)()
    assert setup_resc._resclog.remo is not None
    assert setup_resc._resclog._ssh is not None

    setup_resc.register(
        trigger = "* * * * *",
        ip="128.0.0.1",
        username="tatsuya",
        key_path="example",
    )(hello)()
    assert setup_resc._resclog.remo is not None
    assert setup_resc._resclog._ssh is not None

def test_register_remote_ssh_type_failure(setup_resc):
    # IP Address Raise Error Test
    print(f"RESC SSH REMOTE TYPE ERROR")
    with pytest.raises(
        RescTypeError,
    ) as raiseinfo:
        setup_resc.register(
            trigger = "* * * * *",
            ip=128,
            username="tatsuya",
            key_path="example",
        )(hello)()
    print(f"\tIP: {raiseinfo.value}")
    with pytest.raises(
        RescTypeError,
    ) as raiseinfo:
        setup_resc.register(
            trigger = "* * * * *",
            ip="129.0.0.1",
            port = "22",
            username="tatsuya",
            key_path="example",
        )(hello)()
    print(f"\tPORT: {raiseinfo.value}")
    with pytest.raises(
        RescTypeError,
    ) as raiseinfo:
        setup_resc.register(
            trigger = "* * * * *",
            ip="129.0.0.1",
            username=100,
            key_path="example",
        )(hello)()
    print(f"\tUSERNAME: {raiseinfo.value}")
    with pytest.raises(
        RescTypeError,
    ) as raiseinfo:
        setup_resc.register(
            trigger = "* * * * *",
            ip="129.0.0.1",
            username="tatsuya",
            password=10,
        )(hello)()
    print(f"\tPASSWORD: {raiseinfo.value}")
    with pytest.raises(
        RescTypeError,
    ) as raiseinfo:
        setup_resc.register(
            trigger = "* * * * *",
            ip="129.0.0.1",
            username="tatsuya",
            key_path=10,
        )(hello)()
    print(f"\tKEY_PATH: {raiseinfo.value}")
    with pytest.raises(
        RescTypeError,
    ) as raiseinfo:
        setup_resc.register(
            trigger = "* * * * *",
            ip="129.0.0.1",
            username="tatsuya",
            key_path="example",
            timeout="10",
        )(hello)()
    print(f"\tTIMEOUT: {raiseinfo.value}")

"""

Register SOURCE Test

"""
import re
_DUMMY_DIR = ".dummy"
def test_source_dir(setup_resc):
    test_dir = re.sub(
        r'^~',
        f'{os.path.expanduser("~")}',
        os.path.join(
            setup_resc._RESCPATH_DEFAULT,
            _DUMMY_DIR
        )
    )
    if os.path.exists(test_dir):
        for file in os.listdir(
            test_dir
        ):
            os.remove(os.path.join(test_dir,file))
        os.rmdir(test_dir)

    setup_resc.register(
        trigger = "* * * * *",
        rescdir = _DUMMY_DIR,
    )(hello)()

    assert os.path.exists(test_dir)

def test_register_nonlog(setup_resc):
    # Delete env variable of output path
    os.environ.pop(setup_resc._RESCOUTPUT_ENV,None)
    setup_resc.register(
        trigger = "* * * * *",
        outputfile=None,
    )(hello)()

def test_register_resc_command_not_found(
    setup_resc,
    mocker,
):
    resc_patch = mocker.patch(
        "resc._resc.Resc._which_resc"
    )
    resc_patch.return_value = ""

    with pytest.raises(
        SystemExit
    ) as raiseinfo:
        setup_resc.register(
            trigger = "* * * * *",
            outputfile=None,
        )(hello)()

    print(f"RESC SYS EXIT: {raiseinfo.value}")

def test_register_crons_register_type(
    setup_resc,
):
    setup_resc._crons = 1
    with pytest.raises(
        RescTypeError
    ) as raiseinfo:
        setup_resc._crons_register()
    print(f"RESC CRONS TYPE FAILURE: {raiseinfo.value}")

def test_register_crons_length_zero(
    setup_resc,
):
    result = setup_resc._crons_register()
    assert result is None
    assert len(setup_resc._crons) == 0

def test_register():
    resc = Resc(
        cpu={"threshold":80,"interval":_INTERVAL},
        memory={"threshold":80},
        disk={"threshold":80,"path":"/"},
    )
    @resc.register(
        trigger="*/1 * * * *",
        rescdir="rescs"
    )
    def hello():
        print("hello resc!!!")
    hello()

    os.environ["RESCPATH"] = "rescs"
    os.environ["RESCOUTPUT"] = "rescoutput.txt"
    @resc.register("*/1 * * * *")
    def world(a,b):
        import time
        print(time.time())
    world(1,b="resc test script")

def test_remote():
    resc = Resc(
        cpu={"threshold":0.0,"interval":_INTERVAL},
        memory={"threshold":80},
        disk={"threshold":80,"path":"/"},
    )
    @resc.register(
        trigger="* * * * *",
        rescdir="rescs",
        outputfile="output",
        ip="13.231.122.182",
        username="ubuntu",
        password="example",
        call_first=True,
    )
    def hello():
        print("hello resc!!!")
    hello()

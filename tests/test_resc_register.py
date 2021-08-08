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
import subprocess
from .conftest import *
from ._resc_common import setup_resc,_INTERVAL


@pytest.fixture(scope="function",autouse=False)
def setup_resc():
    resc = Resc(
        cpu={"threshold":80,"interval":_INTERVAL},
        memory={"threshold":80},
        disk={"threshold":80,"path":"/"},
    )
    yield resc


@pytest.fixture(scope="function", autouse=False)
def temp_rescdir():
    direxists = False
    with tempfile.TemporaryDirectory(
        prefix="tmp_test_resc_"
    ) as dirpath:
        if os.path.exists(_RESCDIR_FULL):
            direxists = True
            tmp_dir = shutil.move(_RESCDIR_FULL, dirpath)
        yield
        if os.path.exists(_RESCDIR_FULL):
            for file in os.listdir(_RESCDIR_FULL):
                os.remove(
                    os.path.join(
                        _RESCDIR_FULL,
                        file
                    )
                )
            os.rmdir(_RESCDIR_FULL)

        if direxists:
            shutil.move(tmp_dir, os.path.dirname(_RESCDIR_FULL))

@pytest.mark.parametrize(
    "trigger",[
    ["* * * *"],
    {"trigger": "* * * * *"},
    10,
    10.0,
    b"* * * * *"
])
def test_register_trigger_type_error(setup_resc,trigger):
    with pytest.raises(
        RescTypeError
    ) as raiseinfo:
        setup_resc.register(
            trigger = trigger
        )
    print(
        f"RESC REGISTER TRIGGER TYPE FAILURE:"
        f"{raiseinfo.value}"
    )
@pytest.mark.parametrize(
    "rescdir",[
    ["rescs"],
    {"rescdir": "rescs"},
    10,
    10.0,
    b"rescs",
])
def test_register_rescdir_type_error(setup_resc, rescdir):
    with pytest.raises(
        RescTypeError,
    ) as raiseinfo:
        setup_resc.register(
            trigger="* * * * *",
            rescdir = rescdir,
        )
    print(
        "RESC REGISTER RESCDIR TYPE OUTPUT: "
        f"{raiseinfo.value}"
    )

def test_register_rescdir_auto(setup_resc):
    os.environ.pop(setup_resc._RESCDIR_ENV,None)
    setup_resc.register(
        trigger="* * * * *",
    )
    assert os.getenv(setup_resc._RESCDIR_ENV) is not None
    print(
        "RESC REGISTER DEFAULT RESC DIR: "
        f"{os.getenv(setup_resc._RESCDIR_ENV)}"
    )

def test_register_rescdir2_auto(setup_resc):
    os.environ.pop(setup_resc._RESCDIR_ENV,None)
    os.environ[setup_resc._RESCDIR_ENV] = \
        "rescs"
    setup_resc.register(
        trigger="* * * * *",
    )
    assert os.getenv(setup_resc._RESCDIR_ENV) is not None
    print(
        "RESC REGISTER DEFAULT RESC DIR: "
        f"{os.getenv(setup_resc._RESCDIR_ENV)}"
    )

def test_register_rescdir3_auto(setup_resc):
    os.environ.pop(setup_resc._RESCDIR_ENV,None)
    setup_resc.register(
        trigger="* * * * *",
        rescdir="rescs",
    )
    assert os.getenv(setup_resc._RESCDIR_ENV) is not None
    print(
        "RESC REGISTER DEFAULT RESC DIR: "
        f"{os.getenv(setup_resc._RESCDIR_ENV)}"
    )


@pytest.mark.parametrize(
    "output",[
    ["output.txt"],
    {"output": "output"},
    10,
    10.0,
    b"output",
])
def test_register_outputfile_type_error(setup_resc, output):
    with pytest.raises(
        RescTypeError,
    ) as raiseinfo:
        setup_resc.register(
            trigger="* * * * *",
            outputfile=output,
        )
    print(
        "RESC REGISTER OUTPUTFILE TYPE OUTPUT: "
        f"{raiseinfo.value}"
    )

def test_register_outputfile_env(setup_resc):
    os.environ.pop(Resc._RESCOUTPUT_ENV,None)
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
# test consistent value
from .conftest import _RESCDIR_FULL, _RESCDIR, _OUTPUT, _OUTPUT_FULL

def test_register_remote_ssh(
    setup_resc,
    register_undos,
    register_env,
    temp_rescdir,
):
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

    with pytest.raises(
        RescSSHError
    ):
        setup_resc.register(
            trigger = "* * * * *",
            ip="128.0.0.1",
            username="tatsuya",
            password="example",
        )(hello)()
#    assert setup_resc._resclog.remo is not None
#    assert setup_resc._resclog._ssh is not None

    with pytest.raises(
        RescSSHError
    ):
        setup_resc.register(
            trigger = "* * * * *",
            ip="128.0.0.1",
            username="tatsuya",
            key_path="example",
        )(hello)()
#    assert setup_resc._resclog.remo is not None
#    assert setup_resc._resclog._ssh is not None

def test_register_remote_ssh_type_failure(
    setup_resc,
    register_undos,
    register_env,
    temp_rescdir,
):
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
import tempfile
import shutil
def test_source_dir(
    setup_resc,
    register_undos,
    temp_rescdir
):
    setup_resc.register(
        trigger = "* * * * *",
        rescdir = _RESCDIR,
    )(hello)()
    assert os.path.isdir(_RESCDIR_FULL)
        

def test_register_nonlog(
    setup_resc,
    register_undos,
    temp_rescdir
):
    # Delete env variable of output path
    os.environ.pop(setup_resc._RESCOUTPUT_ENV,None)
    setup_resc.register(
        trigger = "* * * * *",
        outputfile=None,
    )(hello)()

def test_register_resc_command_not_found(
    setup_resc,
    mocker,
    register_undos,
    temp_rescdir,
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

def test_register(
    register_undos,
    temp_rescdir,
):
    resc = Resc(
        cpu={"threshold":80,"interval":_INTERVAL},
        memory={"threshold":80},
        disk={"threshold":80,"path":"/"},
    )
    @resc.register(
        trigger="*/1 * * * *",
        rescdir=_RESCDIR
    )
    def hello():
        print("hello resc!!!")
    hello()

    os.environ[Resc._RESCDIR_ENV] = _RESCDIR
    os.environ[Resc._RESCOUTPUT_ENV] = _OUTPUT
    @resc.register("*/1 * * * *")
    def world(a,b):
        import time
        print(time.time())
    world(1,b="resc test script")

def test_register_first_tab_test(
    register_undos,
    temp_rescdir,
):
    resc = Resc(
        cpu={"threshold":80,"interval":_INTERVAL},
        memory={"threshold":80},
        disk={"threshold":80,"path":"/"},
    )
    @resc.register(
        trigger="*/1 * * * *",
        rescdir=_RESCDIR
    )
    def first_tab():
        ...
    first_tab()
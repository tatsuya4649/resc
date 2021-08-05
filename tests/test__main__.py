import sys
import re
import pytest
from unittest import mock
from unittest.mock import patch, Mock
from resc.__main__ import main
import resc
from resc import *
from resc.cpu import *
from resc.memory import *
from resc.disk import *

@pytest.mark.parametrize(
    # @param over: CPU resource exceed threshold.
    "threshold, mode, interval, over",[
    (80.0, "percent", 1, True),
    (80.0, "percent", 1, False),
    (None, "percent", 1, False),
    (None, "percent", 1, True),
    (10.0, None, None, True),
    (10.0, None, None, False),
])
def test_cpu(threshold, mode, interval, over):
    args = list()
    progname = "test__main__/cpu"
    args.append(progname)
    if threshold is not None:
        args.append("--cpu_t")
        args.append(f"{threshold}")
    if mode is not None:
        args.append("--cpu_mode")
        args.append(f"{mode}")
    if interval is not None:
        args.append("--cpu_interval")
        args.append(f"{interval}")

    with mock.patch(
        'sys.argv',
        args,
    ):
        with mock.patch(
            'resc.Resc.over_one',
            over,
        ):
            with pytest.raises(
                SystemExit
            ) as raiseinfo:
                # Main function of __main__.py
                main()

            if threshold is None:
                assert int(
                raiseinfo.value.args[0]
                ) == 1
            else:
                if over:
                    assert int(
                raiseinfo.value.args[0]
                    ) == 255
                else:
                    assert int(
                raiseinfo.value.args[0]
                    ) == 0
    print(f"__MAIN__ CPU SYSTEM EXIT: {raiseinfo.value}")

@pytest.mark.parametrize(
    "mode",[
    ("percent"),
    ("loadavg"),
    ("per"),
    ("avg"),
])
def test_cpu_mode(mode):
    args = list()
    progname = "test__main__/cpu/mode"
    args.append(progname)
    args.append("--cpu_mode")
    args.append(mode)
    args.append("--cpu_t")
    args.append(f"{80.0}")
    args.append("--cpu_interval")
    args.append("0")

    mode_list = [
        v.value["name"]
        for k, v in CPUDetectMode.__members__.items()
    ]
    with mock.patch("sys.argv",args):
        with pytest.raises(
            SystemExit
        ) as raiseinfo:
            main()
        if mode not in mode_list:
            assert raiseinfo.value.args[0] == 1
        else:
            assert raiseinfo.value.args[0] != 1

@pytest.mark.parametrize(
    # @param over: Memory resource exceed threshold.
    "threshold, mode, over",[
    (80.0, "percent", True),
    (80.0, "percent", False),
    (None, "percent", False),
    (None, "percent", True),
    (10.0, None, True),
    (10.0, None, False),
])
def test_memory(threshold, mode, over):
    args = list()
    progname = "test__main__/memory"
    args.append(progname)

    if threshold is not None:
        args.append("--mem_t")
        args.append(f"{threshold}")
    if mode is not None:
        args.append("--mem_mode")
        args.append(f"{mode}")

    with mock.patch("sys.argv",args):
        with mock.patch(
            'resc.Resc.over_one',
            over,
        ):
            with pytest.raises(
                SystemExit
            ) as raiseinfo:
                # Main function of __main__.py
                main()

            if threshold is None:
                assert int(
                raiseinfo.value.args[0]
                ) == 1
            else:
                if over:
                    assert int(
                raiseinfo.value.args[0]
                    ) == 255
                else:
                    assert int(
                raiseinfo.value.args[0]
                    ) == 0
    print(f"__MAIN__ MEMORY SYSTEM EXIT: {raiseinfo.value}")

@pytest.mark.parametrize(
    "mode",[
    ("percent"),
    ("loadavg"),
    ("per"),
    ("avg"),
])
def test_memory_mode(mode):
    args = list()
    progname = "test__main__/memory/mode"
    args.append(progname)
    args.append("--mem_mode")
    args.append(mode)
    args.append("--mem_t")
    args.append(f"{80.0}")

    mode_list = [
        v.value["name"]
        for k, v in MemoryDetectMode.__members__.items()
    ]
    with mock.patch("sys.argv",args):
        with pytest.raises(
            SystemExit
        ) as raiseinfo:
            main()
        if mode not in mode_list:
            assert raiseinfo.value.args[0] == 1
        else:
            assert raiseinfo.value.args[0] != 1

@pytest.mark.parametrize(
    # @param over: Memory resource exceed threshold.
    "threshold, path, mode, over",[
    (80.0, "/", "percent", True),
    (80.0, "/", "percent", False),
    (None, "/", "percent", False),
    (None, "/", "percent", True),
    (10.0, None, None, True),
    (10.0, None, None, False),
    (10.0, "/", None, True),
    (10.0, "/", None, False),
])
def test_disk(threshold, path, mode, over):
    args = list()
    progname = "test__main__/disk"
    args.append(progname)

    if threshold is not None:
        args.append("--disk_t")
        args.append(f"{threshold}")
    if path is not None:
        args.append("--disk_path")
        args.append(f"{path}")
    if mode is not None:
        args.append("--disk_mode")
        args.append(f"{mode}")

    with mock.patch("sys.argv",args):
        with mock.patch(
            'resc.Resc.over_one',
            over,
        ):
            with pytest.raises(
                SystemExit
            ) as raiseinfo:
                # Main function of __main__.py
                main()

            if threshold is None or path is None:
                assert int(
                raiseinfo.value.args[0]
                ) == 1
            else:
                if over:
                    assert int(
                raiseinfo.value.args[0]
                    ) == 255
                else:
                    assert int(
                raiseinfo.value.args[0]
                    ) == 0
    print(f"__MAIN__ DISK SYSTEM EXIT: {raiseinfo.value}")

@pytest.mark.parametrize(
    "mode",[
    ("percent"),
    ("loadavg"),
    ("per"),
    ("avg"),
])
def test_disk_mode(mode):
    args = list()
    progname = "test__main__/disk/mode"
    args.append(progname)
    args.append("--disk_mode")
    args.append(mode)
    args.append("--disk_t")
    args.append(f"{80.0}")
    args.append("--disk_path")
    args.append("/")

    mode_list = [
        v.value["name"]
        for k, v in DiskDetectMode.__members__.items()
    ]
    with mock.patch("sys.argv",args):
        with pytest.raises(
            SystemExit
        ) as raiseinfo:
            main()
        if mode not in mode_list:
            assert raiseinfo.value.args[0] == 1
        else:
            assert raiseinfo.value.args[0] != 1

@pytest.mark.parametrize(
    "q, over",[
    (True, True),
    (True, False),
    (False, True),
    (False, False),
])
def test_q(q, over, capfd):
    args = list()
    progname = "test__main__/disk/mode"
    args.append(progname)
    args.append("--cpu_t")
    args.append("90.0")
    args.append("--cpu_interval")
    args.append("0")
    if q:
        args.append("-q")
    with mock.patch("sys.argv",args):
        with mock.patch(
            "resc.Resc.over_one",
            over
        ):
            with pytest.raises(
                SystemExit
            ):
                main()
        if not q:
            if over:
                assert re.match(
            r"^exceed",
            capfd.readouterr().out,
            ) is not None
            else:
                assert re.match(
            r"^no exceed",
            capfd.readouterr().out,
            ) is not None
        else:
            assert len(capfd.readouterr().out) == 0

def test_log_analyze(capfd):
    test_output = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "test_data/output"
        )
    )
    args = list()
    progname = "test__main__/disk/mode"
    args.append(progname)
    args.append("--log")
    args.append(test_output)
    with mock.patch("sys.argv",args):
        with pytest.raises(
            SystemExit
        ) as raiseinfo:
            main()
    assert raiseinfo.value.args[0] == 0

def test_log_path_error(capfd):
    args = list()
    progname = "test__main__/disk/mode"
    args.append(progname)
    args.append("--log")
    args.append("output")
    with mock.patch("sys.argv",args):
        with pytest.raises(
            SystemExit
        ) as raiseinfo:
            main()
    assert re.match(
        r"^not found",
        capfd.readouterr().out,
    ) is not None

def test_log_unmatch_error():
    test_output = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "test_data/output"
        )
    )
    args = list()
    progname = "test__main__/disk/mode"
    args.append(progname)
    args.append("--log")
    args.append(test_output)
    with mock.patch("sys.argv",args):
        with mock.patch(
            "resc.RescLogAnalyze.analyze",
            side_effect = RescLogUnMatchError("unmatch")
        ):
            with pytest.raises(
                SystemExit
            ) as raiseinfo:
                main()

def test_log_exception():
    test_output = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "test_data/output"
        )
    )
    args = list()
    progname = "test__main__/disk/mode"
    args.append(progname)
    args.append("--log")
    args.append(test_output)
    with mock.patch("sys.argv",args):
        with mock.patch(
            "resc.RescLogAnalyze.analyze",
            side_effect = Exception("exception")
        ):
            with pytest.raises(
                SystemExit
            ) as raiseinfo:
                main()

def test_log_server():
    args = list()
    progname = "test__main__/start_server"
    args.append(progname)
    args.append("--log_server")

    def server():
        ...

    resc.__main__.start_server = Mock()
    resc.__main__.start_server.side_effect = server
    with mock.patch("sys.argv",args):
        with pytest.raises(
            SystemExit
        ) as raiseinfo:
            main()
    assert raiseinfo.value.args[0] == 0

def test_delete_register():
    args = list()
    progname = "test__main__/delete_register"
    args.append(progname)
    args.append("--delete_register")
    with mock.patch("sys.argv",args):
        with pytest.raises(
            SystemExit
        ) as raiseinfo:
            main()
    assert raiseinfo.value.args[0] == 0

def test_delete_register_no_crontab_no_register(cron_empty,register_empty):
    args = list()
    progname = "test__main__/delete_register_no"
    args.append(progname)
    args.append("--delete_register")
    with mock.patch("sys.argv",args):
        with pytest.raises(
            SystemExit
        ) as raiseinfo:
            main()
    assert raiseinfo.value.args[0] == 0

def test_delete_register_no_crontab_register(cron_empty,register_noempty):
    args = list()
    progname = "test__main__/delete_register"
    args.append(progname)
    args.append("--delete_register")
    with mock.patch("sys.argv",args):
        with pytest.raises(
            SystemExit
        ) as raiseinfo:
            main()
    assert raiseinfo.value.args[0] == 0

def test_delete_register_crontab_no_register(cron_noempty,register_empty):
    args = list()
    progname = "test__main__/delete_register"
    args.append(progname)
    args.append("--delete_register")
    with mock.patch("sys.argv",args):
        with pytest.raises(
            SystemExit
        ) as raiseinfo:
            main()
    assert raiseinfo.value.args[0] == 0

def test_delete_register_crontab_register(cron_noempty,register_noempty):
    args = list()
    progname = "test__main__/delete_register_register"
    args.append(progname)
    args.append("--delete_register")
    with mock.patch("sys.argv",args):
        with pytest.raises(
            SystemExit
        ) as raiseinfo:
            main()
    assert raiseinfo.value.args[0] == 0

def test_delete_register_same_reg_cro(
    same_cron_register
):
    args = list()
    progname = "test__main__/delete_register_same"
    args.append(progname)
    args.append("--delete_register")
    with mock.patch("sys.argv",args):
        with pytest.raises(
            SystemExit
        ) as raiseinfo:
            main()
    assert raiseinfo.value.args[0] == 0

def test_not_found():
    test_output = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "test_data/output"
        )
    )
    args = list()
    progname = "test__main__/not_found"
    args.append(progname)
    args.append("--not_found")
    args.append(f"{test_output}")
    with mock.patch("sys.argv",args):
        with pytest.raises(
            SystemExit
        ) as raiseinfo:
            main()
    assert raiseinfo.value.args[0] == 0

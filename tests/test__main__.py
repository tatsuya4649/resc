import sys
import pytest
from unittest import mock
from unittest.mock import patch
from resc.__main__ import main
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

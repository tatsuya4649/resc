import pytest
import os
from unittest import mock
from resc import *
import subprocess
from .conftest import _OUTPUT, _OUTPUT_FULL
from resc.resclog.analyze import RescLogAnalyze


_resc = Resc(
    cpu={
        "threshold":80,
        "interval": 0,
        "mode": "percent",
    },
    disk={
        "threshold": 0.0,
        "path": "/",
        "mode": "percent"
    }
)
_JOUT = "Jinja test"
@_resc.register(
    trigger = "* */10 * * *",
    quiet=True,
    outputfile=_OUTPUT,
)
def jinja2_test():
    print("Jinja test", end="")

def test_jinja2(
    capfd,
    register_undos,
):
    result = jinja2_test()
    compiled_file = result.compiled_file
    print("RESC COMPILED FILE:")
    print(f"\t{compiled_file}")
    process = subprocess.Popen(
        f"command python3 {compiled_file}",
        shell=True
    )
    process.wait()

    assert os.path.isfile(_OUTPUT_FULL)
    with open(_OUTPUT_FULL, "rb") as f:
        content = f.read()
    assert len(content) > 0

    analyzes = RescLogAnalyze.analyze(content)
    assert analyzes is not None
    assert isinstance(analyzes, list)
    assert len(analyzes) == 1

    analyze = analyzes[0]
    assert analyze["stdout_content"] == (_JOUT).encode("utf-8")

@_resc.register(
    trigger = "* */10 * * *",
    quiet=True,
    outputfile=_OUTPUT,
)
def jinja2_raise():
    raise Exception("Jinja test")

def test_jinja2_raise(
    capfd,
    register_undos,
):
    result = jinja2_raise()
    compiled_file = result.compiled_file
    print("RESC COMPILED FILE:")
    print(f"\t{compiled_file}")
    process = subprocess.Popen(
        f"command python3 {compiled_file}",
        shell=True
    )
    process.wait()

    assert os.path.isfile(_OUTPUT_FULL)
    with open(_OUTPUT_FULL, "rb") as f:
        content = f.read()
    assert len(content) > 0

    analyzes = RescLogAnalyze.analyze(content)
    assert analyzes is not None
    assert isinstance(analyzes, list)
    assert len(analyzes) == 1

    analyze = analyzes[0]
    assert analyze["stderr_content"] == _JOUT.encode("utf-8")

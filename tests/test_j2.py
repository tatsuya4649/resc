import pytest
import os
from unittest import mock
from resc import *
import subprocess
from .conftest import _OUTPUT, _OUTPUT_FULL
from resc.resclog.analyze import RescLogAnalyze
from resc.object import *


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
_EXEC_FILE = os.path.join(
    os.path.dirname(__file__),
    "test_data/exec_file.py"
)
_EXEC_FILE_INDENT = os.path.join(
    os.path.dirname(__file__),
    "test_data/exec_file_indent.py"
)
_EXEC_FILE_ATTRIBUTE = os.path.join(
    os.path.dirname(__file__),
    "test_data/exec_file_attribute.txt"
)
_EXEC_FILE_SYNTAX = os.path.join(
    os.path.dirname(__file__),
    "test_data/exec_file_syntax.py"
)

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
    print(analyze["sour_content"])

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
#    with open(compiled_file, "r") as f:
#        print(f.read())
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

def test_jinja_file(
    register_undos,
):
    result = _resc.register_file(
        trigger = "* */10 * * *",
        exec_file = _EXEC_FILE,
        quiet=True,
        outputfile=_OUTPUT,
    )
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

    process = subprocess.Popen(
        f"command python3 {_EXEC_FILE}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    process.wait()
    out, err =  process.communicate()
    assert analyze["stdout_content"] == out
    print(analyze["sour_content"])

def test_jinja_file_indent_error(
    register_undos,
):
    with pytest.raises(
        RescObjectIndentationError
    ) as raiseinfo:
        result = _resc.register_file(
            trigger = "* */10 * * *",
            exec_file = _EXEC_FILE_INDENT,
            quiet=True,
            outputfile=_OUTPUT,
        )

def test_jinja_file_syntax_error(
    register_undos,
):
    with pytest.raises(
        RescObjectSyntaxError
    ) as raiseinfo:
        result = _resc.register_file(
            trigger = "* */10 * * *",
            exec_file = _EXEC_FILE_SYNTAX,
            quiet=True,
            outputfile=_OUTPUT,
        )

def test_jinja_file_attribute_error(
    register_undos,
):
    with pytest.raises(
        RescObjectAttributeError
    ) as raiseinfo:
        sys.path = []
        result = _resc.register_file(
            trigger = "* */10 * * *",
            exec_file = _EXEC_FILE_ATTRIBUTE,
            quiet=True,
            outputfile=_OUTPUT,
        )

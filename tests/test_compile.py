import pytest
from unittest import mock
import os
from resc.compile import *


def _get_source(path):
    test_file = os.path.join(
        os.path.abspath(
            os.path.dirname(
                __file__
            )
        ),
        f"test_data/{path}"
    )
    return test_file

@pytest.fixture(scope="function", autouse=False)
def get_source1():
    with open(_get_source("compile_test1.py"), "r") as f:
        yield f.read()

@pytest.fixture(scope="function", autouse=False)
def get_source2():
    with open(_get_source("compile_test2.py"), "r") as f:
        yield f.read()

@pytest.fixture(scope="function", autouse=False)
def get_source3():
    with open(_get_source("compile_test3.py"), "r") as f:
        yield f.read()

@pytest.fixture(scope="function", autouse=False)
def get_source4():
    with open(_get_source("compile_test4.py"), "r") as f:
        yield f.read()

@pytest.mark.parametrize(
    "source",[
    b"def hello",
    1,
    1.0,
    ["def hello"],
    {"source": "def hello"}
])
def test_init_type_error(source):
    with pytest.raises(
        RescCompileTypeError
    ) as raiseinfo:
        compiler = RescCompile(
            source = source
        )

def test_compile_test1(get_source1):
    result = RescCompile.compile(get_source1)
    assert result is not None
    assert isinstance(result, str)
    assert re.match(
        r"^\s",
        result
    ) is None
    print("RESC COMPILER TEST:")
    print(f"{result}")

def test_compile_test2(get_source2):
    result = RescCompile.compile(get_source2)
    assert result is not None
    assert isinstance(result, str)
    assert re.match(
        r"^\s",
        result
    ) is None
    print("RESC COMPILER TEST:")
    print(f"{result}")

def test_compile_test3(get_source3):
    result = RescCompile.compile(get_source3)
    assert result is not None
    assert isinstance(result, str)
    assert re.match(
        r"^\s",
        result
    ) is None
    print("RESC COMPILER TEST:")
    print(f"{result}")

def test_compile_indent_error(get_source4):
    with pytest.raises(
        RescCompileIndentationError
    ) as raiseinfo:
        result = RescCompile.compile(get_source4)

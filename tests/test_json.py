import pytest
from unittest import mock
import os
import json
from resc.json import *
from resc import *
from .test_j2 import _EXEC_FILE

_DUMP_FILEPATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "test_data/test.json"
)
_HASH_VALUE = "hash"
_CRONTAB_LINE = "crontab_line"
@pytest.fixture(scope="function", autouse=False)
def dump_file():
    with open(_DUMP_FILEPATH, "w") as f:
        json.dump([{
            "hash": _HASH_VALUE,
            _CRONTAB_LINE: "* * * * * echo",
        }], f)
    yield
    os.remove(_DUMP_FILEPATH)

def hello():
    ...

@pytest.fixture(scope="function",autouse=False)
def rjson(dump_file):
    resc = RescJSON(
        dump_filepath=_DUMP_FILEPATH,
    )
    yield resc

def test_init():
    resc = RescJSON(
        dump_filepath=_DUMP_FILEPATH,
    )

def test_totalline(rjson):
    ...

def test_json_search_filenotfound_error(rjson):
    with pytest.raises(
        RescJSONFileNotFoundError
    ) as raiseinfo:
        rjson.json_search(
            hash_value="100",
            key="crontab_line",
            dump_filepath="notfound.json",
        )

def test_search_json_notfound(rjson):
    result = rjson.json_search(
        hash_value="100",
        key="crontab_line",
        dump_filepath=_DUMP_FILEPATH,
    )
    assert result is None

def test_search(rjson):
    result = rjson.json_search(
        hash_value=_HASH_VALUE,
        key=_CRONTAB_LINE,
        dump_filepath=_DUMP_FILEPATH,
    )
    assert result is not None
    assert isinstance(result, str)

def test_iter__(rjson):
    result = iter(rjson)
    lists = [x for x in result]
    assert result is not None
    assert len(lists) == 1

    for part in lists:
        print(part)

def test_display_json(
    register_undos,
):
    result = register_file(
        exec_file=_EXEC_FILE,
        trigger="* * * * *",
    )
    assert isinstance(result.json_path, str)
    RescJSON.display(result.json_path)

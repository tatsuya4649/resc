import pytest
from unittest import mock
import os
import ndjson
from resc.json import *

_DUMP_FILEPATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "test_data/test.ndjson"
)
_HASH_VALUE = "hash"
_CRONTAB_LINE = "crontab_line"
@pytest.fixture(scope="function", autouse=False)
def dump_file():
    with open(_DUMP_FILEPATH, "w") as f:
        writer = ndjson.writer(f)
        writer.writerow({
            "hash": _HASH_VALUE,
            _CRONTAB_LINE: "* * * * * echo",
        })
    yield
    os.remove(_DUMP_FILEPATH)

def hello():
    ...

@pytest.fixture(scope="function",autouse=False)
def json(dump_file):
    resc = RescJSON(
        dump_filepath=_DUMP_FILEPATH,
    )
    yield resc

def test_init():
    resc = RescJSON(
        dump_filepath=_DUMP_FILEPATH,
    )

def test_totalline(json):
    ...

def test_json_search_filenotfound_error(json):
    with pytest.raises(
        RescJSONFileNotFoundError
    ) as raiseinfo:
        json.json_search(
            hash_value="100",
            key="crontab_line",
            dump_filepath="notfound.json",
        )

def test_search_json_notfound(json):
    result = json.json_search(
        hash_value="100",
        key="crontab_line",
        dump_filepath=_DUMP_FILEPATH,
    )
    assert result is None

def test_search(json):
    result = json.json_search(
        hash_value=_HASH_VALUE,
        key=_CRONTAB_LINE,
        dump_filepath=_DUMP_FILEPATH,
    )
    assert result is not None
    assert isinstance(result, str)

def test_iter__(json):
    result = iter(json)
    lists = [x for x in result]
    assert result is not None
    assert len(lists) == 1

    for part in lists:
        print(part)

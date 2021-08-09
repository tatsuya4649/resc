import pytest
from unittest import mock
import os

from resc.json import *

_DUMP_FILEPATH = "test.json"
@pytest.fixture(scope="function", autouse=False)
def dump_file():
    yield
    os.remove(_DUMP_FILEPATH)

def hello():
    ...

@pytest.fixture(scope="function",autouse=False)
def json(dump_file):
    resc = RescJSON(
        dump_filepath=_DUMP_FILEPATH,
        compiled_file="rescs31421",
        crontab_line="* * * * echo ''\n",
        register_file="register",
        function=hello,
        log_file="output"
    )
    yield resc

def test_init():
    resc = RescJSON(
        dump_filepath="test.json",
        compiled_file="rescs31421",
        crontab_line="* * * * echo ''\n",
        register_file="register",
        function=hello,
        log_file="output"
    )

def test_init_error():
    def test(a):
        return a
    with mock.patch(
        "ndjson.writer",
        side_effect=Exception
    ):
        with pytest.raises(
            RescJSONError
        ):
            RescJSON(
                dump_filepath="test.json",
                compiled_file="rescs31421",
                crontab_line="* * * * echo ''\n",
                register_file="register",
                function=test,
                log_file="output"
            )


def test_hash(json):
    result = json.hash
    assert result is not None
    assert isinstance(result, str)
    print(f"RESC JSON HASH(SHAR256): {result}")

def test_call(json):
    result = json()
    assert result is not None
    assert isinstance(result, dict)
    print(f"RESC _JDICT: {result}")

def test_totalline(json):
    ...

def test_search_json_keyerror(json):
    with pytest.raises(
        RescJSONKeyError
    ) as raiseinfo:
        result = json.json_search(
            hash_value="100",
            key="crontab_lines",
            dump_filepath=_DUMP_FILEPATH,
        )
        assert result is None
    print(f"RESCJSON SEARCH JSON KEY ERROR:{raiseinfo.value}")

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

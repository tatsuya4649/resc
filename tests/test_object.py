import pytest
import re
import sys
import os
from unittest import mock
from resc.object import *
from resc.json import RescJSON
from .test_json import _DUMP_FILEPATH, json, dump_file

@pytest.fixture(scope="function", autouse=False)
def rescob(json):
    resc = RescObject(
        jresc=json
    )
    yield resc

def test_init(json):
    resc = RescObject(
        jresc=json
    )

def test_enter(json):
    resc = RescObject(
        jresc=json
    )
    with resc:
        ...

def test_enter_import_error(json):
    with mock.patch(
        "importlib.util.module_from_spec",
        side_effect=ImportError
    ):
        resc = RescObject(
            jresc=json
        )
        with pytest.raises(
            RescObjectImportError
        ) as raiseinfo:
            with resc:
                ...

def test_call(rescob):
    with rescob:
        result = rescob.call
        assert result is not None
        assert callable(result)

def hello(a):
    return a

def test_call_result():

    _json = RescJSON(
        dump_filepath=_DUMP_FILEPATH,
        compiled_file="rescs1",
        crontab_line="* * * * echo ''\n",
        register_file="register",
        function=hello,
        log_file="output"
    )
    rescob = RescObject(
        jresc=_json
    )
    with rescob:
        result = rescob.call(1)
        assert result is not None
        assert isinstance(result, int)
        assert result == 1

def test_call_attribute(rescob):
    with pytest.raises(
        RescObjectAttributeError
    ) as raiseinfo:
        rescob.call

def test_import_close(rescob):
    rescob.import_module()
    assert rescob.hasmodule is True
    rescob.close()

def test_import_close_notmodule(rescob):
    assert rescob.hasmodule is False
    rescob.import_module()
    rescob.close()
    assert rescob.hasmodule is False

def test_close_tempfp_attribute(rescob):
    with pytest.raises(
        RescObjectAttributeError
    ) as raiseinfo:
        rescob.close()

def test_import_close_attribute2(rescob):
    rescob.import_module()
    del rescob._call
    with pytest.raises(
        RescObjectAttributeError
    ) as raiseinfo:
        rescob.close()

def test_import_module_error(rescob):
    with mock.patch(
        "importlib.util.module_from_spec",
        side_effect=ImportError
    ):
        with pytest.raises(
            RescObjectImportError
        ) as raiseinfo:
            rescob.import_module()

def test_delete_module_error():
    with pytest.raises(
        RescObjectAttributeError
    ) as raiseinfo:
        RescObject._delete_module("1414124")

def test_syspath_append_error(rescob):
    with pytest.raises(
        RescObjectAttributeError
    ) as raiseinfo:
        rescob._syspath_append()

def test_syspath_remove_error(rescob):
    rescob.import_module()
    filepath = RescObject._hashmodule[rescob._hash]\
        ["module_path"]
    del RescObject._hashmodule[rescob._hash]
    with pytest.raises(
        RescObjectKeyError
    ) as raiseinfo:
        rescob._syspath_remove()
    if not os.path.isfile(filepath):
        sys.exit(1)
    os.remove(filepath)

def test_syspath_remove_error2(rescob):
    rescob.import_module()
    del RescObject._hashmodule[rescob._hash]["syspath"]
    with pytest.raises(
        RescObjectKeyError
    ) as raiseinfo:
        rescob._syspath_remove()
    rescob._delete_module(rescob._hash)

def test_create_module(rescob):
    result = rescob.create_module()
    assert result is not None
    assert isinstance(result, str)
    assert re.match(
        r"/tmp/",
        result
    ) is not None

    rescob._delete_module(rescob._hash)

def test_json(rescob):
    result = rescob.json
    assert result is not None
    assert isinstance(result, RescJSON)

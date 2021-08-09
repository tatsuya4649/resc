import pytest
import re
import sys
import os
from unittest import mock
from resc import *
from resc.object import *
from resc.json import RescJSON
from resc.cron import *
from .test_json import _DUMP_FILEPATH, json, dump_file
from .test_resc_register import setup_resc, temp_rescdir

@pytest.fixture(scope="function", autouse=False)
def rescob(dump_file):
    resc = RescObject(
        dump_filepath=_DUMP_FILEPATH,
        compiled_file="rescs31421",
        crontab_line="* * * * echo ''\n",
        register_file="register",
        function=hello,
        log_file="output"
    )
    yield resc

def test_init(json):
    resc = RescObject(
        dump_filepath=_DUMP_FILEPATH,
        compiled_file="rescs31421",
        crontab_line="* * * * echo ''\n",
        register_file="register",
        function=hello,
        log_file="output"
    )

def test_enter(json):
    resc = RescObject(
        dump_filepath=_DUMP_FILEPATH,
        compiled_file="rescs1", crontab_line="* * * * echo ''\n",
        register_file="register",
        function=hello,
        log_file="output"
    )
    with resc:
        ...

def test_enter_import_error(rescob):
    rescob.close()
    with mock.patch(
        "importlib.util.spec_from_file_location",
        side_effect=ImportError
    ):
        with pytest.raises(
            RescObjectImportError
        ) as raiseinfo:
            with rescob:
                ...

def test_call(rescob):
    with rescob:
        result = rescob.call
        assert result is not None
        assert callable(result)

def hello(a):
    return a

def test_call_result():

    rescob = RescObject(
        dump_filepath=_DUMP_FILEPATH,
        compiled_file="rescs1",
        crontab_line="* * * * echo ''\n",
        register_file="register",
        function=hello,
        log_file="output"
    )
    with rescob:
        result = rescob.call(1)
        assert result is not None
        assert isinstance(result, int)
        assert result == 1

def test_call_attribute(rescob):
    rescob.call

def test_import_close(rescob):
    rescob.import_module()
    assert rescob.hasmodule is True
    rescob.close()

def test_import_close_notmodule(rescob):
    assert rescob.hasmodule is True
    rescob.import_module()
    rescob.close()
    assert rescob.hasmodule is False

def test_import_close_attribute2(rescob):
    rescob.import_module()
    del rescob._call
    with pytest.raises(
        RescObjectAttributeError
    ) as raiseinfo:
        rescob.close()

def test_import_module_error():
    with mock.patch(
        "importlib.util.spec_from_file_location",
        side_effect=ImportError
    ):
        with pytest.raises(
            RescObjectImportError
        ) as raiseinfo:
            rescob = RescObject(
                dump_filepath=_DUMP_FILEPATH,
                compiled_file="rescs1",
                crontab_line="* * * * echo ''\n",
                register_file="register",
                function=hello,
                log_file="output"
            )

def test_delete_module_error():
    with pytest.raises(
        RescObjectAttributeError
    ) as raiseinfo:
        RescObject._delete_module("1414124")

def test_syspath_append(rescob):
    rescob._syspath_append()
    rescob._syspath_remove()

def test_syspath_remove_error(rescob):
    rescob.import_module()
    filepath = RescObject._hashmodule[rescob.hash]\
        ["module_path"]
    del RescObject._hashmodule[rescob.hash]
    with pytest.raises(
        RescObjectKeyError
    ) as raiseinfo:
        rescob._syspath_remove()
    if not os.path.isfile(filepath):
        sys.exit(1)
    os.remove(filepath)

def test_syspath_remove_error2(rescob):
    rescob.import_module()
    del RescObject._hashmodule[rescob.hash]["syspath"]
    with pytest.raises(
        RescObjectKeyError
    ) as raiseinfo:
        rescob._syspath_remove()
    rescob._delete_module(rescob.hash)

def test_create_module(rescob):
    result = rescob.create_module()
    assert result is not None
    assert isinstance(result, str)
    assert re.match(
        r"/tmp/",
        result
    ) is not None
    rescob._delete_module(rescob.hash)

def test_json(rescob):
    result = rescob.json
    assert result is not None
    assert isinstance(result, dict)

def test_delete(rescob, cron_noempty):
    assert rescob.length == 1
    assert len(Cron.cronlist()) == 1
    rescob.crontab_line = cron_noempty
    result = rescob.delete()

    assert Cron.cronlist() is None
    assert result is not None
    assert isinstance(result, str)

    assert rescob.length == 0

def test_register_obj(
    setup_resc,
    register_undos,
    temp_rescdir,
):
    @setup_resc.register(
        trigger="* * * * *",
    )
    def hello():
        ...

    result = hello()
    assert result is not None
    assert isinstance(result, RescObject)

import pytest
from resc.resclog.dump import *


@pytest.fixture(scope="module",autouse=True)
def dumper():
    dump = RescDump(b"")
    yield dump

@pytest.mark.parametrize(
    "content",[
    (True),
    (1),
    ("Hello World"),
    ([1]),
    ({"1":1}),
])
def test_init_type_failure(content):
    with pytest.raises(
        RescDumpTypeError
    ) as raiseinfo:
        dump = RescDump(
            content = content
        )

def test_init_type():
    dump = RescDump(
        content = b"Hello World"
    )

@pytest.mark.parametrize(
    "content",[
    (True),
    (1),
    ("Hello World"),
    ([1]),
    ({"1":1}),
])
def test_bindump_type_failure(content,dumper):
    with pytest.raises(
        RescDumpTypeError
    ) as raiseinfo:
        dumper.bindump(content)

@pytest.mark.parametrize(
    "content",[
    (True),
    (1),
    ("Hello World"),
    ([1]),
    ({"1":1}),
])
def test_bindump_classmethod_type_failure(content):
    with pytest.raises(
        RescDumpTypeError
    ) as raiseinfo:
        RescDump.bindump(content)

def test_bindump(dumper):
    res = dumper.bindump(b"Hello World")
    assert res is not None
    assert isinstance(res,str)
    print(f"RESC DUMP BINARY: {res}")

def test_bindump_classmethod():
    res = RescDump.bindump(b"Hello World")
    assert res is not None
    assert isinstance(res,str)
    print(f"RESC DUMP BINARY CLASSMETHOD: {res}")

def test_bindump_nogap(dumper):
    res = dumper.bindump(
        content=b"Hello World",
        empty=False,
    )
    assert res is not None
    assert isinstance(res,str)
    print(f"RESC DUMP BINARY NO GAP: {res}")

def test_bindump_ascii(dumper):
    res = dumper.bindump(
        content=b"Hello World",
        ascii=True,
    )
    assert res is not None
    assert isinstance(res,str)
    print(f"RESC DUMP BINARY ASCII: {res}")

def test_hexdump(dumper):
    res = dumper.hexdump(
        content=b"Hello World",
    )
    assert res is not None
    assert isinstance(res,str)
    print(f"RESC DUMP BINARY HEX: {res}")

def test_hexdump_classmethod():
    res = RescDump.hexdump(
        content=b"Hello World",
    )
    assert res is not None
    assert isinstance(res,str)
    print(f"RESC DUMP BINARY HEX CLASSMETHOD: {res}")

import pytest
from unittest import mock
from resc.file import *


@pytest.fixture(scope="function", autouse=False)
def file_init():
    fd = FileDetect(
        threshold=100,
        mode="number"
    )
    yield fd

@pytest.mark.parametrize(
    "threshold",[
    "80",
    b"80",
    [80],
    {"threshold": 80},
])
def test_init_threshold_type_error(threshold):
    with pytest.raises(
        FileDetectTypeError
    ):
        FileDetect(
            threshold=threshold
        )

@pytest.mark.parametrize(
    "mode",[
    80.0,
    80,
    b"percent",
    ["moe"],
    {"mode": "percent"},
    True,
])
def test_init_mode_type_error(mode):
    with pytest.raises(
        FileDetectTypeError
    ):
        FileDetect(
            threshold=80.0,
            mode=mode
        )

def test_init_mode_value_error():
    with pytest.raises(
        FileDetectValueError
    ):
        FileDetect(
            threshold=80.0,
            mode="a"
        )

def test_check(file_init):
    with mock.patch(
        "resc.file.FileDetect.number",
        new_callable=mock.PropertyMock
    ) as mock_number:
        mock_number.return_value = 0
        result = file_init.check
    assert result is True

    with open("/proc/sys/fs/file-max", "r") as f:
        maxfd = f.read()
    with mock.patch(
        "resc.file.FileDetect.number",
        new_callable=mock.PropertyMock
    ) as mock_number:
        mock_number.return_value = int(maxfd)
        result = file_init.check
    assert result is False

def test_resource(file_init):
    result = file_init.resource
    assert result is not None
    assert isinstance(result, str)

import pytest
from unittest import mock
from resc.disk import *

_DISK_THRESHOLD=80
_DISK_PATH="/"

def test_disk():
	disk = DiskDetect(
		_DISK_PATH,
		_DISK_THRESHOLD,
		mode="percent",
	)
	res = disk.percent("/")
	assert res is not None
	assert isinstance(res,float)
	assert res >= 0.0
	print(f'DIST PERCENT {res}% ({type(res)})')

	res = disk.free("/")
	assert res is not None
	assert isinstance(res,int)
	assert res >= 0
	print(f'DIST FREE {res} bytes [ {round(res/(1024*1024),1)}MB , {round(res/(1024*1024*1024),1)}GB ] ({type(res)})')

	res = disk.check
	assert res is not None
	assert isinstance(res,bool)
	print(f'DISK CHECK {res} ({type(res)})')

@pytest.mark.parametrize(
    "path",[
    1.0,
    1,
    b"path",
    ["/hello"],
    {"path": "world"}
])
def test_disk_init_path_type_error(path):
    with pytest.raises(
        DiskTypeError
    ) as raiseinfo:
        disk = DiskDetect(
            path=path,
            threshold=80.0,
            mode="percent",
        )

@pytest.mark.parametrize(
    "threshold",[
    "1.0",
    b"threshold",
    [90],
    {"threshold": 90}
])
def test_disk_init_threshold_type_error(threshold):
    with pytest.raises(
        DiskTypeError
    ) as raiseinfo:
        disk = DiskDetect(
            path=_DISK_PATH,
            threshold=threshold,
            mode="percent",
        )

@pytest.mark.parametrize(
    "mode",[
    1.0,
    b"percent",
    ["percent"],
    {"mode": "percent"}
])
def test_disk_init_mode_type_error(mode):
    with pytest.raises(
        DiskTypeError
    ) as raiseinfo:
        disk = DiskDetect(
            path=_DISK_PATH,
            threshold=_DISK_THRESHOLD,
            mode=mode,
        )

def test_disk_check_none():
    with mock.patch(
        "resc.disk.DiskDetect.percent",
        return_value = None
    ):
        with pytest.raises(
            DiskValueError
        ) as raiseinfo:
            disk = DiskDetect(
                _DISK_PATH,
                _DISK_THRESHOLD,
                mode="percent",
            )
            disk.check

def test_disk_check_false():
    with mock.patch(
        "resc.disk.DiskDetect.percent",
        return_value = 90.0
    ):
        disk = DiskDetect(
            _DISK_PATH,
            _DISK_THRESHOLD,
            mode="percent",
        )
        assert disk.check is False

def test_disk_check_true():
    with mock.patch(
        "resc.disk.DiskDetect.percent",
        return_value = 70.0
    ):
        disk = DiskDetect(
            _DISK_PATH,
            _DISK_THRESHOLD,
            mode="percent",
        )
        assert disk.check is True

@pytest.mark.parametrize(
    "path",[
    1.0,
    1,
    b"path",
    ["/path"],
    {"path": "/path"},
])
def test_usage_type_error(path):
    with pytest.raises(
        DiskTypeError
    ) as raiseinfo:
        DiskDetect._usage(path)

def test_usage_found_error():
    with pytest.raises(
        FileNotFoundError
    ) as raiseinfo:
        DiskDetect._usage("hello/world")

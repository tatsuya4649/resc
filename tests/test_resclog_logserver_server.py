import pytest
import os
import uvicorn
from unittest import mock
from resc.resclog.logserver import server
from resc.resclog.logserver.env import *


def test_host_environ():
    _HOSTNAME = "localhost"
    os.environ[SERVERENV.HOST_ENV] = _HOSTNAME
    result = server._host()
    assert result is not None
    assert isinstance(result, str)
    assert result == _HOSTNAME

def test_host_no_environ():
    os.environ.pop(SERVERENV.HOST_ENV, None)
    result = server._host()
    assert result is not None
    assert isinstance(result, str)
    assert result == SERVERENV.HOST_DEFAULT

def test_default_port():
    result = server._default_port()
    assert result is not None
    assert isinstance(result, int)
    assert result == SERVERENV.PORT_DEFAULT

def test_port():
    _PORT = 20021
    os.environ[SERVERENV.PORT_ENV] = f"{_PORT}"
    result = server._port()
    assert result is not None
    assert isinstance(result, int)
    assert result == _PORT

def test_port_type_error():
    os.environ[SERVERENV.PORT_ENV] = "hello"
    result = server._port()
    assert result is not None
    assert isinstance(result, int)
    assert result == server._default_port()

def test_port_no_environ():
    os.environ.pop(SERVERENV.PORT_ENV, None)
    result = server._port()
    assert result is not None
    assert isinstance(result, int)
    assert result == server._default_port()

def test_start_server():
    def mockserver(
        app,
        host,
        port,
        reload
    ):
        ...

    with mock.patch(
        "uvicorn.run",
        side_effect = mockserver
    ):
        server.start_server()

import os
import pytest
from unittest import mock
from resc.ssh import *
from resc.resclog.resclog import RescLog
from .conftest import _KEY_PATH
import paramiko
import scp

@pytest.fixture(scope="function",autouse=False)
def ssh():
    ssh = SSH(
        ip="localhost",
        port=20022,
        username="root",
        key_filename=_KEY_PATH,
    )
    yield ssh
@pytest.fixture(scope="function",autouse=False)
def ssh2():
    ssh = SSH(
        ip="localhost",
        port=20022,
        username="root",
        password="test_resc",
    )
    yield ssh

def test_init():
    ssh = SSH(
        ip="127.0.0.1",
        username="root",
        key_filename="key",
    )

@pytest.mark.parametrize(
    "ip",[
    100,
    100.0,
    b"127.0.0.1",
    ["127.0.0.1"],
    {"ip": "127.0.0.1"}
])
def test_init_ip_type_error(ip):
    with pytest.raises(
        SSHTypeError
    ) as raiseinfo:
        ssh = SSH(
            ip=ip,
            username="root",
            key_filename="key",
        )

@pytest.mark.parametrize(
    "username",[
    100,
    100.0,
    b"username",
    ["username"],
    {"ip": "username"}
])
def test_init_username_type_error(username):
    with pytest.raises(
        SSHTypeError
    ) as raiseinfo:
        ssh = SSH(
            ip="localhost",
            username=username,
            key_filename="key",
        )

@pytest.mark.parametrize(
    "password",[
    100,
    100.0,
    b"password",
    ["password"],
    {"ip": "password"}
])
def test_init_password_type_error(password):
    with pytest.raises(
        SSHTypeError
    ) as raiseinfo:
        ssh = SSH(
            ip="localhost",
            username="username",
            password=password
        )

@pytest.mark.parametrize(
    "key_filename",[
    100,
    100.0,
    b"password",
    ["password"],
    {"ip": "password"}
])
def test_init_key_filename_type_error(
    key_filename
):
    with pytest.raises(
        SSHTypeError
    ) as raiseinfo:
        ssh = SSH(
            ip="localhost",
            username="username",
            key_filename=key_filename
        )

@pytest.mark.parametrize(
    "port",[
    "100",
    100.0,
    b"100",
    [100],
    {"port": 200}
])
def test_init_port_type_error(
    port
):
    with pytest.raises(
        SSHTypeError
    ) as raiseinfo:
        ssh = SSH(
            ip="localhost",
            username="username",
            key_filename="key_filename",
            port=port
        )

@pytest.mark.parametrize(
    "timeout",[
    "100",
    100.0,
    b"100",
    [100],
    {"port": 200}
])
def test_init_timeout_type_error(
    timeout
):
    with pytest.raises(
        SSHTypeError
    ) as raiseinfo:
        ssh = SSH(
            ip="localhost",
            username="username",
            key_filename="key_filename",
            timeout=timeout
        )

def test_init_pass_key_error():
    with pytest.raises(
        SSHValueError
    ) as raiseinfo:
        ssh = SSH(
            ip="localhost",
            username="username",
            key_filename="key_filename",
            password="password"
        )

def test_ip(ssh):
    result = ssh.ip
    assert result is not None
    assert isinstance(result, str)

def test_port(ssh):
    result = ssh.port
    assert result is not None
    assert isinstance(result, int)

def test_username(ssh):
    result = ssh.username
    assert result is not None
    assert isinstance(result, str)

def test_password(ssh2):
    result = ssh2.password
    assert result is not None
    assert isinstance(result, str)

def test_key_filename(ssh):
    result = ssh.key_filename
    assert result is not None
    assert isinstance(result, str)

def test_timeout(ssh):
    result = ssh.timeout
    assert result is not None
    assert isinstance(result, int)

def test_ssh_pin_err(ssh):
    with mock.patch(
        "paramiko.Channel.recv_exit_status"
    ) as stdout:
        stdout.return_value = 1
        with pytest.raises(
            RescSSHError
        ) as raiseinfo:
            ssh.ssh_ping()

@pytest.mark.parametrize(
    "err",[
    paramiko.ssh_exception.NoValidConnectionsError,
    paramiko.ssh_exception.SSHException,
    BlockingIOError,
    FileNotFoundError,
    Exception
])
def test_connect_error(ssh,err):
    _FILE="output"
    _DEFAULT_PATH=f"~/.resc/{_FILE}"
    _RESCLOG=RescLog()
    if err is paramiko.ssh_exception. \
        NoValidConnectionsError:
        _ERRCONTENT = "World"
        _ERR = {
            ("127.0.0.1",22): _ERRCONTENT
        }
    else:
        _ERR = "Hello"
    with mock.patch(
        "paramiko.SSHClient.connect",
        side_effect=err(_ERR)
    ) as client:
        result = ssh.connect(
            resclog=_RESCLOG
        )
    assert result is None

    if err is not paramiko.ssh_exception. \
        NoValidConnectionsError:
        assert _RESCLOG.stderr == \
            _ERR.encode("utf-8")

def test__connect_novalidconnection_error(ssh):
    _RESCLOG=RescLog()
    with mock.patch(
        "paramiko.SSHClient.connect",
        side_effect=paramiko.ssh_exception. \
    NoValidConnectionsError({
        ("127.0.0.1",20022) : (
            "error",
            "hello"
        )
    })
    ) as client:
        with pytest.raises(
            RescSSHConnectionError
        ) as raiseinfo:
            result = ssh._connect()

def test__connect_sshexception_error(ssh):
    _RESCLOG=RescLog()
    with mock.patch(
        "paramiko.SSHClient.connect",
        side_effect=paramiko.ssh_exception. \
    SSHException
    ) as client:
        with pytest.raises(
            RescSSHError
        ) as raiseinfo:
            result = ssh._connect()
def test__connect_blocking_error(ssh):
    _RESCLOG=RescLog()
    with mock.patch(
        "paramiko.SSHClient.connect",
        side_effect=BlockingIOError
    ) as client:
        with pytest.raises(
            RescSSHTimeoutError
        ) as raiseinfo:
            result = ssh._connect()
def test__connect_filenotfound_error(ssh):
    _RESCLOG=RescLog()
    with mock.patch(
        "paramiko.SSHClient.connect",
        side_effect=FileNotFoundError
    ) as client:
        with pytest.raises(
            RescSSHFileNotFoundError
        ) as raiseinfo:
            result = ssh._connect()
def test__connect_exception_error(ssh):
    _RESCLOG=RescLog()
    with mock.patch(
        "paramiko.SSHClient.connect",
        side_effect=Exception
    ) as client:
        with pytest.raises(
            RescSSHError
        ) as raiseinfo:
            result = ssh._connect()



def test_scpfile_status_error(ssh):
    _FILE="output"
    _DEFAULT_PATH=f"~/.resc/{_FILE}"
    _RESCLOG=RescLog(
    )
    with mock.patch(
        "paramiko.Channel.recv_exit_status"
    ) as stdout:
        stdout.return_value = 1
        with pytest.raises(
            SSHError
        ) as raiseinfo:
            ssh.scpfile(
                connect=ssh._connect(),
                script_path=_FILE,
                resclog=_RESCLOG,
            )

@pytest.mark.parametrize(
    "err",[
    scp.SCPException,
    FileNotFoundError,
    Exception
])
def test_scpfile_scp_error(ssh,err):
    _FILE="output"
    _DEFAULT_PATH=f"~/.resc/{_FILE}"
    _RESCLOG=RescLog()
    _ERR_CONTENT = "hello"
    with mock.patch(
        "scp.SCPClient.put",
        side_effect=err(_ERR_CONTENT)
    ) as client:
        result = ssh.scpfile(
            connect=ssh._connect(),
            script_path=_FILE,
            resclog=_RESCLOG,
        )
    assert result is False
    assert isinstance(_RESCLOG.stderr,bytes)
    assert _RESCLOG.stderr == _ERR_CONTENT.encode("utf-8")

def test_scpfile_scp_out_err(ssh):
    _PATH="scpfile/test/output"
    _DEFAULT_PATH=f"{os.path.expanduser('~')}/.resc"

    paths = list()
    for path in os.path.dirname(
        _PATH
    ).split('/'):
        paths.append(path)
        path = "/".join(paths)
        fullpath = os.path.join(
            _DEFAULT_PATH,
            path
        )
        if not os.path.isdir(fullpath):
            os.mkdir(fullpath)

    with open(os.path.join(
        _DEFAULT_PATH,
        _PATH
    ), "w") as f:
        f.write("Hello World")

    _RESCLOG=RescLog()
    _ERR_CONTENT = "hello"

    def my__iter__():
        return iter(["OUTPUT","HELLO"])

    with mock.patch(
        "paramiko.Channel.recv_exit_status",
        return_value=0
    ):
        with mock.patch(
            "paramiko.BufferedFile.__iter__",
            side_effect=my__iter__
        ):
            result = ssh.scpfile(
                connect=ssh._connect(),
                script_path=os.path.join(
                    _DEFAULT_PATH,
                    _PATH
                ),
                resclog=_RESCLOG,
            )
    expected = "".join(list(my__iter__()))
    assert _RESCLOG.stdout == expected.encode("utf-8")
    assert _RESCLOG.stderr == expected.encode("utf-8")

    os.remove(
        os.path.join(
            _DEFAULT_PATH,
            _PATH
        )
    )
    for _ in range(len(paths)):
        path = "/".join(paths)
        print(path)
        fullpath = os.path.join(
            _DEFAULT_PATH,
            path
        )
        if os.path.isdir(fullpath):
            os.rmdir(fullpath)

        paths.pop(-1)

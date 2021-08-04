import paramiko
import scp
import os

from .rescerr import RescSSHConnectionError, RescSSHFileNotFoundError, \
    RescSSHError, RescSSHTimeoutError


class SSHError(Exception):
    pass


class SSH:
    _FORDEST = "/var/resc/"

    def __init__(
        self,
        ip,
        username,
        password=None,
        key_filename=None,
        timeout=5,
        port=22,
    ):
        self._ip = ip
        self._port = port
        self._username = username
        self._password = password
        self._key_filename = key_filename
        self._timeout = timeout
        self._startup_scripts = None

    @property
    def ip(self):
        return self._ip

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def key_filename(self):
        return self._key_filename

    @property
    def timeout(self):
        return self._timeout

    def ssh_ping(self):
        client = self._connect()
        _, stdout, stderr = client.exec_command(
            "true"
        )
        if int(stdout.channel.recv_exit_status()) != 0:
            raise RescSSHError("Remote Host \"true\" command failure.")

    def _connect(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        )
        try:
            client.connect(
                hostname=self._ip,
                port=self._port,
                username=self._username,
                password=self._password,
                key_filename=self._key_filename,
                timeout=self._timeout,
            )
            return client
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            raise RescSSHConnectionError(e)
        except paramiko.ssh_exception.SSHException as e:
            raise RescSSHError(e)
        except BlockingIOError as e:
            raise RescSSHTimeoutError(e)
        except FileNotFoundError as e:
            raise RescSSHFileNotFoundError(e)
        except Exception as e:
            raise RescSSHError(e)

    def connect(self, resclog):
        try:
            client = self._connect()
            return client
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            resclog.stderr = str(e).encode("utf-8")
        except paramiko.ssh_exception.SSHException as e:
            resclog.stderr = str(e).encode("utf-8")
        except BlockingIOError as e:
            resclog.stderr = str(e).encode("utf-8")
        except FileNotFoundError as e:
            resclog.stderr = str(e).encode("utf-8")
        except Exception as e:
            resclog.stderr = str(e).encode("utf-8")
        return None

    def close(self, client):
        client.close()

    def scpfile(self, connect, script_path, resclog):
        # Remote Host Path
        self._startup_scripts = f"~/.resc/{os.path.basename(script_path)}"
        _, stdout, stderr = connect.exec_command(
            "cd ~;mkdir -p .resc"
        )
        for line in stdout:
            resclog.stdout = line
        for line in stderr:
            resclog.stderr = line
        if int(stdout.channel.recv_exit_status()) != 0:
            raise SSHError(
                f"""server exit status \
                {stdout.channel.recv_exit_status()}"""
            )
        try:
            with scp.SCPClient(
                connect.get_transport()
            ) as s:
                s.put(
                    files=script_path,
                    remote_path=self._startup_scripts,
                    recursive=True
                )
            return True
        except scp.SCPException as e:
            resclog.stderr = str(e).encode("utf-8")
        except FileNotFoundError as e:
            resclog.stderr = str(e).encode("utf-8")
        except Exception as e:
            resclog.stderr = str(e).encode("utf-8")
        return False

    @property
    def startup_scripts(self):
        return self._startup_scripts

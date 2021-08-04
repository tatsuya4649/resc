import subprocess
import sys
import os

class RemoteHostError(Exception):
    pass


class RemoteHostStartupFailure(Exception):
    pass


class RemoteHostShutdownFailure(Exception):
    pass


class RemoteHost:
    _DOCKER_SETUP_SCRIPT = \
        os.path.join(
            os.path.dirname(
                os.path.abspath(
                    __file__
                )
            ),
            "docker_remote_setup.sh"
        )
    _DOCKER_SHUTDOWN_SCRIPT = \
        os.path.join(
            os.path.dirname(
                os.path.abspath(
                    __file__
                )
            ),
            "docker_remote_shutdown.sh"
        )
    _DEFAULT_TIMEOUT_TIME = 60
    _DEFAULT_COMM_TIMEOUT = 5
    def __init__(self):
        ...

    def startup(self,stdout=False,stderr=False):
        process = subprocess.Popen(
            f"bash {self._DOCKER_SETUP_SCRIPT}",
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            universal_newlines = True,
            shell=True,
        )
        try:
            result = process.wait(
                timeout = self._DEFAULT_TIMEOUT_TIME
            )
            _stdout,_stderr = process.communicate(
                timeout = self._DEFAULT_COMM_TIMEOUT
            )
        except subprocess.TimeoutExpired as e:
            print(e)
            sys.exit(1)
        except Exception as e:
            print(e)
            sys.exit(1)
        if stdout:
            sys.stderr.write(_stdout)
        if stderr:
            sys.stderr.write(_stderr)
        if result:
            raise RemoteHostStartupFailure(
                "failure to startup docker remote host."
            )

    def shutdown(self,stdout=False,stderr=False):
        process = subprocess.Popen(
            f"bash {self._DOCKER_SHUTDOWN_SCRIPT}",
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            universal_newlines = True,
            shell=True,
        )
        try:
            result = process.wait(
                timeout = self._DEFAULT_TIMEOUT_TIME
            )
            _stdout,_stderr = process.communicate(
                timeout = self._DEFAULT_COMM_TIMEOUT
            )
        except subprocess.TimeoutExpired as e:
            print(e)
            sys.exit(1)
        except Exception as e:
            print(e)
            sys.exit(1)
        if stdout:
            sys.stderr.write(_stdout)
        if stderr:
            sys.stderr.write(_stderr)
        if result:
            raise RemoteHostShutdownFailure(
                "failure to shutdown docker remote host."
            )


if __name__ == "__main__":
    remote = RemoteHost()
    remote.startup(stdout=True,stderr=True)
    remote.shutdown(stdout=True,stderr=True)

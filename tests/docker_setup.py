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
    _DEFAULT_TIMEOUT_TIME = 180
    def __init__(self):
        ...

    def startup(self,stdout=False,stderr=False):
        process = subprocess.Popen(
            f"bash {self._DOCKER_SETUP_SCRIPT}",
            universal_newlines = True,
            shell=True,
        )
        try:
            result = process.wait(
                timeout = self._DEFAULT_TIMEOUT_TIME
            )
        except subprocess.TimeoutExpired as e:
            print(e)
            sys.exit(1)
        except Exception as e:
            print(e)
            sys.exit(1)
        if result:
            raise RemoteHostStartupFailure(
                "failure to startup docker remote host."
            )
        return

    def shutdown(self,stdout=False,stderr=False):
        process = subprocess.Popen(
            f"bash {self._DOCKER_SHUTDOWN_SCRIPT}",
            universal_newlines = True,
            shell=True,
        )
        try:
            result = process.wait(
                timeout = self._DEFAULT_TIMEOUT_TIME
            )
        except subprocess.TimeoutExpired as e:
            print(e)
            sys.exit(1)
        except Exception as e:
            print(e)
            sys.exit(1)
        if result:
            raise RemoteHostShutdownFailure(
                "failure to shutdown docker remote host."
            )


if __name__ == "__main__":
    remote = RemoteHost()
    remote.startup(stdout=True,stderr=True)
    remote.shutdown(stdout=True,stderr=True)

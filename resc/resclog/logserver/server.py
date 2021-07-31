import os
import uvicorn
from .env import SERVERENV


def _host():
    if os.getenv(SERVERENV.HOST_ENV) is not None:
        return os.getenv(SERVERENV.HOST_ENV)
    else:
        return SERVERENV.HOST_DEFAULT


def _default_port():
    return SERVERENV.PORT_DEFAULT


def _port():
    if os.getenv(SERVERENV.PORT_ENV) is not None:
        try:
            return int(os.getenv(SERVERENV.PORT_ENV))
        except ValueError:
            return _default_port()
    else:
        return _default_port()


def start_server():
    uvicorn.run(
        "resc.resclog.logserver.log:app",
        host=_host(),
        port=_port(),
        reload=True,
    )

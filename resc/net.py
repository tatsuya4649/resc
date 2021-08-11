import psutil
from .detect import DetectBase
from enum import Enum


class NetKind(Enum):
    INET = "inet"
    INET4 = "inet4"
    INET6 = "inet6"
    TCP = "tcp"
    TCP4 = "tcp4"
    TCP6 = "tcp6"
    UDP4 = "udp4"
    UDP6 = "udp6"
    UNIX = "unix"
    ALL = "all"


class NetDetectTypeError(TypeError):
    pass


class NetDetectAttributeError(AttributeError):
    pass


class NetDetectValueError(ValueError):
    pass


class NetDetect(DetectBase):
    """
    """

    def __init__(
        self,
        threshold,
        kind=NetKind.ALL.value,
    ):
        self.threshold = threshold
        self.kind = kind

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        if not isinstance(value, int):
            raise NetDetectTypeError(
                "threshold must be int."
            )
        self._threshold = value

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, value):
        if not isinstance(value, str):
            raise NetDetectTypeError(
                "kind must be str."
            )
        if value not in [ x.value for x in NetKind ]:
            raise NetDetectValueError(
                f"invalid value {value}.(valid:{[ x.value for x in NetKind]})"
            )
        self._kind = value

    @property
    def check(self):
        """
        Check over Network connections.
        over threshold: return False
        within threshold: return True
        """
        conns = psutil.net_connections(kind=self.kind)
        if len(conns) < self.threshold:
            return True
        else:
            return False

    @property
    def resource(self):
        return "net"

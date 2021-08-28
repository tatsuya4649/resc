import psutil
import re
from .logical import Logic
from .detect import DetectBase
from enum import Enum


class FileDetectTypeError(TypeError):
    pass


class FileDetectValueError(ValueError):
    pass


class FileDetectMode(Enum):
    PERCENT = {"name": "percent", "logic": Logic.GT}
    NUMBER = {"name": "number", "logic": Logic.GT}


class FileDetect(DetectBase):
    def __init__(
        self,
        threshold,
        mode=FileDetectMode.PERCENT.value["name"],
    ):
        self.threshold = threshold
        self.mode = mode

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        if not isinstance(value, (int, float)):
            raise FileDetectTypeError(
                "threshold must be int or float type."
            )
        self._threshold = value

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if not isinstance(value, str):
            raise FileDetectTypeError(
                "mode must be str type."
            )
        if value not in [ x.value["name"] for x in FileDetectMode]:
            raise FileDetectValueError(
                f"invalid mode value.(valid: {[ x.value['name'] for x in FileDetectMode]})"
            )
        self._mode = [
            x for x in FileDetectMode
            if re.match(
                rf'^{x.value["name"]}$',
                f'{value}',
                flags=re.IGNORECASE
            )][0]

    @property
    def maxfd(self):
        with open("/proc/sys/fs/file-max", "r") as f:
            maxfd = f.read()
        return int(maxfd)

    @property
    def number(self):
        pids = psutil.pids()
        total = 0
        for pid in pids:
            process = psutil.Process(pid)
            try:
                total += process.num_fds()
            except psutil.AccessDenied as e:
                pass
            except psutil.NoSuchProcess as e:
                pass
        return total

    @property
    def percent(self):
        return 100*(float(self.number)/float(self.maxfd))

    @property
    def check(self):
        """
        Check over File threshold.
        over threshold: return False
        within threshold: return True
        """
        if self._mode is FileDetectMode.PERCENT:
            res = eval(f"self.{self.mode.value['name']}")
        else:
            res = eval(f"self.{self.mode.value['name']}")

        if eval(
            f"{res} {self.mode.value['logic'].value} {self.threshold}"
        ):
            return False
        else:
            return True

    @property
    def resource(self):
        return "file"

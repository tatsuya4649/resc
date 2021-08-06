import psutil
import os
import re
from enum import Enum
from .logical import Logic
from .detect import DetectBase


class DiskDetectMode(Enum):
    PERCENT = {"name": "percent", "logic": Logic.GT}
    USAGE = {"name": "usage", "logic": Logic.GT}
    FREE = {"name": "free", "logic": Logic.LT}


class DiskTypeError(TypeError):
    pass


class DiskValueError(ValueError):
    pass


class DiskDetect(DetectBase):
    def __init__(
        self,
        path,
        threshold,
        mode=DiskDetectMode.PERCENT.value["name"],
    ):
        if not isinstance(path, str):
            raise DiskTypeError("path must be string type.")
        self._path = path
        if not isinstance(threshold, int) and not isinstance(threshold, float):
            raise DiskTypeError("threshold must be float or int type.")
        self._threshold = threshold

        if not isinstance(mode, str):
            raise DiskTypeError("mode must be string type.")
        if len([x for x in DiskDetectMode
                if re.match(
                    rf'{x.value["name"]}',
                    f'{mode}',
                    flags=re.IGNORECASE
                ) is not None]) == 0:
            raise DiskValueError(
                f"""{mode} is invalid value.-\
                valid value {[x.value['name'] for x in DiskDetectMode]}"""
            )
        self._mode = [
            x for x in DiskDetectMode
            if re.match(
                rf'{x.value["name"]}',
                f'{mode}',
                flags=re.IGNORECASE
            ) is not None][0]

    @property
    def path(self):
        return self._path

    @property
    def resource(self):
        return "disk"

    @property
    def threshold(self):
        return self._threshold

    @property
    def mode(self):
        return self._mode

    @property
    def check(self):
        """
        Check over Disk threshold.
        over threshold: return False
        within threshold: return True
        """
        res = eval(f'self.{self._mode.value["name"]}(self.path)')
        if res is None:
            raise DiskValueError("disk value must be not None.")
        if eval(f"{res} {self._mode.value['logic'].value} {self._threshold}"):
            return False
        else:
            return True

    @staticmethod
    def _usage(path):
        if not isinstance(path, str):
            raise DiskTypeError("path must be string type.")
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} not exists")
        return psutil.disk_usage(path)

    @staticmethod
    def percent(path):
        return DiskDetect._usage(path).percent

    @staticmethod
    def free(path):
        return DiskDetect._usage(path).free

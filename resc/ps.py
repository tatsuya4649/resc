import psutil
import resource
from .logical import Logic
from .detect import DetectBase
from enum import Enum
import re


class PSDetectTypeError(TypeError):
    pass


class PSDetectMode(Enum):
    PERCENT = {"name": "percent", "logic": Logic.GT}
    NUMBER = {"name": "number", "logic": Logic.GT}


class PSDetectLimits(Enum):
    SOFT = "soft"
    HARD = "hard"


class PSDetect(DetectBase):
    def __init__(
        self,
        threshold,
        mode=PSDetectMode.PERCENT.value["name"],
        limits=PSDetectLimits.SOFT.value,
    ):
        self.threshold = threshold
        self.mode = mode
        self.limits = limits

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self,value):
        if not isinstance(value, (int, float)):
            raise PSDetectTypeError(
                "threshold must be int or float type."
            )
        self._threshold = value

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if not isinstance(value ,str):
            raise PSDetectTypeError(
                "mode must be str type."
            )
        if value not in [ x.value["name"] for x in PSDetectMode ]:
            raise PSDetectValueError(
                "invalid mode value. "
                f"(valid: {[ x.value['name'] for x in PSDetectMode ]})"
            )
        self._mode = [
            x for x in PSDetectMode
            if re.match(
                rf'^{x.value["name"]}$',
                f'{value}',
                flags=re.IGNORECASE
            )][0]

    @property
    def limits(self):
        self._limits

    @limits.setter
    def limits(self, value):
        if not isinstance(value, str):
            raise PSDetectTypeError(
                "limits must be str type."
            )
        if value not in [ x.value for x in PSDetectLimits ]:
            raise PSDetectValueError(
                "invalid limits value. "
                f"(valid: {[ x.value for x in PSDetectLimits ]})"
            )
        self._limits = value

    @property
    def maxps(self):
        return resource.getrlimit(resource.RLIMIT_NPROC)

    @property
    def percent(self):
        soft, hard = self.maxps
        if self.limits == PSDetectLimits.SOFT.value:
            return float(self.number)/float(soft)
        else:
            return float(self.number)/float(hard)

    @property
    def number(self):
        pids = psutil.pids()
        return len(pids)

    @property
    def check(self):
        """
        Check over PS threshold.
        over threshold: return False
        within threshold: return True
        """
        if self.mode is PSDetectMode.PERCENT:
            res = eval(f"self.{self.mode.value['name']}")
        else:
            res = eval(f"self.{self.mode.value['name']}")
        if eval(f"{res} {self._mode.value['logic'].value} {self.threshold}"):
            return False
        else:
            return True

    @property
    def resource(self):
        return "ps"

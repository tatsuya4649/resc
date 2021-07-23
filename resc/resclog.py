import enum
from enum import Enum
import time
import datetime
import re

@enum.unique
class RescLogFormat(Enum):
    DATE="date"
    OVER="over"
    FUNC="func"
    FILE="file"
    REMO="remo"
    SOUR="sour"

class RescLogTypeError(TypeError):
    pass
class RescLogValueError(ValueError):
    pass

class RescLog: 
    """
    """
    _LOGPATH_DEFAULT="~/.resc/log/"
    _LOGFILE_DEFAULT=""
    _LOGFORMAT_DEFAULT=[
        RescLogFormat.DATE,
        RescLogFormat.OVER,
        RescLogFormat.FUNC,
        RescLogFormat.REMO,
        RescLogFormat.FILE,
    ]

    def __init__(
            self,
            logfile=None,
            format=None,
    ):
        self.logfile=logfile
        self.format=self._default_format(format)
        self._date = str(datetime.datetime.now())
        self._over = "over"
        self._func = "func"
        self._file = "file"
        self._remo = "ip"
        self._sour = "sour"

    @property
    def log(self):
            return self._logfile is not None
    @staticmethod
    def default_directory():
        return RescLog._LOGPATH_DEFAULT
    def _default_format(self,format):
        if format is not None and isinstance(format,list) \
            and len([x for x in format if x not in RescLogFormat]) == 0:
            return format
        else:
            return self._LOGFORMAT_DEFAULT

    @property
    def format_str(self):
        results = list()
        for f in self.format:
            if not isinstance(f,RescLogFormat):
                raise RescLogTypeError("format must be RescLogFormat(enum) type.")
            f_str = eval(f'self.format_{f.value}(self._{f.value})')
            results.append(f_str)
        return " ".join(results)
    def format_date(self,date):
        return date
    def format_over(self,over):
        return over
    def format_func(self,func):
        return func
    def format_remo(self,remo):
        return remo
    def format_file(self,file):
        return file
    def format_sour(self,sour):
        return sour
    @property
    def date(self):
        pass
    @date.getter
    def date(self):
        return self._date
    @date.setter
    def date(self,date):    
        self._date = date
    @property
    def over(self):
        pass
    @over.getter
    def over(self):
        return self._over
    @over.setter
    def over(self,over):
        self._over = over
    
    @property
    def func(self):
        pass
    @func.getter
    def func(self):
        return self._func
    @func.setter
    def func(self,func):
        self._func = func
    @property
    def remo(self):
        pass
    @remo.getter
    def remo(self):
        return self._remo
    @remo.setter
    def remo(self,remo):
        self._remo = remo
    @property
    def sour(self):
        pass
    @sour.getter
    def sour(self):
        return self._sour
    @sour.setter
    def sour(self,sour):
        self._sour = sour
    @property
    def file(self):
        pass
    @file.getter
    def file(self):
        return self._file
    @file.setter
    def file(self,file):
        self._file = file
    
    
    def write(self):
        for f in self._format:
            if not hasattr(self,f"{f.value}") or eval(f'self._{f.value}') is None:
                    raise RescLogValueError(f"threre is \"{f.value}\" in format,but not define.")
        with open(self._logfile,"a") as f:
            f.write(f"{self.format_str}\n")
    @property
    def _import_log(self):
        return "from resc import RescLog\n"
    def _define_resclog(self,resclog):
        lists=list()
        for k,v in vars(self).items():
            lists.append(f"resclog.{re.sub(r'^_','',k)}={v}")
        res = str()
        res += "resclog=RescLog(\n"
        res += f"logfile=\"{resclog.logfile}\",\n"
        res += f"format={resclog.format},\n"
        res += ")\n"
        res += "%s"%('\n'.join(lists))
        return res

    @property
    def _write_log(self):
        return "\tresclog.Write()\n"


__all__ = [
    RescLog.__name__,
]
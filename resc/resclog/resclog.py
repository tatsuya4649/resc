import enum
from enum import Enum
from logging import log
import pathlib
import time
import datetime
import re
import sys
import os
from .header import RescLogHeader
from .rformat import RescLogFormat,RescLogOver

from paramiko.util import log_to_file

class RescLogTypeError(TypeError):
    pass
class RescLogValueError(ValueError):
    pass
class RescLogPathError(Exception):
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
        RescLogFormat.SOUR,
    ]

    def __init__(
            self,
            logfile=None,
            format=None,
    ):
        if logfile is not None:
            self.pure_log = logfile
            self.logfile=self._LOGPATH_DEFAULT + re.sub(r'^/','',logfile)
            self.logfile=re.sub(r'^~',f'{os.path.expanduser("~")}',self.logfile)
        else:
            self.pure_log = None
            self.logfile = None
        log_pathlist = list()
        for path in os.path.dirname(self.logfile).split('/'):
            log_pathlist.append(path)
            path = "/".join(log_pathlist)
            if len(path) > 0 and not os.path.isdir(path):
                os.mkdir(path)
        self.format=self._default_format(format)
        self._date = str(datetime.datetime.now())
        self._over = RescLogOver.FALSE
        self._func = None
        self._file = None
        self._remo = None
        self._sour = None

    @property
    def log(self):
            return self.logfile is not None
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
            results.append(str(f_str))
        return " ".join(results)

    def format_date(self,date):
        date_str = str()
        date_str = str(date)
        return date_str
    def format_over(self,over):
        over_str = str()
        over_str = str(over)
        return over_str
    def format_func(self,func):
        func_str = str()
        func_str = str(func)
        return func_str
    def format_remo(self,remo):
        remo_str = str()
        remo_str = str(remo)
        return remo_str
    def format_file(self,file):
        file_str = str()
        file_str = str(file)
        return file_str
    def format_sour(self,sour):
        sour_str = str()
        sour_str = str(sour)
        return sour_str

    @property
    def date(self):
        pass
    @date.getter
    def date(self):
        return str(self._date).encode("utf-8")
    @date.setter
    def date(self,date):
        if not isinstance(date,datetime.datetime) and not isinstance(date,str):
            raise RescLogTypeError(f"date must be datetime or str.now {type(date)}")
        self._date = str(date)
    @property
    def over(self):
        pass
    @over.getter
    def over(self):
        return self._over.value.encode("utf-8")
    @over.setter
    def over(self,over):
        if not isinstance(over,RescLogOver):
            raise RescLogTypeError(f"over must be RescLogOver.now ({type(over)})")
        self._over = over
    
    @property
    def func(self):
        pass
    @func.getter
    def func(self):
        return self._func.encode("utf-8")
    @func.setter
    def func(self,func):
        if not isinstance(func,str):
            raise RescLogTypeError(f"func must be str. now {type(func)}")
        self._func = func
    @property
    def remo(self):
        pass
    @remo.getter
    def remo(self):
        return self._remo.encode("utf-8")
    @remo.setter
    def remo(self,remo):
        if not isinstance(remo,str):
            raise RescLogTypeError(f"remo must be str. now {type(remo)}")
        self._remo = remo
    @property
    def sour(self):
        pass
    @sour.getter
    def sour(self):
        return self._sour
    @sour.setter
    def sour(self,sour):
        if not isinstance(sour,bytes):
            raise RescLogTypeError(f"sour must be bytes. now {type(sour)}")
        self._sour = sour
    @property
    def file(self):
        pass
    @file.getter
    def file(self):
        return self._file.encode("utf-8")
    @file.setter
    def file(self,file):
        if not isinstance(file,str):
            raise RescLogTypeError(f"file must be str. now {type(file)}")
        self._file = file
    
    @property
    def stdout(self):
        pass
    @stdout.getter
    def stdout(self):
        if not hasattr(self,"_stdout"):
            return b''
        res = bytes()
        for ele in self._stdout:
            res += ele
        return res
    @stdout.setter
    def stdout(self,out):
        if not isinstance(out,list):
            raise RescLogTypeError("output must be list type.")
        if not hasattr(self,"_stdout"):
            self._stdout = list()
        self._stdout += out
    @property
    def stderr(self):
        pass
    @stderr.getter
    def stderr(self):
        if not hasattr(self,"_stderr"):
            return b''
        res = bytes()
        for ele in self._stderr:
            res += ele
        return res
    @stderr.setter
    def stderr(self,out):
        if not isinstance(out,list):
            raise RescLogTypeError("output must be list type.")
        if not hasattr(self,"_stderr"):
            self._stderr = list()
        self._stderr += out
    
    @property
    def body(self):
        res = bytes()
        for f in RescLogFormat:
            if f in self.format:
                if isinstance(eval(f'self.{f.value}'),str):
                    res += eval(f'self.{f.value}.encode("utf-8")')
                elif isinstance(eval(f'self.{f.value}'),bytes):
                    res += eval(f'self.{f.value}')
                else:
                    res += eval(f'str(self.{f.value}).encode("utf-8")')
        return res
    def header(self):
        lendict = dict()
        for f in RescLogFormat:
            if f in self.format:
                value = eval(f'self.{f.value}')
                if not isinstance(value,bytes):
                    raise RescLogTypeError(f"{value}({f}) must be str type.")
                lendict[f.value] = len(value)
        self._header = RescLogHeader(
            bodylen=len(self.body),
            stdoutlen=len(self.stdout),
            stderrlen=len(self.stderr),
            flaglist=RescLogHeader.convert(self.format),
            lendict=lendict,
        )
        return self._header.bytes
    def write(self,over):
        if self.log:
            self.over = over
            for f in self.format:
                if not hasattr(self,f"{f.value}") or eval(f'self.{f.value}') is None:
                        raise RescLogValueError(f"threre is \"{f.value}\" in format,but not define.")
            with open(self.logfile,"a") as f:
                f.write(f"{self.header()}")
                f.write(f"{self.body}")
                f.write(f"{self.stdout}")
                f.write(f"{self.stderr}")
    @property
    def _import_log(self):
        log_str = str()
        log_str += "from resc import RescLog,RescLogFormat,RescLogOver\n"
        log_str += "import re\n"
        return log_str
    def _define_resclog(self,resclog):
        lists=list()
        for k,v in vars(self).items():
            value = v if not isinstance(v,str) else f'\"{v}\"'
            if re.match('^_',k) is not None:
                lists.append(f"resclog.{re.sub(r'^_','',k)}={value}")
        res = str()
        res += "resclog=RescLog(\n"
        if resclog.logfile is not None:
            res += f"logfile=\"{resclog.pure_log}\",\n"
        res += f"format={self.format_meta(resclog)},\n"
        res += ")\n"
        res += "%s"%('\n'.join(lists))
        res += "\n"
        return res
    def format_meta(self,resclog):
        meta_list = list()
        for format in resclog.format:
            meta_list.append(format.__class__.__name__ + '.' + format.name)
        return re.sub(r"'",'',str(meta_list))
    @property
    def _noover_log(self):
        return f"else:\n\t{self._write_log_noover}"

    @property
    def _write_log_over(self):
        return "\tresclog.write(RescLogOver.TRUE)\n"
    @property
    def _write_log_noover(self):
        return "resclog.write(RescLogOver.FALSE)\n"
    

__all__ = [
    RescLog.__name__,
    RescLogFormat.__name__,
]

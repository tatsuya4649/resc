import os
import re
import io
import pathlib
from ctypes import *

from resc.resclog.rformat import RescLogFormat
from .cons import COMMONMAGIC
from .header import RescLogSFlag,RescLogEmergeHeader,RescLogHeader
from .dump import RescDump
from .anaerr import *

class RescLogCommonHeader(LittleEndianStructure):
        _fields_ = (
            (COMMONMAGIC.IDENTIFY_NAME,COMMONMAGIC.IDENTIFY_TYPE),
            (COMMONMAGIC.COMMONFLAG_NAME,COMMONMAGIC.COMMONFLAG_TYPE),
        )

class RescLogAnalyze:
    def __init__(self,path):
        self._path = path
    @property
    def path(self):
        pass
    @path.getter
    def path(self):
        return re.sub(r'^~',os.path.expanduser('~'),self._path)

    def _emerge(self,sflag):
        if (RescLogSFlag.EME.value["flag"] & sflag) != 0 and (RescLogSFlag.ERR.value["flag"] & sflag) != 0:
            return True
        else:
            return False

    def _errinfo(self,flag_set):
        for flag in flag_set:
            print(flag.value["explain"])
    
    def _analyze_deco(func):
        def _wrapper(*args,**kwargs):
            if "counter" not in kwargs.keys() or not isinstance(kwargs["counter"],int):
                raise RescLogKeyError("_analyze_deco must be counter argument(int type).")
            print(f"----------------------analyze({kwargs['counter']})------------------------")
            result = func(*args,**kwargs)
            print("--------------------------------------------------------------")
            return result
        return _wrapper

    @_analyze_deco
    def _analyze(
        self,
        log,
        **kwargs,
    ):
        if not isinstance(log,bytes):
            raise RescLogTypeError("log must be bytes type.")
        common_header = RescLogCommonHeader()
        now_log = log
        _buffer = io.BytesIO(log)
        _now_seek = _buffer.tell()
        _buffer.readinto(common_header)
        identify = common_header.identify
        sflag = common_header.sflag
        if common_header.identify != COMMONMAGIC.IDENTIFY:
            return False,None
        flag_set = set()
        for flag in RescLogSFlag:
            if flag.value["flag"] & sflag:
                flag_set.add(flag)
        # Emergency Headr
        if self._emerge(sflag):
            _buffer.seek(_now_seek)
            emergeheader = RescLogEmergeHeader()
            _buffer.readinto(emergeheader)
            error_length = emergeheader.errlen
            print(f'ERROR LENGTH: {error_length}')
            err = _buffer.read(error_length)
            print(f'ERROR CONTENT: {err}')
            print(f'ERROR BINARY: {RescDump.bindump(err)}')
        # Nornal Header
        else:
            _buffer.seek(_now_seek)
            logheader = RescLogHeader()
            _buffer.readinto(logheader)
            header_length = logheader.headlen
            body_length = logheader.bodylen
            date_length = logheader.datelen
            over_length = logheader.overlen
            func_length = logheader.funclen
            file_length = logheader.filelen
            remo_length = logheader.remolen
            sour_length = logheader.sourlen
            stdout_length = logheader.stdoutlen
            stderr_length = logheader.stderrlen
            print(f'HEAEDR LENGTH: {header_length}')
            print(f'BODY LENGTH: {body_length}')
            print(f'\tDATE LENGTH: {date_length}')
            print(f'\tOVER LENGTH: {over_length}')
            print(f'\tFUNC LENGTH: {func_length}')
            print(f'\tFILE LENGTH: {file_length}')
            print(f'\tREMO LENGTH: {remo_length}')
            print(f'\tSOUR LENGTH: {sour_length}')
            if body_length != (date_length+over_length+func_length+file_length+remo_length+sour_length):
                raise RescLogUnMatchError("unmatch total body length and individual length.")
            print(f'STDOUT LENGTH: {stdout_length}')
            print(f'STDERR LENGTH: {stderr_length}')
            body = _buffer.read(body_length)
            body_buffer = io.BytesIO(body)
            date = body_buffer.read(date_length)
            over = body_buffer.read(over_length)
            func = body_buffer.read(func_length)
            file = body_buffer.read(file_length)
            remo = body_buffer.read(remo_length)
            sour = body_buffer.read(sour_length)
            stdout = _buffer.read(stdout_length)
            stderr = _buffer.read(stderr_length)
            print(f'BODY CONTENT: {body}')
            print(f'BODY BINARY: {RescDump.bindump(body)}')
            print(f'\tDATE: {date}')
            print(f'\tDATE BINARY: {RescDump.bindump(date)}')
            print(f'\tOVER: {over}')
            print(f'\tOVER BINARY: {RescDump.bindump(over)}')
            print(f'\tFUNC: {func}')
            print(f'\tFUNC BINARY: {RescDump.bindump(func)}')
            print(f'\tREMO: {remo}')
            print(f'\tREMO BINARY: {RescDump.bindump(remo)}')
            print(f'\tSOUR: {sour}')
            print(f'\tSOUR BINARY: {RescDump.bindump(sour)}')
            print(f'STDOUT CONTENT: {stdout}')
            print(f'STDERR CONTENT: {stderr}')
        if len(flag_set)>0:
            self._errinfo(flag_set)
        return True,log[_buffer.tell():]

    def getlog(self):
        if not pathlib.Path(self.path).is_absolute():
            self._path = str(pathlib.Path(self.path).resolve())
        if not os.path.isfile(self.path):
            raise RescLogPathError(f"not found {self.path}")
        with open(self.path,"rb") as f:
            alllog = f.read()
        return alllog
    def analyze(self):
        alllog = self.getlog()
        counter = 0
        while True:
            result,alllog = self._analyze(alllog,counter=counter)
            counter += 1
            if not result or len(alllog)==0:
                break

__all__ = [
    RescLogAnalyze.__name__,
]
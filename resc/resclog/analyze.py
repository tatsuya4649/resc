import os
import re
import io
import pathlib
from ctypes import *
from resc.resclog.cons import header

from resc.resclog.rformat import RescLogFormat
from .cons import COMMONMAGIC
from .header import RescLogSFlag,RescLogEmergeHeader,RescLogHeader
from .dump import RescDump, RescDumpTypeError
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

    @classmethod
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
    
    @classmethod
    def _analyze_dict(
        self,
        log,
        **kwargs,
    ):
        resdict = dict()
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
            return False,None,None
        flag_set = set()
        for flag in RescLogSFlag:
            if flag.value["flag"] & sflag:
                flag_set.add(flag)
        # Emergency Headr
        if RescLogAnalyze._emerge(sflag):
            _buffer.seek(_now_seek)
            emergeheader = RescLogEmergeHeader()
            _buffer.readinto(emergeheader)
            error_length = emergeheader.errlen
            date_length = emergeheader.datelen
            err = _buffer.read(error_length)
            date = _buffer.read(date_length)
            resdict["sflag"] = sflag
            resdict["error_length"] = error_length
            resdict["date_length"] = date_length
            resdict["error_content"] = err
            resdict["error_binary"] = RescDump.bindump(err)
            resdict["date_content"] = date
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
            
            resdict["sflag"] = sflag
            resdict["header_length"] = header_length
            resdict["body_length"] = body_length
            resdict["date_length"] = date_length
            resdict["over_length"] = over_length
            resdict["func_length"] = func_length
            resdict["file_length"] = file_length
            resdict["remo_length"] = remo_length
            resdict["sour_length"] = sour_length
            if body_length != (date_length+over_length+func_length+file_length+remo_length+sour_length):
                raise RescLogUnMatchError("unmatch total body length and individual length.")
            resdict["stdout_length"] = stdout_length
            resdict["stderr_length"] = stderr_length
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
            resdict["body_content"] = body
            resdict["body_binary"] = RescDump.bindump(body)
            resdict["date_content"] = date
            resdict["date_binary"] = RescDump.bindump(date)
            resdict["over_content"] = over
            resdict["over_binary"] = RescDump.bindump(over)
            resdict["func_content"] = func
            resdict["func_binary"] = RescDump.bindump(func)
            resdict["file_content"] = file
            resdict["file_binary"] = RescDump.bindump(file)
            resdict["remo_content"] = remo
            resdict["remo_binary"] = RescDump.bindump(remo)
            resdict["sour_content"] = sour
            resdict["sour_binary"] = RescDump.bindump(sour)
            resdict["stdout_content"] = stdout
            resdict["stderr_content"] = stderr
        return True,log[_buffer.tell():],resdict

    def getlog(self):
        if not pathlib.Path(self.path).is_absolute():
            self._path = str(pathlib.Path(self.path).resolve())
        if not os.path.isfile(self.path):
            raise RescLogPathError(f"not found {self.path}")
        with open(self.path,"rb") as f:
            alllog = f.read()
        return alllog
    @classmethod
    def analyze(self,logbytes):
        results = list()
        alllog = logbytes
        while True:
            result,alllog,logdict = RescLogAnalyze._analyze_dict(alllog)
            if logdict is not None:
                results.append(logdict)
            if not result or len(alllog)==0:
                break
        return results

__all__ = [
    RescLogAnalyze.__name__,
]
from ctypes import c_uint32, c_int32, c_uint16, LittleEndianStructure, sizeof
import io
from enum import Enum
import re
from .cons import COMMONMAGIC
from .rformat import RescLogFormat


class RescLogFlag(Enum):
    DATE = 1 << 0
    OVER = 1 << 1
    FUNC = 1 << 2
    FILE = 1 << 3
    REMO = 1 << 4
    SOUR = 1 << 5


class RescLogHeaderTypeError(TypeError):
    pass


class RescLogSFlag(Enum):
    # General Error
    ERR = {"flag": 1 << 0, "explain": "General Error."}
    # Emergency Header
    EME = {"flag": 1 << 1, "explain": "Emergency Header."}
    # Defination Error
    DEF = {"flag": 1 << 2, "explain": "Defination Error."}
    # RescLog Error
    ROG = {"flag": 1 << 3, "explain": "RescLog Error."}
    # SSH Error
    SSH = {"flag": 1 << 4, "explain": "SSH Error."}
    # Remote Host Error
    REM = {"flag": 1 << 5, "explain": "Remote Host Error."}
    # Local Host Error
    LOC = {"flag": 1 << 6, "explain": "Local Host Error."}
    # Module Not Found Error
    MNF = {"flag": 1 << 7, "explain": "Module Not Found Error."}
    # Import Error
    IMP = {"flag": 1 << 8, "explain": "Import Error."}
    # Function Error
    FUN = {"flag": 1 << 9, "explain": "Trigger Function Error."}
    # Indent Error
    IND = {"flag": 1 << 10, "explain": "Indent Error."}
    # Not Found Script File
    NFS = {"flag": 1 << 11, "explain": "Not Found Script File Error."}
    # Reverse
    RVS = {"flag": 1 << 12, "explain": "Reverse Exceeded Flag."}


class RescLogEmergeHeader(LittleEndianStructure):
    _fields_ = (
        (COMMONMAGIC.IDENTIFY_NAME, COMMONMAGIC.IDENTIFY_TYPE),
        (COMMONMAGIC.COMMONFLAG_NAME, COMMONMAGIC.COMMONFLAG_TYPE),
        ('errlen', c_int32),
        ('datelen', c_int32),
    )


class RescLogHeader(LittleEndianStructure):
    _fields_ = (
        (COMMONMAGIC.IDENTIFY_NAME, COMMONMAGIC.IDENTIFY_TYPE),
        (COMMONMAGIC.COMMONFLAG_NAME, COMMONMAGIC.COMMONFLAG_TYPE),
        ('headlen', c_uint16),
        ('bodylen', c_uint32),
        ('stdoutlen', c_uint32),
        ('stderrlen', c_uint32),
        (f'{RescLogFormat.DATE.value}len', c_uint16),
        (f'{RescLogFormat.OVER.value}len', c_uint16),
        (f'{RescLogFormat.FUNC.value}len', c_uint16),
        (f'{RescLogFormat.FILE.value}len', c_uint16),
        (f'{RescLogFormat.REMO.value}len', c_uint16),
        (f'{RescLogFormat.SOUR.value}len', c_uint16),
        ('flag', c_uint32),
    )

    @classmethod
    def _flag(self, flaglist):
        if not isinstance(flaglist, list):
            raise RescLogHeaderTypeError("flaglist must be list type.")
        if len([x for x in flaglist if not isinstance(x, RescLogFlag)]) != 0:
            raise RescLogHeaderTypeError(
                "flaglist element must be list RescLogFlag."
            )
        flaglist = list(set(flaglist))
        result = int(0)
        for flag in flaglist:
            result |= flag.value
        return result

    @classmethod
    def convert(self, formatlist):
        res = list()
        for f in formatlist:
            res.append(
                eval(f"{re.sub('^RescLogFormat', 'RescLogFlag', str(f))}"))
        return res

    @staticmethod
    def length():
        return sizeof(RescLogHeader)

    @property
    def bytes(self):
        buffer = io.BytesIO()
        buffer.write(self)
        return buffer.getvalue()

from ctypes import *

class COMMONMAGIC:
    IDENTIFY=b'resc'
    IDENTIFY_NAME="identify"
    IDENTIFY_TYPE=c_char*4

    COMMONFLAG_NAME="sflag"
    COMMONFLAG_TYPE=c_uint32

__all__ = [
    COMMONMAGIC.__name__,
]
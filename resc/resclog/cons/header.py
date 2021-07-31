from ctypes import c_char, c_uint32


class COMMONMAGIC:
    IDENTIFY = b'resc'
    IDENTIFY_NAME = "identify"
    IDENTIFY_TYPE = c_char * 4

    COMMONFLAG_NAME = "sflag"
    COMMONFLAG_TYPE = c_uint32

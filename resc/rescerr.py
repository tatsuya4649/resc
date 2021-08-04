class RescTypeError(TypeError):
    pass


class RescValueError(ValueError):
    pass


class RescAttributeError(AttributeError):
    pass


class RescKeyError(KeyError):
    pass


class RescServerError(Exception):
    pass


class RescCronError(Exception):
    pass


class RescSSHError(Exception):
    pass


class RescSCPError(Exception):
    pass


class RescSCPException(Exception):
    pass


class RescSSHFileNotFoundError(FileNotFoundError):
    pass


class RescSCPFileNotFoundError(FileNotFoundError):
    pass


class RescSSHConnectionError(Exception):
    pass


class RescSSHTimeoutError(Exception):
    pass

class DetectBaseNotImplementedError(NotImplementedError):
    pass


class DetectInheritenceError(Exception):
    pass


class DetectAttributeError(AttributeError):
    pass


class DetectMeta(type):
    _MUSTATTRS=[
        "resource",
        "check",
        "threshold",
    ]
    def __new__(
        cls,
        name,
        bases,
        attributes
    ):
        for attr in DetectMeta._MUSTATTRS:
            if attr not in attributes.keys():
                raise DetectAttributeError(
                    f"{attr} must be defined."
                )
        return super().__new__(
            cls,
            name,
            bases,
            attributes
        )

class DetectBase(metaclass=DetectMeta):

    def __init__(self):
        raise DetectInheritenceError(
            f"{__class__.__name__} must be inherited."
        )

    def _notimplestr(self, param):
        return (
            "resource detect must have "
            f"{param}\" property."
        )

    @property
    def resource(self):
        raise DetectBaseNotImplementedError(
            self._notimplestr("resource")
        )

    @property
    def mode(self):
        raise DetectBaseNotImplementedError(
            self._notimplestr("mode")
        )

    @property
    def check(self):
        raise DetectBaseNotImplementedError(
            self._notimplestr("check")
        )

    @property
    def threshold(self):
        raise DetectBaseNotImplementedError(
            self._notimplestr("threshold")
        )

    @property
    def percent(self):
        raise DetectBaseNotImplementedError(
            self._notimplestr("percent")
        )

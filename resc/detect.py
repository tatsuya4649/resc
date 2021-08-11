class DetectBaseNotImplementedError(NotImplementedError):
    pass

class DetectMeta(type):
    def __new__(
        cls,
        name,
        bases,
        attributes
    ):
        return super().__new__(
            cls,
            name,
            bases,
            attributes
        )

class DetectBase(metaclass=DetectMeta):
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

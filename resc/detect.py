class DetectBaseNotImplementedError(NotImplementedError):
    pass


class DetectBase:
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

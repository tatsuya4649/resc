class RescLogPathError(FileNotFoundError):
    pass
class RescLogTypeError(TypeError):
    pass
class RescLogKeyError(KeyError):
    pass
class RescLogUnMatchError(ValueError):
    pass

__all__ = [
    RescLogPathError.__name__,
    RescLogTypeError.__name__,
    RescLogKeyError.__name__,
    RescLogUnMatchError.__name__,
]
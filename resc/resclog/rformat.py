from enum import Enum
import enum


@enum.unique
class RescLogFormat(Enum):
    DATE = "date"
    OVER = "over"
    FUNC = "func"
    FILE = "file"
    REMO = "remo"
    SOUR = "sour"


@enum.unique
class RescLogOver(Enum):
    TRUE = "True"
    FALSE = "False"

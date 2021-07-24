import os
import re
import pathlib

class RescLogAnalyze:
    def __init__(self,path):
        self._path = path
    def analyze(self):
        self._path = re.sub(r'^~',os.path.expanduser('~'),self._path)
        if not pathlib.Path(self._path).is_absolute():
            self._path = pathlib.Path(self._path).resolve()
        if not os.path.isfile(self._path):
            raise RescLogPathError(f"not found {self._path}")
        with open(self._path,"rb") as f:
            buffer = f.read()
            print(buffer)
            print(type(buffer))

__all__ = [
    RescLogAnalyze.__name__,
]
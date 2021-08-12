import json
import os
import hashlib
import inspect
import sys


class RescJSONError(Exception):
    pass


class RescJSONKeyError(KeyError):
    pass


class RescJSONTypeError(TypeError):
    pass


class RescJSONFileNotFoundError(FileNotFoundError):
    pass


class RescJSON:
    def __new__(
        cls,
        dump_filepath,
    ):
        return super().__new__(cls)

    def __init__(
        self,
        dump_filepath,
    ):
        self._dump_filepath = dump_filepath

    @staticmethod
    def dump_row(
        dump_filepath,
        _jdict
    ):
        try:
            if os.path.isfile(dump_filepath):
                with open(dump_filepath) as f:
                    _jsons = json.load(f)
            else:
                _jsons = list()
            _jsons.append(_jdict)
            with open(dump_filepath, "w") as f:
                json.dump(_jsons, f)
        except Exception as e:
            raise RescJSONError(e)

    @staticmethod
    def _hash(key):
        return hashlib.sha256(
            key.encode("utf-8")
        ).hexdigest()

    @property
    def dump_filepath(self):
        return self._dump_filepath

    @classmethod
    def json_search(
        self,
        hash_value,
        key,
        dump_filepath
    ):
        if not isinstance(key, str):
            raise RescJSONTypeError(
                "key must be str type."
            )
        if not os.path.isfile(dump_filepath):
            raise RescJSONFileNotFoundError(
                "JSON file not found."
            )
        with open(dump_filepath) as f:
            _jsons = json.load(f)

        for _json in _jsons:
            if hash_value == _json["hash"] and key in _json.keys():
                return _json[key]
        return None

    @staticmethod
    def _iter(dump_filepath):
        with open(dump_filepath, "r") as f:
            print(f.read())
        try:
            with open(dump_filepath) as f:
                jsons = json.load(f)
        except json.decoder.JSONDecodeError as e:
            return iter([])
        except Exception as e:
            raise RescJSONError(e)
        return iter(jsons)

    def __iter__(
        self,
    ):
        return RescJSON._iter(self._dump_filepath)

    @property
    def length(self):
        return len(list(iter(self)))

    @staticmethod
    def jdump(
        dump_filepath,
        elements
    ):
        with open(dump_filepath, "w") as f:
            json.dump(elements, f)

    @staticmethod 
    def display(
        dump_filepath,
    ):
        try:
            _jsons = RescJSON._iter(dump_filepath)
        except RescJSONError as e:
            print("Not found json path", file=sys.stderr)
            sys.exit(1)
        print(_jsons)

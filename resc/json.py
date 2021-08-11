import ndjson
import os
import hashlib
import inspect


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
            with open(dump_filepath, "a") as f:
                writer = ndjson.writer(f)
                writer.writerow(_jdict)
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
            _jsons = ndjson.load(f)

        for json in _jsons:
            if hash_value == json["hash"] and key in json.keys():
                return json[key]
        return None

    @staticmethod
    def _iter(dump_filepath):
        try:
            with open(dump_filepath) as f:
                jsons = ndjson.load(f)
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
            writer = ndjson.writer(f)
            for element in elements:
                writer.writerow(element)

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
        compiled_file,
        crontab_line,
        register_file,
        function,
        log_file=None,
    ):
        cls._keys = [
            "compiled_file",
            "crontab_line",
            "register_file",
            "func_source",
            "func_name",
            "log_file",
        ]
        self = super().__new__(cls)
        func_name = function.__name__
        func_source = inspect.getsource(
            function.__code__
        )
        for key in cls._keys:
            exec(f"self.{key} = {key}")
        self.hash = RescJSON._hash(
            compiled_file
        )
        return self

    def __init__(
        self,
        dump_filepath,
        compiled_file,
        crontab_line,
        register_file,
        function,
        log_file=None,
    ):
        _jdict = dict()
        _jdict["compiled_file"] = compiled_file
        _jdict["crontab_line"] = crontab_line
        _jdict["register_file"] = register_file
        _jdict["func_source"] = inspect.getsource(
            function.__code__
        )
        _jdict["funcname"] = function.__name__
        if log_file is not None:
            _jdict["log_file"] = log_file
        _jdict["hash"] = self._hash(compiled_file)
        self._jdict = _jdict

        self._dump_filepath = dump_filepath

        try:
            with open(self._dump_filepath, "a") as f:
                writer = ndjson.writer(f)
                writer.writerow(_jdict)
        except Exception as e:
            raise RescJSONError(e)

    @staticmethod
    def _hash(key):
        return hashlib.sha256(
            key.encode("utf-8")
        ).hexdigest()

    def __call__(self):
        return self._jdict

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
        if key not in RescJSON._keys:
            raise RescJSONKeyError(
                f"invalid key ({key}). "
                f"valid key ({RescJSON._keys})"
            )
        if not os.path.isfile(dump_filepath):
            raise RescJSONFileNotFoundError(
                "JSON file not found."
            )
        with open(dump_filepath) as f:
            _jsons = ndjson.load(f)

        for json in _jsons:
            if hash_value == json["hash"]:
                return json["crontab_line"]
        return None

    def __iter__(
        self,
    ):
        try:
            with open(self._dump_filepath) as f:
                jsons = ndjson.load(f)
        except Exception as e:
            raise RescJSONError(e)
        return iter(jsons)

    @property
    def length(self):
        return len(list(iter(self)))

    def jdelete(
        self,
        hash_value
    ):
        elements = [ x for x in self
            if x["hash"] != hash_value ]
        with open(self._dump_filepath, "w") as f:
            writer = ndjson.writer(f)
            for element in elements:
                writer.writerow(element)


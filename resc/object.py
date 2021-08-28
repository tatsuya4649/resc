import sys
import os
import tempfile
import importlib
import datetime
import inspect
from .json import RescJSON
from .cron import Cron
from .compile import RescCompile


class RescObjectTypeError(TypeError):
    pass


class RescObjectValueError(ValueError):
    pass


class RescObjectKeyError(KeyError):
    pass


class RescObjectImportError(ImportError):
    pass


class RescObjectAttributeError(ImportError):
    pass


class RescObjectIndentationError(IndentationError):
    pass


class RescObjectSyntaxError(SyntaxError):
    pass


class RescObject(RescJSON):
    def __new__(
        cls,
        dump_filepath,
        compiled_file,
        crontab_line,
        limit,
        permanent,
        function=None,
        exec_file=None,
        log_file=None,
    ):
        if not hasattr(cls, "_hashmodule"):
            cls._hashmodule = dict()
        cls._keys = [
            "compiled_file",
            "register_date",
            "crontab_line",
            "func_source",
            "func_name",
            "exec_file",
            "limit",
            "permanent",
            "log_file",
        ]
        self = super().__new__(
            cls,
            dump_filepath=dump_filepath,
        )
        if function is not None:
            func_name = function.__name__
            func_source = inspect.getsource(
                function.__code__
            )
        for key in cls._keys:
            if key in locals().keys():
                exec(f"self.{key} = {key}")
        self.hash = RescJSON._hash(
            compiled_file
        )
        if not hasattr(self, "hash"):
            raise RescObjectKeyError(
                "jresc must have hash key."
            )
        return self

    def __init__(
        self,
        dump_filepath,
        compiled_file,
        crontab_line,
        limit,
        permanent,
        function=None,
        exec_file=None,
        log_file=None,
    ):
        super().__init__(
            dump_filepath,
        )
        _jdict = dict()
        _jdict["register_date"] = self.date
        _jdict["compiled_file"] = compiled_file
        _jdict["crontab_line"] = crontab_line
        _jdict["limit"] = limit
        _jdict["limit_init"] = limit
        _jdict["permanent"] = permanent
        if function is not None:
            _jdict["func_source"] = self.func_source
            _jdict["func_name"] = self.func_name
        else:
            _jdict["exec_file"] = exec_file

        if log_file is not None:
            _jdict["log_file"] = log_file
        _jdict["hash"] = self._hash(compiled_file)
        self._jdict = _jdict

        self.dump_row(self._dump_filepath,_jdict)

    def __enter__(
        self
    ):
        self.import_module()
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):
        self.close()
    
    @property
    def date(self):
        return datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    def _create_module(self, source):
        self._tempfp = tempfile.NamedTemporaryFile(
            mode="w+b",
            prefix="resc_object_",
            suffix=".py",
            delete=False,
        )
        self._tempfile_name = self._tempfp.name
        compiled_code = RescCompile.compile(source)
        self._tempfp.write(compiled_code.encode("utf-8"))
        self._tempfp.seek(0)
        RescObject._hashmodule[self.hash]["module_path"] = \
            self._tempfile_name

    @property
    def json_path(self):
        return self._dump_filepath

    @property
    def call(self):
        if not hasattr(self, "_call"):
            raise RescObjectAttributeError(
                "call must be used in 'with' statement.")
        return self._call

    @property
    def func_or_not(self):
        if hasattr(self, "func_source"):
            return True
        else:
            return False

    def import_module(self):
        if hasattr(self, "_tempfp") and \
                hasattr(self, "_call") and self.func_or_not:
            return
        RescObject._hashmodule[self.hash] = dict()
        self.create_module()
        self._syspath_append()
        __module_name = os.path.basename(
            self._tempfile_name
        ).split(".")[0]
        try:
            __spec = importlib.util.spec_from_file_location(
                __module_name,
                self._tempfile_name
            )
            __module = importlib.util.module_from_spec(__spec)
            __spec.loader.exec_module(__module)
        except IndentationError as e:
            raise RescObjectIndentationError(e)
        except ImportError as e:
            raise RescObjectImportError(e)
        except SyntaxError as e:
            raise RescObjectSyntaxError(e)
        except AttributeError as e:
            raise RescObjectAttributeError(e)

        __syspath = os.path.dirname(self._tempfile_name)

        self._syspath = __syspath
        self._module = __module
        if self.func_or_not:
            try:
                __func = getattr(__module, self.func_name)
                if not callable(__func):
                    raise RescObjectTypeError(
                        "__func must be function type."
                    )
            except AttributeError as e:
                raise RescObjectAttributeError(e)
            self._call = __func
            RescObject._hashmodule[self.hash].update({
                "module": __module,
                "module_name": __module_name,
                "syspath": __syspath,
                "func": __func,
            })
        else:
            self._call = self.import_module
            RescObject._hashmodule[self.hash].update({
                "module": __module,
                "module_name": __module_name,
                "syspath": __syspath,
            })

    def close(self):
        if not hasattr(self, "_tempfp") or \
                not hasattr(self, "_call"):
            raise RescObjectAttributeError(
                "not found tempfile name"
            )
        self._tempfp.close()
        del self._tempfp
        del self._tempfile_name
        del self._syspath
        del self._module
        del self._call

        self._syspath_remove()
        self.__class__._delete_module(self.hash)

    @property
    def hasmodule(self):
        if hasattr(self, "_tempfp"):
            return True
        else:
            return False

    def create_module(self):
        if self.func_or_not:
            self._create_module(self.func_source)
        else:
            self._tempfile_name = os.path.abspath(
                self.exec_file
            )
        return self._tempfile_name

    @staticmethod
    def _delete_module(hash_value):
        if hash_value not in RescObject._hashmodule.keys():
            raise RescObjectAttributeError(
                f"RescObject not save data of hash({hash_value})."
            )
        os.remove(RescObject._hashmodule[hash_value]["module_path"])
        del RescObject._hashmodule[hash_value]

    def delete(self):
        """
        delete from crontab and rescjson file.
        """
        if self.hash not in RescObject._hashmodule.keys():
            raise RescObjectAttributeError(
                f"RescObject not save data of hash({self.hash})."
            )
        self._jdelete(self.hash)
        Cron.crondelete(self.crontab_line)
        return self.crontab_line

    @staticmethod
    def sdelete(hash_value, dump_filepath):
        """
        delete from crontab and rescjson file.
        """
        if hash_value not in RescObject._hashmodule.keys():
            raise RescObjectAttributeError(
                f"RescObject not save data of hash({hash_value})."
            )
        element = RescObject.jdelete(hah_value, _dump_filepath)
        if element is None:
            raise RescObjectValueError(
                "not found crontab line with hash value."
            )
        Cron.crondelete(element["crontab_line"])
        return element["crontab_line"]

    @staticmethod
    def jdelete(
        hash_value,
        dump_filepath,
    ):
        elements = list()
        result = None
        for element in RescJSON._iter(dump_filepath):
            if element["hash"] != hash_value:
                elements.append(element)
            else:
                result = element
        RescJSON.jdump(dump_filepath,elements)
        return result

    def _jdelete(
        self,
        hash_value
    ):
        elements = [ x for x in self
            if x["hash"] != hash_value ]
        self.jdump(self._dump_filepath,elements)

    def _syspath_append(self):
        if not hasattr(self, "_tempfile_name"):
            raise RescObjectAttributeError(
                "not found tempfile name"
            )
        sys.path.append(
            os.path.dirname(self._tempfile_name)
        )

    def _syspath_remove(self):
        if self.hash not in RescObject._hashmodule.keys():
            raise RescObjectKeyError(
                f"{self.hash} value not found in _hashmodule's key"
            )
        if "syspath" not in RescObject._hashmodule[self.hash]:
            raise RescObjectKeyError(
                f"RescObject's _hashmodule ({self.hash}) not have \"syspath\" key"
            )
        sys.path.remove(RescObject._hashmodule[self.hash]["syspath"])

    def __call__(self):
        return self._jdict

    @property
    def json(self):
        return self.__call__()

    @staticmethod
    def limit_update(
        hash_value,
        dump_filepath,
    ):
        elements = RescJSON._iter(dump_filepath)
        result = False
        for ele in elements:
            if ele["hash"] == hash_value:
                ele["limit"] -= 1
            if ele["limit"] == 0:
                result = True
                if ele["permanent"] is True:
                    ele["limit"] = ele["limit_init"]
                else:
                    RescObject.sdelete(
                        hash_value,
                        dump_filepath,
                    )
        RescJSON.jdump(dump_filepath, list(elements))
        return result

    @staticmethod
    def exist_samescript(
        filepath,
        dump_filepath
    ):
        if os.path.isfile(dump_filepath):
            elements = RescJSON._iter(dump_filepath)
            for ele in elements:
                if "exec_file" in ele.keys() and ele["exec_file"] == filepath:
                    return True
        return False

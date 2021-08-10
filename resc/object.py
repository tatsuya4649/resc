import sys
import os
import tempfile
import importlib
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


class RescObject(RescJSON):
    def __new__(
        cls,
        dump_filepath,
        compiled_file,
        crontab_line,
        register_file,
        function,
        limit,
        permanent,
        log_file=None,
    ):
        if not hasattr(cls, "_hashmodule"):
            cls._hashmodule = dict()
        self = super().__new__(
            cls,
            dump_filepath=dump_filepath,
            compiled_file=compiled_file,
            crontab_line=crontab_line,
            register_file=register_file,
            function=function,
            limit=limit,
            permanent=permanent,
            log_file=log_file,
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
        register_file,
        function,
        limit,
        permanent,
        log_file=None,
    ):
        super().__init__(
            dump_filepath,
            compiled_file,
            crontab_line,
            register_file,
            function,
            limit,
            permanent,
            log_file=None,
        )
        self.import_module()

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
        RescObject._hashmodule[self.hash] = dict()
        RescObject._hashmodule[self.hash]["module_path"] = \
            self._tempfile_name

    @property
    def call(self):
        if not hasattr(self, "_call"):
            raise RescObjectAttributeError(
                "call must be used in 'with' statement.")
        return self._call

    def import_module(self):
        if hasattr(self, "_tempfp") and \
                hasattr(self, "_call"):
                return
        self._create_module(self.func_source)
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
        except ImportError as e:
            raise RescObjectImportError(e)
        try:
            __func = getattr(__module, self.func_name)
            if not callable(__func):
                raise RescObjectTypeError(
                    "__func must be function type."
                )
        except AttributeError as e:
            raise RescObjectAttributeError(e)

        __syspath = os.path.dirname(self._tempfile_name)

        RescObject._hashmodule[self.hash].update({
            "module": __module,
            "module_name": __module_name,
            "syspath": __syspath,
            "func": __func,
        })
        self._syspath = __syspath
        self._module = __module
        self._call = __func

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
        self._create_module(self.func_source)
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

    @property
    def json(self):
        return super().__call__()

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
        RescJSON.jdump(dump_filepath, elements)
        return result
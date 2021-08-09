import sys
import os
import tempfile
import importlib
import inspect
from .json import RescJSON


class RescObjectTypeError(TypeError):
    pass


class RescObjectKeyError(KeyError):
    pass


class RescObjectImportError(ImportError):
    pass


class RescObjectAttributeError(ImportError):
    pass


class RescObject:
    def __new__(
        cls,
        jresc,
    ):
        if not hasattr(cls, "_hashmodule"):
            cls._hashmodule = dict()
        if not isinstance(jresc, RescJSON):
            raise RescObjectTypeError(
                "jresc must be RescJSON type."
            )
        self = super().__new__(cls)
        if not hasattr(jresc, "hash"):
            raise RescObjectKeyError(
                "jresc must have hash key."
            )
        self._hash = jresc.hash
        return self

    def __init__(
        self,
        jresc,
    ):
        self._jresc = jresc

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
        self._tempfp.write(source.encode("utf-8"))
        self._tempfp.seek(0)
        RescObject._hashmodule[self._jresc.hash] = dict()
        RescObject._hashmodule[self._jresc.hash]["module_path"] = \
            self._tempfile_name

    @property
    def call(self):
        if not hasattr(self, "_call"):
            raise RescObjectAttributeError(
                "call must be used in 'with' statement.")
        return self._call

    def import_module(self):
        self._create_module(self._jresc.func_source)
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
            __func = getattr(__module, self._jresc.func_name)
            if not callable(__func):
                raise RescObjectTypeError(
                    "__func must be function type."
                )
        except AttributeError as e:
            raise RescObjectAttributeError(e)

        __syspath = os.path.dirname(self._tempfile_name)

        RescObject._hashmodule[self._jresc.hash].update({
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
        self.__class__._delete_module(self._jresc.hash)

    @property
    def hasmodule(self):
        if hasattr(self, "_tempfp"):
            return True
        else:
            return False

    def create_module(self):
        self._create_module(self._jresc.func_source)
        return self._tempfile_name

    @staticmethod
    def _delete_module(hash_value):
        if hash_value not in RescObject._hashmodule.keys():
            raise RescObjectAttributeError(
                f"RescObject not save data of hash({hash_value})."
            )
        os.remove(RescObject._hashmodule[hash_value]["module_path"])
        del RescObject._hashmodule[hash_value]

    def _syspath_append(self):
        if not hasattr(self, "_tempfile_name"):
            raise RescObjectAttributeError(
                "not found tempfile name"
            )
        sys.path.append(
            os.path.dirname(self._tempfile_name)
        )

    def _syspath_remove(self):
        if self._hash not in RescObject._hashmodule.keys():
            raise RescObjectKeyError(
                f"{self._hash} value not found in _hashmodule's key"
            )
        if "syspath" not in RescObject._hashmodule[self._hash]:
            raise RescObjectKeyError(
                f"RescObject's _hashmodule ({self._hash}) not have \"syspath\" key"
            )
        sys.path.remove(RescObject._hashmodule[self._hash]["syspath"])

    @property
    def json(self):
        return self._jresc

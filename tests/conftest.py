"""
Common Definition of test
"""
import sys
import os
import re
import pytest
import subprocess
from .docker_setup import RemoteHost
from resc import *
import tempfile
import shutil


class _RemoteSingleton:
    def __new__(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self):
        ...
    def __call__(self):
        if self._instance is not None:
            self._instance = None
            return True
        else:
            return False

@pytest.fixture(scope="session",autouse=True)
def _remote_singleton():
    _rsingleton = _RemoteSingleton()
    yield _rsingleton

@pytest.fixture(scope="session",autouse=False)
def _remote_init():
    remote_host = RemoteHost()
    yield remote_host

    # If use remote host, shutdown at end of test
    if remote_host.use:
        remote_host.shutdown()

@pytest.fixture(scope="module",autouse=False)
def setup_remote_host(_remote_singleton,_remote_init):
    """
    setup and shutdown of Remote Host(made using Docker)
    """
    if _remote_singleton():
        _remote_init.startup()
        yield _remote_init
    else:
        yield

_KEY_PATH = \
    os.path.join(
        os.path.dirname(
            os.path.abspath(
                __file__
            )
        ),
        'test_data/test_resc'
    )

_TEST_LOGFILE = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "test_data/output"
    )
)

def _cronlist():
    process = subprocess.Popen(
        "command crontab -l",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        shell=True,
    )
    stderr = process.stderr.read()
    if process.wait() != 0 and \
        re.match(
            r"^no crontab",
            stderr,
        ) is None:
        sys.exit(1)
    return process

def _crondelete():
    process = subprocess.Popen(
        "command crontab -r",
        stderr=subprocess.PIPE,
        universal_newlines=True,
        shell=True,
    )
    stderr = process.stderr.read()
    if process.wait() != 0 and \
        re.match(
            r"^no crontab",
            stderr,
        ) is None:
        sys.exit(1)
    return process

def _cronregister(register):
    if len(register) == 0:
        return
    process = subprocess.Popen(
        "command crontab",
        stdin = subprocess.PIPE,
        shell=True,
    )
    process.communicate(
        input=register.encode("utf-8"),
        timeout=5,
    )
    if process.wait() != 0:
        sys.exit(1)
    return process


@pytest.fixture(scope="function",autouse=False)
def cron_empty():
    process = _cronlist()
    crontab_list = process.stdout.read()
    _crondelete()
    yield
    _crondelete()
    _cronregister(crontab_list)

@pytest.fixture(scope="function",autouse=False)
def cron_noempty():
    _LINE = "* * * * * echo 'Hello World'\n"
    process = _cronlist()
    crontab_list = process.stdout.read()
    _crondelete()
    _cronregister(_LINE)
    yield _LINE
    _crondelete()
    _cronregister(crontab_list)

_EXREG = "* * * * * resc --help\n"
class _RegDir:
    def __new__(cls, path):
        if not hasattr(cls, "_alldir"):
            cls._alldir = list()
        return super().__new__(cls)
    def __init__(self, path):
        self._target = path
        self._paths = list()
        self._makepaths = list()
    def __enter__(
        self
    ):
        for path in os.path.dirname(
            self._target
        ).split('/'):
            self._paths.append(path)
            dire = "/".join(self._paths)
            if not os.path.isdir(dire) and \
            len(dire) > 0:
                os.mkdir(dire)
                self._makepaths.append(dire)
                _RegDir._alldir.append(dire)
        return self
    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        for dire in reversed(self._makepaths):
            if os.path.isdir(dire) and \
                len(os.listdir(dire)) == 0:
                os.rmdir(dire)
                if not os.path.isdir(dire):
                    _RegDir._alldir.remove(dire)

@pytest.fixture(scope="function",autouse=False)
def register_empty():
    with _RegDir(Resc._REGIPATH):
        prereg_em = None
        if os.path.isfile(Resc._REGIPATH):
            with open(Resc._REGIPATH,"r") as f:
                prereg_em = f.read()
            with open(Resc._REGIPATH,"w") as f:
                f.truncate(0)
        yield

        if (prereg_em is None or len(prereg_em) == 0) and \
            os.path.isfile(Resc._REGIPATH):
            os.remove(Resc._REGIPATH)
        else:
            if (prereg_em is not None and len(prereg_em) > 0):
                with open(Resc._REGIPATH,"w") as f:
                    f.write(prereg_em)

@pytest.fixture(scope="function",autouse=False)
def register_noempty():
    with _RegDir(Resc._REGIPATH):
        prereg_ne = None
        if os.path.isfile(Resc._REGIPATH):
            with open(Resc._REGIPATH,"r") as f:
                prereg_ne = f.read()
            with open(Resc._REGIPATH,"w") as f:
                f.truncate(0)
        with open(Resc._REGIPATH,"w") as f:
            f.write(_EXREG)
        yield
        with open(Resc._REGIPATH,"w") as f:
            f.truncate(0)

        if (prereg_ne is None or len(prereg_ne) == 0) and \
            os.path.isfile(Resc._REGIPATH):
            os.remove(Resc._REGIPATH)
        else:
            if (prereg_ne is not None and len(prereg_ne) > 0):
                with open(Resc._REGIPATH,"w") as f:
                    f.write(prereg_ne)

# pass of resc dir
_RESCDIR = "test/rescs"
_RESCDIR_FULL = os.path.join(
    Resc._RESCDIR_PATH,
    _RESCDIR
)
# pass of resc log
_OUTPUT = "test_output"
_OUTPUT_FULL = os.path.join(
    Resc._RESCLOG_PATH,
    _OUTPUT
)

@pytest.fixture(scope="function", autouse=False)
def rescjson_undo():
    with _RegDir(Resc._RESCJSONPATH):
        prejson = None
        if os.path.isfile(Resc._RESCJSONPATH):
            with open(Resc._RESCJSONPATH, "r") as f:
                prejson = f.read()
        yield
        if (prejson is None or len(prejson) == 0) and \
            os.path.isfile(Resc._RESCJSONPATH):
            os.remove(Resc._RESCJSONPATH)
        else:
            if (prejson is not None and len(prejson) > 0):
                with open(Resc._RESCJSONPATH,"w") as f:
                    f.write(prejson)

@pytest.fixture(scope="function", autouse=False)
def register_undo():
    with _RegDir(Resc._REGIPATH):
        preregu = None
        if os.path.isfile(Resc._REGIPATH):
            with open(Resc._REGIPATH, "r") as f:
                preregu = f.read()
        yield
        if (preregu is None or len(preregu) == 0) and \
            os.path.isfile(Resc._REGIPATH):
            os.remove(Resc._REGIPATH)
        else:
            if (preregu is not None and len(preregu) > 0):
                with open(Resc._REGIPATH,"w") as f:
                    f.write(preregu)


@pytest.fixture(scope="function", autouse=False)
def temp_logdir():
    direxists = False
    logdir = os.path.dirname(_OUTPUT_FULL)
    with tempfile.TemporaryDirectory(
        prefix="tmp_test_log_"
    ) as dirpath:
        if os.path.exists(logdir):
            direxists = True
            tmp_dir = shutil.move(logdir, dirpath)
        yield
        if os.path.exists(logdir):
            for file in os.listdir(logdir):
                os.remove(
                    os.path.join(
                        logdir,
                        file
                    )
                )
            os.rmdir(logdir)

        if direxists:
            shutil.move(
                tmp_dir,
                logdir
            )

@pytest.fixture(scope="function", autouse=False)
def log_undo(temp_logdir):
    with _RegDir(_OUTPUT_FULL):
        logdir = os.path.dirname(_OUTPUT_FULL)
        with _RegDir(logdir):
            prelogs = None
            if os.path.isdir(logdir):
                predfiles = os.listdir(logdir)
            prelog = None
            if os.path.isfile(_OUTPUT_FULL):
                with open(_OUTPUT_FULL, "r") as f:
                    prelog = f.read()
            yield
            if prelogs is not None or \
                    os.path.isdir(logdir):
                for path in os.listdir(logdir):
                    if prelogs is None or \
                            path not in prelogs:
                        if os.path.isdir(
                            os.path.join(
                                logdir,
                                path
                            )
                        ):
                            shutil.rmtree(
                                os.path.join(
                                    logdir,
                                    path
                                )
                            )
                        elif os.path.isfile(
                            os.path.join(
                                logdir,
                                path
                            )
                        ):
                            os.remove(
                                os.path.join(
                                    logdir,
                                    path
                                )
                            )
            if (prelog is None or len(prelog) == 0) and \
                os.path.isfile(_OUTPUT_FULL):
                os.remove(_OUTPUT_FULL)
            else:
                if (prelog is not None and len(prelog) > 0):
                    with open(_OUTPUT_FULL,"w") as f:
                        f.write(prelog)

@pytest.fixture(scope="function", autouse=False)
def resc_default_undo():
    with _RegDir(Resc._RESCDIR_DEFAULT):
        predfiles = None
        if os.path.isdir(Resc._RESCDIR_DEFAULT):
            predfiles = os.listdir(Resc._RESCDIR_DEFAULT)
        yield
        if predfiles is not None or \
                os.path.isdir(Resc._RESCDIR_DEFAULT):
            for path in os.listdir(Resc._RESCDIR_DEFAULT):
                if predfiles is None or \
                        path not in predfiles:
                    if os.path.isdir(
                        os.path.join(
                            Resc._RESCDIR_DEFAULT,
                            path
                        )
                    ):
                        shutil.rmtree(
                            os.path.join(
                                Resc._RESCDIR_DEFAULT,
                                path
                            )
                        )
                    elif os.path.isfile(
                        os.path.join(
                            Resc._RESCDIR_DEFAULT,
                            path
                        )
                    ):
                        os.remove(
                            os.path.join(
                                Resc._RESCDIR_DEFAULT,
                                path
                            )
                        )

@pytest.fixture(scope="function", autouse=False)
def temp_rescdir():
    direxists = False
    with tempfile.TemporaryDirectory(
        prefix="tmp_test_resc_"
    ) as dirpath:
        if os.path.exists(_RESCDIR_FULL):
            direxists = True
            tmp_dir = shutil.move(_RESCDIR_FULL, dirpath)
        yield
        if os.path.exists(_RESCDIR_FULL):
            for file in os.listdir(_RESCDIR_FULL):
                if os.path.isdir(file):
                    shutil.rmtree(
                        os.path.join(
                            _RESCDIR_FULL,
                            file
                        )
                    )
                else:
                    os.remove(
                        os.path.join(
                            _RESCDIR_FULL,
                            file
                        )
                    )
            shutil.rmtree(_RESCDIR_FULL)

        if direxists:
            shutil.move(
                tmp_dir,
                os.path.dirname(_RESCDIR_FULL)
            )

@pytest.fixture(scope="function", autouse=False)
def resc_undo(resc_default_undo, temp_rescdir):
    with _RegDir(_RESCDIR_FULL):
        prefiles = None
        if os.path.isdir(_RESCDIR_FULL):
            prefiles = os.listdir(_RESCDIR_FULL)
        yield
        if prefiles is not None or \
                    os.path.isdir(Resc._RESCDIR_DEFAULT):
            for path in os.listdir(Resc._RESCDIR_DEFAULT):
                if prefiles is None or \
                        path not in prefiles:
                    if os.path.isdir(
                        os.path.join(
                            _RESCDIR_FULL,
                            path
                        )
                    ):
                        shutil.rmtree(
                            os.path.join(
                                _RESCDIR_FULL,
                                path
                            )
                        )
                    elif os.path.isfile(
                        os.path.join(
                            _RESCDIR_FULL,
                            path
                        )
                    ):
                        os.remove(
                            os.path.join(
                                _RESCDIR_FULL,
                                path
                            )
                        )



@pytest.fixture(scope="function", autouse=False)
def crontab_undo():
    process = _cronlist()
    crontab_list = process.stdout.read()
    yield
    _crondelete()
    _cronregister(crontab_list)

@pytest.fixture(scope="session",autouse=False)
def final_delete():
    yield
    length = len(_RegDir("")._alldir)
    i = 0
    while True:
        for d in sorted(_RegDir("")._alldir, reverse=False):
            if os.path.isdir(d) and \
                len(os.listdir(d)) == 0:
                os.rmdir(d)
                _RegDir("")._alldir.remove(d)
                i = 0
        if len(_RegDir("")._alldir) == 0 or \
                i > length:
            break
        i += 1

@pytest.fixture(scope="function",autouse=False)
def register_undos(
    final_delete,
    crontab_undo,
    resc_undo,
    log_undo,
    register_undo,
    rescjson_undo,
):
    yield

    try:
        os.removedirs(
            Resc._RESCDIR_PATH
        )
    except Exception as e:
        print(e)

@pytest.fixture(scope="function", autouse=False)
def register_env():
    os.environ[Resc._RESCDIR_ENV] = _RESCDIR
    yield
    os.environ.pop(Resc._RESCDIR_ENV, None)

@pytest.fixture(scope="function",autouse=False)
def same_cron_register():
    with _RegDir(Resc._REGIPATH):
        # Register file only _EXREG
        prereg_s = None
        if os.path.isfile(Resc._REGIPATH):
            with open(Resc._REGIPATH,"r") as f:
                prereg_s = f.read()
            with open(Resc._REGIPATH,"w") as f:
                f.truncate(0)
        with open(Resc._REGIPATH,"w") as f:
            f.write(_EXREG)
        # Crontab only _EXREG
        process = _cronlist()
        crontab_list = process.stdout.read()
        _crondelete()
        _cronregister(_EXREG)
        yield
        # Undo
        _crondelete()
        _cronregister(crontab_list)

        with open(Resc._REGIPATH,"w") as f:
            f.truncate(0)
        if prereg_s is None or len(prereg_s) == 0 and \
            os.path.isfile(Resc._REGIPATH):
            os.remove(Resc._REGIPATH)
        else:
            with open(Resc._REGIPATH,"w") as f:
                f.write(prereg_s)

@pytest.fixture(scope="function",autouse=False)
def logfile_empty():
    with _RegDir(_TEST_LOGFILE):
        _logcontent = None
        if os.path.isfile(_TEST_LOGFILE):
            with open(_TEST_LOGFILE,"rb") as f:
                _logcontent = f.read()
            with open(_TEST_LOGFILE,"wb") as f:
                f.truncate(0)
        yield _TEST_LOGFILE

        if (_logcontent is None  is None or len(_logcontent) == 0) \
            and os.path.isfile(_TEST_LOGFILE):
            os.remove(_TEST_LOGFILE)
        else:
            with open(_TEST_LOGFILE,"wb") as f:
                f.write(_logcontent)

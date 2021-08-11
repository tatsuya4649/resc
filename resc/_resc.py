from .cpu import CPUDetect
from .memory import MemoryDetect
from .disk import DiskDetect
from .net import NetDetect
from .ps import PSDetect
from .file import FileDetect
from .cron import Cron, CronCommandError
from .resclog.header import RescLogSFlag, RescLogFlag
from .object import RescObject
from .ssh import SSH
from .rescerr import RescTypeError, RescKeyError, RescCronError, \
    RescValueError, RescServerError, RescExistError
from .resclog import RescLog
from .compile import RescCompile
import resc
import inspect
import hashlib
import os
import pathlib
import re
import sys
import subprocess
from jinja2 import Environment, FileSystemLoader


def _resc_init(
    **kwargs
):
    cpu = None if "cpu" not in kwargs.keys() else kwargs["cpu"]
    memory = None if "memory" not in kwargs.keys() else kwargs["memory"]
    disk = None if "disk" not in kwargs.keys() else kwargs["disk"]
    net = None if "net" not in kwargs.keys() else kwargs["net"]
    return Resc(
        cpu=cpu,
        memory=memory,
        disk=disk,
        net=net,
    )


def register(
    trigger,
    **kwargs,
):
    """
    register decorated function to crontab and resource check script.
    namespace of decorated function must be independent,
    because it be executed in cron independently.

    params:
    @trigger           : Format of crontab. Specify interval of check resource.
    @rescdir    (=None): Compiled file path to be placed. ("~/.resc/" + rescdir)
    @outputfile (=None): Log file path to be placed. ("~/.resc/log" + outputfile)
    @ip         (=None): IP Address of resources be checked.
    @username   (=None): Username that of host of IP Address. (used in SSH)
    @password   (=None): Password that of host of IP Address. (used in SSH)
    @key_path   (=None): Key path file used for key authentication for SSH to communicate with host of IP Address.
    @port       (=22): Port number used in SSH.
    @timeout    (=5): Connection timeout used in SSH.
    @format     (=None): Log format. (detail are shown in `RescLogFormat class`.)
    @call_first (=False): Call now body of this function without resource check?
    @quiet      (=False): Without output of path name of compiled, log.
    @limit      (=1): How many times a resource threshold is exceeded before executing decorated function.
    @permanent  (=True): If False, delete crontab line(registered in this) when a resource threshold once exceeded
    @reverse    (=False): If it doesn't exceed threshold, execute.

    return:
        RescObject
    
    example:
        from resc import register

        @register(
            trigger="* * * * *",
        )
        def test():
            print("Hello World")
        
        result = test()
        print(type(result))     # <class 'resc.object.RescObject'>
    """
    _resc = _resc_init(**kwargs)
    return _resc.register(
        trigger,
        **kwargs
    )


def register_file(
    exec_file,
    trigger,
    **kwargs,
):
    """
    register .py script to crontab and resource check script.
    your registered file(exec_file params) will be executed every specified trigger time(trigger params).

    params:
    @exec_file         : If a resource exceeded, @exec_file will be executed.
    @trigger           : Format of crontab. Specify interval of check resource.
    @rescdir    (=None): Compiled file path to be placed. ("~/.resc/" + rescdir)
    @outputfile (=None): Log file path to be placed. ("~/.resc/log" + outputfile)
    @ip         (=None): IP Address of resources be checked.
    @username   (=None): Username that of host of IP Address. (used in SSH)
    @password   (=None): Password that of host of IP Address. (used in SSH)
    @key_path   (=None): Key path file used for key authentication for SSH to communicate with host of IP Address.
    @port       (=22): Port number used in SSH.
    @timeout    (=5): Connection timeout used in SSH.
    @format     (=None): Log format. (detail are shown in `RescLogFormat class`.)
    @call_first (=False): Call now body of this function without resource check?
    @quiet      (=False): Without output of path name of compiled, log.
    @limit      (=1): How many times a resource threshold is exceeded before executing decorated function.
    @permanent  (=True): If False, delete crontab line(registered in this) when a resource threshold once exceeded
    @reverse    (=False): If it doesn't exceed threshold, execute.
    @exist_ok   (=False): If there is a same file in registered crontab, raise error.

    return:
        RescObject

    example:
        from resc import register_file

        result = register_file(
            exec_file="./exec.py"
            trigger="* * * * *",
        )
        print(type(result))     # <class 'resc.object.RescObject'>
    """
    _resc = _resc_init(**kwargs)
    return _resc.register_file(
        exec_file,
        trigger,
        **kwargs
    )


class Resc:
    """
    """
    _RESCDIR_ENV = "RESCDIR"
    _RESCDIR_PATH = os.path.join(
        os.path.expanduser("~"),
        ".resc"
     )
    _RESCDIR_DEFAULT = os.path.join(
        _RESCDIR_PATH,
        "resc"
    )
    _RESCLOG_PATH = os.path.join(
        os.path.expanduser("~"),
        ".resc/log"
     )
    _REGIPATH = os.path.join(
            _RESCDIR_PATH,
            "register"
    )
    _RESCJSONPATH = os.path.join(
            _RESCDIR_PATH,
            "resc.ndjson"
    )
    _RESCOUTPUT_ENV = "RESCOUTPUT"
    _SERVER_SCRIPT = "server.sh"

    def _cpu_check(self, cpu):
        if cpu is not None and not isinstance(cpu, dict):
            raise RescTypeError("cpu must be None or dict.")
        elif cpu is not None:
            cpu_detect_keys = [
                k for k, v in
                inspect
                .signature(CPUDetect.__init__)
                .parameters
                .items()
            ]
            unexpected_keys = [
                x for x in cpu.keys()
                if x not in cpu_detect_keys
            ]
            if len(unexpected_keys) > 0:
                raise RescKeyError(
                    f"cpu must have only {cpu_detect_keys} key."
                    f"unexpected keys ({unexpected_keys})."
                )

        if cpu is not None:
            cpu_string = str()
            for x in cpu.keys():
                if isinstance(cpu[x], str):
                    cpu_string += f"{x}=\"{cpu[x]}\","
                else:
                    cpu_string += f"{x}={cpu[x]},"
            self._cpu = eval(f'CPUDetect({cpu_string})')
        else:
            self._cpu = None

    def _memory_check(self, memory):
        if memory is not None and not isinstance(memory, dict):
            raise RescTypeError("memory must be None or dict.")
        elif memory is not None:
            memory_detect_keys = [
                k for k, v in
                inspect
                .signature(MemoryDetect.__init__)
                .parameters
                .items()
            ]
            unexpected_keys = [
                x for x in memory.keys()
                if x not in memory_detect_keys
            ]
            if len(unexpected_keys) > 0:
                raise RescKeyError(
                    f"memory must have only {memory_detect_keys} key."
                    f"unexpected keys ({unexpected_keys})."
                )
        if memory is not None:
            memory_string = str()
            for x in memory.keys():
                if isinstance(memory[x], str):
                    memory_string += f"{x}=\"{memory[x]}\","
                else:
                    memory_string += f"{x}={memory[x]},"
            self._memory = eval(f'MemoryDetect({memory_string})')
        else:
            self._memory = None
    
    def _disk_check(self, disk):
        if disk is not None and not isinstance(disk, dict):
            raise RescTypeError("disk must be None or dict.")
        elif disk is not None:
            disk_detect_keys = [
                k for k, v in
                inspect
                .signature(DiskDetect.__init__)
                .parameters
                .items()
            ]
            unexpected_keys = [
                x for x in disk.keys()
                if x not in disk_detect_keys
            ]
            if len(unexpected_keys) > 0:
                raise RescKeyError(
                    f"disk must have only {disk_detect_keys} key."
                    f"unexpected keys ({unexpected_keys})."
                )
        if disk is not None:
            disk_string = str()
            for x in disk.keys():
                if isinstance(disk[x], str):
                    disk_string += f"{x}=\"{disk[x]}\","
                else:
                    disk_string += f"{x}={disk[x]},"
            self._disk = eval(f'DiskDetect({disk_string})')
        else:
            self._disk = None

    
    def _net_check(self, net):
        if net is not None and not isinstance(net, dict):
            raise RescTypeError("net must be None or dict.")
        elif net is not None:
            net_detect_keys = [
                k for k, v in
                inspect
                .signature(NetDetect.__init__)
                .parameters
                .items()
            ]
            unexpected_keys = [
                x for x in net.keys()
                if x not in net_detect_keys
            ]
            if len(unexpected_keys) > 0:
                raise RescKeyError(
                    f"net must have only {net_detect_keys} key."
                    f"unexpected keys ({unexpected_keys})."
                )
        if net is not None:
            net_string = str()
            for x in net.keys():
                if isinstance(net[x], str):
                    net_string += f"{x}=\"{net[x]}\","
                else:
                    net_string += f"{x}={net[x]},"
            self._net = eval(f'NetDetect({net_string})')
        else:
            self._net = None

    
    def _ps_check(self, ps):
        if ps is not None and not isinstance(ps, dict):
            raise RescTypeError("ps must be None or dict.")
        elif ps is not None:
            ps_detect_keys = [
                k for k, v in
                inspect
                .signature(PSDetect.__init__)
                .parameters
                .items()
            ]
            unexpected_keys = [
                x for x in ps.keys()
                if x not in ps_detect_keys
            ]
            if len(unexpected_keys) > 0:
                raise RescKeyError(
                    f"ps must have only {ps_detect_keys} key."
                    f"unexpected keys ({unexpected_keys})."
                )
        if ps is not None:
            ps_string = str()
            for x in ps.keys():
                if isinstance(ps[x], str):
                    ps_string += f"{x}=\"{ps[x]}\","
                else:
                    ps_string += f"{x}={ps[x]},"
            self._ps = eval(f'PSDetect({ps_string})')
        else:
            self._ps = None

    def _file_check(self, file):
        if file is not None and not isinstance(file, dict):
            raise RescTypeError("file must be None or dict.")
        elif file is not None:
            file_detect_keys = [
                k for k, v in
                inspect
                .signature(FileDetect.__init__)
                .parameters
                .items()
            ]
            unexpected_keys = [
                x for x in file.keys()
                if x not in file_detect_keys
            ]
            if len(unexpected_keys) > 0:
                raise RescKeyError(
                    f"file must have only {file_detect_keys} key."
                    f"unexpected keys ({unexpected_keys})."
                )
        if file is not None:
            file_string = str()
            for x in file.keys():
                if isinstance(file[x], str):
                    file_string += f"{x}=\"{file[x]}\","
                else:
                    file_string += f"{x}={file[x]},"
            self._file = eval(f'FileDetect({file_string})')
        else:
            self._file = None

    def __init__(
        self,
        cpu=None,
        memory=None,
        disk=None,
        net=None,
        ps=None,
        file=None,
    ):
        self._cpu_dict = cpu
        self._memory_dict = memory
        self._disk_dict = disk
        self._net_dict = net
        self._ps_dict = ps

        self._cpu_check(cpu)
        self._memory_check(memory)
        self._disk_check(disk)
        self._net_check(net)
        self._ps_check(ps)
        self._file_check(file)

        self._checkers = list()
        self._checkers.append(self._cpu)
        self._checkers.append(self._memory)
        self._checkers.append(self._disk)
        self._checkers.append(self._net)
        self._checkers.append(self._ps)
        self._checkers.append(self._file)
        self._checkers = [x for x in self._checkers if x is not None]
        self._crons = list()
        self._resclog = None

    @property
    def thresholds(self):
        retdic = dict()
        for x in self._checkers:
            retdic[x.resource] = {
                "threshold": x.threshold,
            }
        return retdic

    @property
    def checks(self):
        if not hasattr(self, "_checks") or self._checks is None:
            retdic = dict()
            for x in self._checkers:
                retdic[x.resource] = x.check
            self._checks = retdic
        return self._checks

    @property
    def over_one(self):
        return False in [v for k, v in self.checks.items()]

    @property
    def overs(self):
        resources = [k for k, v in self.checks.items() if v is False]
        overlist = list()
        for res in resources:
            for check in self._checkers:
                if check.resource == res:
                    overlist.append(check)
        return overlist

    @property
    def _check_command(self):
        return subprocess \
            .run("command", shell=True) \
            .returncode

    def _ip_type(self, ip):
        if not isinstance(ip, str):
            raise RescTypeError("IP Address must by str type.")
        return ip

    def _port_type(self, port):
        if not isinstance(port, int):
            raise RescTypeError("Port Number must by str type.")
        return port

    def _username_type(self, username):
        if not isinstance(username, str):
            raise RescTypeError("username must by str type.")
        return username

    def _password_type(self, password):
        if password is None:
            return password
        if not isinstance(password, str):
            raise RescTypeError("password must by str type.")
        return password

    def _key_path_type(self, key_path):
        if key_path is None:
            return key_path
        if not isinstance(key_path, str):
            raise RescTypeError("key_path must by str type.")
        key_path = re.sub(
            r'~',
            f"{os.path.expanduser('~')}",
            key_path,
        )
        return key_path

    def _timeout_type(self, timeout):
        if not isinstance(timeout, int):
            raise RescTypeError("timeout must by int type.")
        return timeout

    @property
    def quiet(self):
        if not hasattr(self, "_quiet"):
            return False
        return self._quiet

    @quiet.setter
    def quiet(self, value):
        if not isinstance(value, bool):
            raise RescTypeError(
                "quiet must be bool type."
            )
        self._quiet = value

    @property
    def limit(self):
        if not hasattr(self, "_limit"):
            return 1
        return self._limit
    
    @limit.setter
    def limit(self, value):
        if not isinstance(value, int) or value <= 0:
            raise RescTypeError(
                "limit must be int type and greater than zero."
            )
        self._limit = value

    @property
    def permanent(self):
        if not hasattr(self, "_permanent"):
            return True
        return self._permanent
    
    @permanent.setter
    def permanent(self, value):
        if not isinstance(value, bool):
            raise RescTypeError(
                "permanent must be bool type."
            )
        self._permanent = value

    @property
    def reverse(self):
        if not hasattr(self, "_reverse"):
                return False
        return self._reverse
    
    @reverse.setter
    def reverse(self, value):
        if not isinstance(value, bool):
            raise RescTypeError(
                "reverse must be bool type."
            )
        self._reverse = value
    
    def _register(
        self,
        trigger,
        rescdir=None,
        outputfile=None,
        format=None,
        call_first=False,
        quiet=False,
        limit=1,
        permanent=True,
        reverse=False
    ):
        self.quiet = quiet
        self.limit = limit
        self.permanent = permanent
        self.reverse = reverse

        if not Cron.available():
            raise CronCommandError(
                "not found crontab command. you must have crontab command."
            )
        if self._check_command != 0:
            raise RescCronError(
                ("not found command builtin command."
                 "you must have builtin command.")
            )
        self._call_first = call_first \
            if isinstance(call_first, bool) else False
        if rescdir is not None and isinstance(rescdir, str):
            os.environ[self._RESCDIR_ENV] = rescdir
        elif rescdir is not None and not isinstance(rescdir, str):
            raise RescTypeError("rescdir must be str type.")

        if outputfile is not None and isinstance(outputfile, str):
            os.environ[self._RESCOUTPUT_ENV] = outputfile
        elif outputfile is not None and not isinstance(outputfile, str):
            raise RescTypeError("outputfile must be str type.")

        if os.getenv(self._RESCDIR_ENV) is None:
            os.environ[self._RESCDIR_ENV] = self._RESCDIR_DEFAULT
        else:
            if rescdir is not None:
                os.environ[self._RESCDIR_ENV] = os.path.join(
                    self._RESCDIR_PATH,
                    rescdir
                )
            else:
                os.environ[self._RESCDIR_ENV] = os.path.join(
                    self._RESCDIR_PATH,
                    os.environ[self._RESCDIR_ENV]
                )

        if not isinstance(trigger, str):
            raise RescTypeError("trigger must be string type.")
        self._resclog = RescLog(
            logfile=None if os.getenv(self._RESCOUTPUT_ENV) is None else \
                    os.path.join(
                        self._RESCLOG_PATH,
                        os.getenv(self._RESCOUTPUT_ENV)
            ),
            format=format,
        )
        if self._resclog.logfile is not None:
            os.environ[self._RESCOUTPUT_ENV] = self._resclog.logfile

    def _remote_ssh(
        self,
        ip=None,
        port=22,
        username=None,
        password=None,
        key_path=None,
        timeout=5,
    ):
        if ip is not None and \
                username is not None and \
                (key_path is not None or password is not None):
            ssh = SSH(
                self._ip_type(ip),
                port=self._port_type(port),
                username=self._username_type(username),
                password=self._password_type(password),
                key_filename=self._key_path_type(key_path),
                timeout=self._timeout_type(timeout),
            )
            ssh.ssh_ping()
        else:
            ssh = None
        self._resclog._ssh = ssh
        if ip is not None:
            self._resclog.remo = ip
        return ssh
    
    def register_file(
        self,
        exec_file,
        trigger,
        rescdir=None,
        outputfile=None,
        ip=None,
        username=None,
        password=None,
        key_path=None,
        port=22,
        timeout=5,
        format=None,
        call_first=False,
        quiet=False,
        limit=1,
        permanent=True,
        reverse=False,
        exist_ok=False,
    ):
        self._register(
            trigger=trigger,
            rescdir=rescdir,
            outputfile=outputfile,
            format=format,
            call_first=call_first,
            quiet=quiet,
            limit=limit,
            permanent=permanent,
            reverse=reverse,
        )
        ssh = self._remote_ssh(
            ip=ip,
            port=port,
            username=username,
            password=password,
            key_path=key_path,
            timeout=timeout,
        )
        compiled_filename = self._sourcefile(
            filename=exec_file,
            ssh=ssh,
            exist_ok=exist_ok,
        )
        # Register crontable from trigger
        totalline = self._crons_get(trigger, compiled_filename)
        self._crons_register()

        return RescObject(
            dump_filepath=self._RESCJSONPATH,
            compiled_file=compiled_filename,
            crontab_line=totalline,
            register_file=self._REGIPATH,
            limit=self.limit,
            exec_file=os.path.abspath(exec_file),
            permanent=self.permanent,
            log_file=None,
        )

    def register(
        self,
        trigger,
        rescdir=None,
        outputfile=None,
        ip=None,
        username=None,
        password=None,
        key_path=None,
        port=22,
        timeout=5,
        format=None,
        call_first=False,
        quiet=False,
        limit=1,
        permanent=True,
        reverse=False
    ):
        self._register(
            trigger=trigger,
            rescdir=rescdir,
            outputfile=outputfile,
            format=format,
            call_first=call_first,
            quiet=quiet,
            limit=limit,
            permanent=permanent,
            reverse=reverse,
        )
        def _register_func(func):
            def _wrapper(*args, **kwargs):
                call_code = inspect.getsource(func.__code__)
                func_args = dict()
                func_args["args"] = args
                func_args["kwargs"] = kwargs

                ssh = self._remote_ssh(
                    ip=ip,
                    port=port,
                    username=username,
                    password=password,
                    key_path=key_path,
                    timeout=timeout
                )
                self._resclog.func = func.__name__

                compiled_filename = self._sourcefile(
                    func_source=call_code,
                    funcname=func.__name__,
                    func_args=func_args,
                    ssh=ssh,
                )

                # Register crontable from trigger
                totalline = self._crons_get(trigger, compiled_filename)
                self._crons_register()

                if self._call_first:
                    func(*args, **kwargs)
                
                return RescObject(
                    dump_filepath=self._RESCJSONPATH,
                    compiled_file=compiled_filename,
                    crontab_line=totalline,
                    register_file=self._REGIPATH,
                    function=func,
                    limit=self.limit,
                    permanent=self.permanent,
                    log_file=None,
                )

            return _wrapper
        return _register_func

    def _directory_make(self, dirpath):
        os.makedirs(dirpath,exist_ok=True)

    def _sourcefile(
        self,
        **kwargs
#        filename=None
#        funcname=None,
#        func=None,
#        func_args=None,
#        ssh=None
    ):
        if "filename" not in kwargs.keys() and "funcname" not in kwargs.keys():
            raise RescKeyError(
                "filename or function name must be passed."
            )
        filename = None if "filename" not in kwargs.keys() else kwargs["filename"]
        funcname = None if "funcname" not in kwargs.keys() else kwargs["funcname"]
        func_source = None if "func_source" not in kwargs.keys() else kwargs["func_source"]
        func_args = None if "func_args" not in kwargs.keys() else kwargs["func_args"]
        ssh = None if "ssh" not in kwargs.keys() else kwargs["ssh"]
        exist_ok = None if "exist_ok" not in kwargs.keys() else kwargs["exist_ok"]

        resc_dir = os.getenv(self._RESCDIR_ENV)
        i = 0
        self._directory_make(resc_dir)
        while True:
            resc_key = os.path.join(
                resc_dir,
                f"resc{i}.py"
            )
            hash_value = hashlib.md5(resc_key.encode('utf-8')).hexdigest()
            resc_filename = os.path.join(
                resc_dir,
                f"resc{hash_value}.py"
            )
            if not os.path.exists(resc_filename):
                return self._source_write(
                    resc_filename=resc_filename,
                    filename=filename,
                    func_source=func_source,
                    funcname=funcname,
                    func_args=func_args,
                    ssh=ssh,
                    exist_ok=exist_ok,
                )
            i += 1

    def _which_resc(self):
        cp = subprocess.run(
            "command which resc",
            encoding="utf-8",
            stdout=subprocess.PIPE,
            shell=True,
        )
        return cp.stdout

    def _crons_get(self, trigger, triggerscript):
        if os.getenv(self._RESCOUTPUT_ENV) is not None:
            output_path = f"{os.getenv(self._RESCOUTPUT_ENV)}"
            output = f' >>{output_path} 2>&1'
            self._directory_make(os.path.dirname(output_path))
        else:
            output_path = str()
            output = str()

        stdout = self._which_resc()
        which_resc = re.sub(r'\s*$', '', stdout)
        if len(which_resc) > 0:
            not_found = str()
            if len(output) > 0:
                not_found = f'{which_resc} --not_found \'{output_path}\''
            else:
                not_found = ':'
            totalline = (
                f'if ! [ -f {triggerscript} ]; '
                f'then {not_found}; '
                f'else command python3 {triggerscript} {output}; fi'
            )
            cron = Cron(
                command=totalline,
                interval_str=trigger,
                register_file=self._REGIPATH
            )
            if self._call_first and len(output_path) > 0:
                with open(output_path, "wb") as fp:
                    subprocess.run(
                        f"command python3 {triggerscript}",
                        stdout=fp,
                        stderr=fp,
                        shell=True,
                    )
            self._crons.append(cron)
            return totalline
        else:
            print(
                (
                    "resc command not found. "
                    "required in crontab."
                ), file=sys.stderr)
            if os.path.isfile(triggerscript):
                os.remove(triggerscript)
            sys.exit([1, "resc command not found"])

    def _crons_register(self):
        if not isinstance(self._crons, list):
            raise RescTypeError("_crons must be list.")
        if len(self._crons) == 0:
            return
        # register directive into crontable
        for cron in self._crons:
            cron.register()

    def _source_write(
        self,
        resc_filename,
        **kwargs,
    ):
        filename = None if "filename" not in kwargs.keys() else kwargs["filename"]
        funcname = None if "funcname" not in kwargs.keys() else kwargs["funcname"]
        func_source = None if "func_source" not in kwargs.keys() else kwargs["func_source"]
        func_args = None if "func_args" not in kwargs.keys() else kwargs["func_args"]
        ssh = None if "ssh" not in kwargs.keys() else kwargs["ssh"]
        # compiled file name
        self._resclog.file = resc_filename

        renparams = {
            "syspath": sys.path,
            "rescsflag": inspect.getsource(RescLogSFlag),
            "resc_cpu": self._cpu_dict,
            "resc_mem": self._memory_dict,
            "resc_disk": self._disk_dict,
            "logfile": f"\"{self._resclog.pure_log}\"" \
                if self._resclog.pure_log is not None else None,
            "logformat": self._resclog.format_meta,
            "logvars": self._resclog.define_resclog,
            "ssh": ssh,
            "object_hash": RescObject._hash(resc_filename),
            "jfile": self._RESCJSONPATH,
            "reverse": self.reverse,
        }
        if funcname is not None:
            """
            function
            """
            source = RescCompile.compile(func_source)
            self._resclog.sour = source.encode("utf-8")

            args_str = str()
            if len(func_args["args"]) > 0:
                args_str = ",".join(
                    [str(x) if not isinstance(x, str)
                        else f"\"{x}\""
                        for x in func_args["args"]]
                )
                args_str += ","
            kwargs_str = str()
            if len(func_args["kwargs"].items()) > 0:
                for k, v in func_args["kwargs"].items():
                    if isinstance(v, str):
                        func_args["kwargs"][k] = f'\"{v}\"'
                kwargs_str = ",".join(
                    ["=".join([str(k), str(v)])
                    for k, v in func_args["kwargs"].items()]
                )
            i = 0
            while True:
                resc_key = f"def{i}.py"
                hash = hashlib.md5(resc_key.encode('utf-8')).hexdigest()
                sourcefile = f"{os.path.dirname(resc_filename)}/def_{hash}.py"
                if not os.path.exists(sourcefile):
                    break
                i += 1
            renparams.update({
                "sourcefile": sourcefile,
                "source": source,
                "sourcebyte": self._resclog.sour,
                "func": f"{funcname}({args_str}{kwargs_str})",
                "defname": funcname,
            })
        else:
            """
            source file
            """
            if not kwargs["exist_ok"]:
                # don't allow to be same python sdcript in crontab
                if RescObject.exist_samescript(
                    os.path.abspath(filename),
                    self._RESCJSONPATH
                ):
                    raise RescExistError(
                        "already exec_file be registered in cron."
                    )
            with open(filename, "r") as f:
                source = f.read()
            self._resclog.sour = source.encode("utf-8")

            renparams.update({
                "source": source,
                "sourcebyte": self._resclog.sour,
            })
        env = Environment(
            loader=FileSystemLoader(
                f'{self._package_path}/templates',
                encoding="utf-8"
            )
        )
        if funcname is not None:
            tmpl = env.get_template('resc_func.j2')
        else:
            tmpl = env.get_template('resc_file.j2')
        render = tmpl.render(renparams)
            
        with open(resc_filename, "w") as sf:
            sf.write(render)
        if not self.quiet:
            print("Output of compile:\t %s" % (resc_filename))
            if self._resclog.log:
                print("Output of log:\t %s" % (self._resclog.logfile))
            print("Output of register:\t %s"
                % (self._REGIPATH)
                )
        return resc_filename

    @property
    def _package_path(self):
        if resc.__path__ is None:
            raise RescValueError("resc package path is invalid.")
        if not isinstance(resc.__path__, list):
            raise RescTypeError("resc package path must be list")
        if len(resc.__path__) != 1:
            raise RescValueError("resc path list is invalid.")
        package_path = resc.__path__[0]
        return package_path

    def _startup_script(self, client, ssh):
        stdin, stdout, stderr = client.exec_command(
            f"bash {ssh.startup_scripts}"
        )
        stdin.close()
        return int(stdout.channel.recv_exit_status()), stderr

    def _resc_q(self, client):
        """
            Check Remote Host Resource using 'resc' command
        """
        stdin, stdout, stderr = client.exec_command(
            f"PATH=\"$PATH:~/.local/bin\" resc -q {self._resc_arg}"
        )
        stdin.close()
        status_code = int(stdout.channel.recv_exit_status())
        return status_code, stdout, stderr

    def _output_log(self, stdout, stderr, resclog):
        for out in stdout:
            resclog.stdout = out
        for err in stderr:
            resclog.stderr = err

    def over_one_ssh(
        self,
        ssh,
        resclog,
    ):
        client = ssh.connect(resclog)
        if client is None:
            return False

        package_path = self._package_path
        full_path = f"{package_path}/scripts/{self._SERVER_SCRIPT}"
        if not self._send_script(ssh, client, full_path, resclog):
            return False

        startup_exit_status, stderr = self._startup_script(client, ssh)
        if startup_exit_status != 0:
            ssh.close(client)
            for err in stderr:
                resclog.stderr = err
            raise RescServerError(
                (
                    f"server {os.path.basename(full_path)} "
                    f"exit status {startup_exit_status}"
                )
            )
        status_code, stdout, stderr = self._resc_q(client)
        ssh.close(client)
        if status_code == 0:
            self._output_log(stdout, stderr, resclog)
            return False
        elif status_code == 1:
            self._output_log(stdout, stderr, resclog)
            return False
        else:
            self._output_log(stdout, stderr, resclog)
            # return 255 is over resource
            return True

    @property
    def _resc_arg(self):
        resc_arg = list()
        if self._cpu_dict is not None:
            resc_arg.append(f'--cpu_t {self._cpu_dict["threshold"]}')
            if "mode" in self._cpu_dict.keys():
                resc_arg.append(f'--cpu_mode {self._cpu_dict["mode"]}')
            if "interval" in self._cpu_dict.keys():
                resc_arg.append(f'--cpu_interval {self._cpu_dict["interval"]}')
        if self._memory_dict is not None:
            resc_arg.append(f'--mem_t {self._memory_dict["threshold"]}')
            if "mode" in self._memory_dict.keys():
                resc_arg.append(f'--mem_mode {self._memory_dict["mode"]}')
        if self._disk_dict is not None:
            resc_arg.append(f'--disk_t {self._disk_dict["threshold"]}')
            resc_arg.append(f'--disk_path {self._disk_dict["path"]}')
            if "mode" in self._disk_dict.keys():
                resc_arg.append(f'--disk_mode {self._disk_dict["mode"]}')
        return " ".join(resc_arg)

    def _send_script(self, ssh, connect, script_path, resclog):
        return ssh.scpfile(connect, script_path, resclog)
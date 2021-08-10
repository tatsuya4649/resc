from .cpu import CPUDetect
from .memory import MemoryDetect
from .disk import DiskDetect
from .cron import Cron, CronCommandError
from .resclog.header import RescLogSFlag
from .object import RescObject
from .ssh import SSH
from .rescerr import RescTypeError, RescKeyError, RescCronError, \
    RescValueError, RescServerError
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
    _RESCSLOG_DEFAULT = os.path.join(
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

    def __init__(
        self,
        cpu=None,
        memory=None,
        disk=None,
    ):
        cpu = cpu if cpu else None
        memory = memory if memory else None
        disk = disk if disk else None
        self._cpu_dict = cpu
        self._memory_dict = memory
        self._disk_dict = disk
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

        self._checkers = list()
        self._checkers.append(self._cpu)
        self._checkers.append(self._memory)
        self._checkers.append(self._disk)
        self._checkers = [x for x in self._checkers if x is not None]
        self._crons = list()
        self._resclog = None

    @property
    def thresholds(self):
        retdic = dict()
        for x in self._checkers:
            retdic[x.resource] = {
                "threshold": x.threshold,
                "mode": x.mode,
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
    ):
        self.quiet = quiet
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
                        self._RESCSLOG_DEFAULT,
                        os.getenv(self._RESCOUTPUT_ENV)
            ),
            format=format,
        )
        if self._resclog.logfile is not None:
            os.environ[self._RESCOUTPUT_ENV] = self._resclog.logfile

        def _register(func):
            def _wrapper(*args, **kwargs):
                call_file = inspect.stack()[1].filename
                call_code = inspect.getsource(func.__code__)
                func_args = dict()
                func_args["args"] = args
                func_args["kwargs"] = kwargs
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
                self._resclog.func = func.__name__
                if ip is not None:
                    self._resclog.remo = ip
                compiled_filename = self._sourcefile(
                    file=call_file,
                    func=call_code,
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
                    log_file=None,
                )

            return _wrapper
        return _register

    def _directory_make(self, dirpath):
        os.makedirs(dirpath,exist_ok=True)

    def _sourcefile(self, file, func, funcname, func_args, ssh=None):
        resc_dir = os.getenv(self._RESCDIR_ENV)
        i = 0
        self._directory_make(resc_dir)
        while True:
            resc_key = os.path.join(
                resc_dir,
                f"resc{i}.py"
            )
            hash_value = hashlib.md5(resc_key.encode('utf-8')).hexdigest()
            filename = os.path.join(
                resc_dir,
                f"resc{hash_value}.py"
            )
            if not os.path.exists(filename):
                return self._source_write(
                    filename,
                    func,
                    funcname,
                    func_args,
                    ssh
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

    def _source_write(self, filename, func_source, funcname, func_args, ssh=None):
        self._resclog.file = filename
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
            sourcefile = f"{os.path.dirname(filename)}/def_{hash}.py"
            if not os.path.exists(sourcefile):
                break
            i += 1
        renparams = {
            "sourcefile": sourcefile,
            "source": source,
            "sourcebyte": self._resclog.sour,
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
            "func": f"{funcname}({args_str}{kwargs_str})",
            "defname": funcname,
        }
        env = Environment(loader=FileSystemLoader(
            f'{self._package_path}/templates',
            encoding="utf-8")
        )
        tmpl = env.get_template('resc.j2')
        render = tmpl.render(renparams)

        with open(filename, "w") as sf:
            sf.write(render)
        if not self.quiet:
            print("Output of compile:\t %s" % (filename))
            if self._resclog.log:
                print("Output of log:\t %s" % (self._resclog.logfile))
            print("Output of register:\t %s"
                % (self._REGIPATH)
                )
        return filename

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
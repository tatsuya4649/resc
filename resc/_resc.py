from .cpu import CPUDetect
from .memory import MemoryDetect
from .disk import DiskDetect
from .cron import Cron, CronCommandError
from .resclog.header import RescLogSFlag
from .ssh import SSH
from .rescerr import RescTypeError, RescKeyError, RescCronError, \
    RescValueError, RescAttributeError, RescServerError
from .resclog import RescLog
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
    _RESCPATH_ENV = "RESCPATH"
    _RESCPATH_DEFAULT = "~/.resc/"
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
            mustkeys = [x for x in
                        [k for k, v in
                            inspect
                            .signature(CPUDetect.__init__)
                            .parameters
                            .items()
                         if v.default is inspect._empty]
                        if x not in cpu.keys()]
            mustkeys.remove("self")
            if len(mustkeys) > 0:
                raise RescKeyError(f"cpu must have {mustkeys} key.")

        if memory is not None and not isinstance(memory, dict):
            raise RescTypeError("memory must be None or dict.")
        elif memory is not None:
            mustkeys = [x for x in
                        [k for k, v in
                            inspect
                            .signature(MemoryDetect.__init__)
                            .parameters
                            .items()
                            if v.default is inspect._empty]
                        if x not in memory.keys()]
            mustkeys.remove("self")
            if len(mustkeys) > 0:
                raise RescKeyError(f"memory must have {mustkeys} key.")

        if disk is not None and not isinstance(disk, dict):
            raise RescTypeError("disk must be None or dict.")
        elif disk is not None:
            mustkeys = [x for x in
                        [k for k, v in
                            inspect
                            .signature(DiskDetect.__init__)
                            .parameters
                            .items()
                            if v.default is inspect._empty]
                        if x not in disk.keys()
                        ]
            mustkeys.remove("self")
            if len(mustkeys) > 0:
                raise RescKeyError(f"disk must have {mustkeys} key.")

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
    def crons(self):
        return self._crons

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
    ):
        if not Cron.available():
            raise CronCommandError(
                "not found crontab command. you must have crontab command."
            )
        if subprocess.run("command", shell=True).returncode != 0:
            raise RescCronError(
                "not found command builtin command. \
                    you must have builtin command."
            )
        self._call_first = call_first \
            if isinstance(call_first, bool) else False
        if rescdir is not None and isinstance(rescdir, str):
            os.environ[self._RESCPATH_ENV] = rescdir
        if outputfile is not None and isinstance(outputfile, str):
            os.environ[self._RESCOUTPUT_ENV] = outputfile

        if os.getenv(self._RESCPATH_ENV) is None:
            os.environ[self._RESCPATH_ENV] = re.sub(
                r'^~',
                f'{os.path.expanduser("~")}',
                self._RESCPATH_DEFAULT + "resc",
            )
        else:
            if rescdir is not None:
                os.environ[self._RESCPATH_ENV] = re.sub(
                    r'^~',
                    f'{os.path.expanduser("~")}',
                    self._resc_dir(rescdir),
                )
            else:
                os.environ[self._RESCPATH_ENV] = re.sub(
                    r'^~',
                    f'{os.path.expanduser("~")}',
                    self._RESCPATH_DEFAULT + os.environ[self._RESCPATH_ENV]
                )
        if not isinstance(trigger, str):
            raise RescTypeError("trigger must be string type.")
        self._resclog = RescLog(
            logfile=os.getenv(self._RESCOUTPUT_ENV),
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
                        ip,
                        port=port,
                        username=username,
                        password=password,
                        key_filename=re.sub(
                            r'~',
                            f"{os.path.expanduser('~')}",
                            key_path
                        ) if key_path is not None else None,
                        timeout=timeout,
                    )
                else:
                    ssh = None
                self._resclog.func = func.__name__
                self._resclog.remo = ip
                filename = self._sourcefile(
                    file=call_file,
                    func=call_code,
                    funcname=func.__name__,
                    func_args=func_args,
                    ssh=ssh,
                )

                # Register crontable from trigger
                self._crons_get(trigger, filename)
                self._crons_register()

                if self._call_first:
                    func(*args, **kwargs)
            return _wrapper
        return _register

    def _resc_dir(self, dire):
        return self._RESCPATH_DEFAULT + re.sub(r'^/', '', str(dire))

    def _sourcefile(self, file, func, funcname, func_args, ssh=None):
        resc_dir = os.getenv(self._RESCPATH_ENV)
        # relative path to absolute path
        if not pathlib.Path(resc_dir).is_absolute():
            resc_dir = pathlib.Path(resc_dir).resolve()
        i = 0
        if not os.path.isdir(f"{resc_dir}"):
            os.makedirs(f"{resc_dir}")
        if not isinstance(func_args["args"], tuple):
            raise RescTypeError(
                'func_args["args"] must be tuple of argument.'
            )
        if not isinstance(func_args["kwargs"], dict):
            raise RescTypeError(
                'func_args["kwargs"] must be dict of keyword argument.'
            )
        while True:
            resc_path = f"{resc_dir}"
            resc_key = f"{resc_path}/resc{i}.py"
            hash = hashlib.md5(resc_key.encode('utf-8')).hexdigest()
            filename = f"{resc_path}/resc{hash}.py"
            if not os.path.exists(filename):
                return self._source_write(
                    filename,
                    func,
                    funcname,
                    func_args,
                    ssh
                )
            i += 1

    def _crons_get(self, trigger, triggerscript):
        if os.getenv(self._RESCOUTPUT_ENV) is not None:
            if not pathlib.Path(os.getenv(self._RESCOUTPUT_ENV)).is_absolute():
                output_path = f"""{pathlib.Path(
                    os.getenv(self._RESCOUTPUT_ENV)
                    ).resolve()}"""
            else:
                output_path = f"{os.getenv(self._RESCOUTPUT_ENV)}"
            output = f' >>{output_path} 2>&1'
        else:
            output = str()
            output_path = str()
        cp = subprocess.run(
            "command which resc",
            encoding="utf-8",
            stdout=subprocess.PIPE,
            shell=True,
        )
        which_resc = re.sub(r'\s*$', '', cp.stdout)
        if len(which_resc) > 0:
            totalline = (
                f'if ! [ -f {triggerscript} ]; '
                f'then {which_resc} --not_found \'{output_path}\'; '
                f'else command python3 {triggerscript} {output}; fi'
            )
            cron = Cron(
                totalline,
                trigger,
                re.sub(
                    r'^~',
                    f'{os.path.expanduser("~")}',
                    self._RESCPATH_DEFAULT + "register",
                )
            )
            if self._call_first:
                with open(output_path, "wb") as fp:
                    subprocess.run(
                        f"command python3 {triggerscript}",
                        stdout=fp,
                        stderr=fp,
                        shell=True,
                    )
            self._crons.append(cron)
        else:
            print(
                (
                    "resc command not found. "
                    "required in crontab."
                ), file=sys.stderr)
            if os.path.isfile(triggerscript):
                os.remove(triggerscript)
            sys.exit(1)

    def _crons_register(self):
        if not hasattr(self, "_crons"):
            raise RescAttributeError("_crons not found.")
        if not isinstance(self._crons, list):
            raise RescTypeError("_crons must be list.")
        if len(self._crons) == 0:
            return
        # register directive into crontable
        for cron in self._crons:
            cron.register()

    def _source_write(self, filename, func, funcname, func_args, ssh=None):
        self._resclog.file = filename
        iters = list()
        # delete until def keyword
        func = func[re.search(r'(?=.*)\t*def', func).start():]
        for line in func.split('\n'):
            match = re.match(r'^(?!(\s*)@).*$', line)
            if match is not None:
                iters.append(match)
        first_tab = re.match(r'^\s*', iters[0].group())
        matchs = list()
        if first_tab is not None and len(first_tab.group()) > 0:
            matchs = [
                re.sub(f'^{first_tab.group()}',
                       '',
                       x.group())
                for x in iters
            ]
            matchs = [x + '\n' for x in matchs]
        else:
            matchs = [x.group() for x in iters]
            matchs = [x + '\n' for x in matchs]
        matchs_str = "".join(matchs)
        self._resclog.sour = matchs_str[re.search(r'(?=.*)def',
                                                  matchs_str).start():
                                        ].encode("utf-8")

        args_str = str()
        if len(func_args["args"]) > 0:
            args_str = ",".join(
                [str(x) if not isinstance(x, str)
                    else f"\"{x}\""
                    for x in func_args["args"]]
            )
            args_str += ","
        kwargs_str = str()
        if len(func_args["kwargs"]) > 0:
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
        renparams = dict()
        renparams["sourcefile"] = sourcefile
        renparams["source"] = matchs_str[
            re.search(r'(?=.*)def', matchs_str).start():
        ]
        renparams["sourcebyte"] = bytes(
            matchs_str[re.search(r'(?=.*)def',
                       matchs_str).start():].encode("utf-8")
        )
        renparams["rescsflag"] = inspect.getsource(RescLogSFlag)
        renparams["syspath"] = self._par_resc
        renparams["resc_cpu"] = self._cpu_dict
        renparams["resc_mem"] = self._memory_dict
        renparams["resc_disk"] = self._disk_dict
        renparams["logfile"] = f"\"{self._resclog.pure_log}\"" \
            if self._resclog.pure_log is not None else None
        renparams["logformat"] = self._resclog.format_meta(self._resclog)
        renparams["logvars"] = self._resclog.define_resclog(self._resclog)
        renparams["ssh"] = ssh
        renparams["func"] = f"{funcname}({args_str}{kwargs_str})"
        renparams["defname"] = funcname
        env = Environment(loader=FileSystemLoader(
            f'{self._package_path}/templates',
            encoding="utf-8")
        )
        tmpl = env.get_template('resc.j2')
        render = tmpl.render(renparams)

        with open(filename, "w") as sf:
            sf.write(render)
        print("Output of compile:\t %s" % (filename))
        if self._resclog.log:
            print("Output of log:\t %s" % (self._resclog.logfile))
        print("Output of register:\t %s"
              % (re.sub(
                  r'^~',
                  f'{os.path.expanduser("~")}',
                  self._RESCPATH_DEFAULT + "register")
                 )
              )
        return filename

    @property
    def _package_path(self):
        if resc.__path__ is None or not isinstance(resc.__path__, list):
            raise RescValueError("resc package path is invalid.")
        if len(resc.__path__) != 1:
            raise RescValueError("resc path list is invalid.")
        package_path = resc.__path__[0]
        return package_path

    def over_one_ssh(self, ssh, resclog):
        client = ssh.connect
        package_path = self._package_path
        full_path = f"{package_path}/scripts/{self._SERVER_SCRIPT}"
        self._send_script(ssh, client, full_path, resclog)
        stdin, stdout, stderr = client.exec_command(
            f"bash {ssh.startup_scripts}"
        )
        if int(stdout.channel.recv_exit_status()) != 0:
            ssh.close(client)
            for err in stdout:
                resclog.output.append(err)
            raise RescServerError(
                (
                    f"server {os.path.basename(full_path)} "
                    f"exit status {stdout.channel.recv_exit_status()}"
                )
            )
        _, stdout, stderr = client.exec_command(
            f"PATH=\"$PATH:~/.local/bin\" resc -q {self._resc_arg}"
        )
        status_code = int(stdout.channel.recv_exit_status())
        ssh.close(client)
        if status_code == 0:
            for out in stdout:
                resclog.output.append(out)
            return False
        elif status_code == 1:
            for err in stderr:
                resclog.output.append(err)
            return False
        else:
            for out in stdout:
                resclog.output.append(out)
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
                resc_arg.append(f'--mem_mode {self._mem_dict["mode"]}')
        if self._disk_dict is not None:
            resc_arg.append(f'--disk_t {self._disk_dict["threshold"]}')
            if "mode" in self._disk_dict.keys():
                resc_arg.append(f'--disk_mode {self._disk_dict["mode"]}')
        return " ".join(resc_arg)

    def _send_script(self, ssh, connect, script_path, resclog):
        ssh.scpfile(connect, script_path, resclog)

    @property
    def _par_resc(self):
        dir = os.path.dirname(__file__)
        pardir = pathlib.Path(dir).resolve().parents[0]
        return pardir

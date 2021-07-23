import resc
from resc.cpu import CPUDetect
from resc.memory import MemoryDetect
from resc.disk import DiskDetect
from resc.cron import Cron
from resc.ssh import SSH
import inspect
import hashlib
import os
import pathlib
import re
import sys
import paramiko

class RescTypeError(TypeError):
	pass
class RescValueError(ValueError):
	pass
class RescAttributeError(AttributeError):
	pass
class RescKeyError(KeyError):
	pass
class RescServerError(Exception):
	pass

class Resc:
	"""
	"""
	_RESCPATH_ENV="RESCPATH"
	_RESCOUTPUT_ENV="RESCOUTPUT"
	_SERVER_SCRIPT="server.sh"
	def __init__(
		self,
		cpu=None,
		memory=None,
		disk=None,
	):
		cpu = cpu if cpu else None
		memory = memory if memory else None
		disk = disk if disk else None

		self._cpu_dict=cpu
		self._memory_dict=memory
		self._disk_dict=disk
		if cpu is not None and not isinstance(cpu,dict):
			raise RescTypeError("cpu must be None or dict.")
		elif cpu is not None:
			mustkeys = [x for x in [k for k,v in inspect.signature(CPUDetect.__init__).parameters.items() if v.default is inspect._empty] if x not in cpu.keys()]
			mustkeys.remove("self")
			if len(mustkeys) > 0:
				raise RescKeyError(f"cpu must have {mustkeys} key.")

		if memory is not None and not isinstance(memory,dict):
			raise RescTypeError("memory must be None or dict.")
		elif memory is not None:
			mustkeys = [x for x in [k for k,v in inspect.signature(MemoryDetect.__init__).parameters.items() if v.default is inspect._empty] if x not in memory.keys()]
			mustkeys.remove("self")
			if len(mustkeys) > 0:
				raise RescKeyError(f"memory must have {mustkeys} key.")

		if disk is not None and not isinstance(disk,dict):
			raise RescTypeError("disk must be None or dict.")
		elif disk is not None:
			mustkeys = [x for x in [k for k,v in inspect.signature(DiskDetect.__init__).parameters.items() if v.default is inspect._empty] if x not in disk.keys()]
			mustkeys.remove("self")
			if len(mustkeys) > 0:
				raise RescKeyError(f"disk must have {mustkeys} key.")

		if cpu is not None:
			cpu_string = str()
			for x in cpu.keys():
				if isinstance(cpu[x],str):
					cpu_string += f"{x}=\"{cpu[x]}\","
				else:
					cpu_string += f"{x}={cpu[x]},"
			self._cpu = eval(f'CPUDetect({cpu_string})')
		else:
			self._cpu = None

		if memory is not None:
			memory_string = str()
			for x in memory.keys():
				if isinstance(memory[x],str):
					memory_string += f"{x}=\"{memory[x]}\","
				else:
					memory_string += f"{x}={memory[x]},"
			self._memory = eval(f'MemoryDetect({memory_string})')
		else:
			self._memory = None

		if disk is not None:
			disk_string = str()
			for x in disk.keys():
				if isinstance(disk[x],str):
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
		if not hasattr(self,"_checks") or self._checks is None:
			retdic = dict()
			for x in self._checkers:
				retdic[x.resource] = x.check
			self._checks = retdic
		return self._checks
	@property
	def over_one(self):
		return False in [v for k,v in self.checks.items()]
	@property
	def overs(self):
		resources = [k for k,v in self.checks.items() if v is False]
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
	):
		if rescdir is not None and isinstance(rescdir,str):
			os.environ[self._RESCPATH_ENV] = rescdir
		if outputfile is not None and isinstance(outputfile,str):
			os.environ[self._RESCOUTPUT_ENV] = outputfile
		if rescdir is None and os.getenv(self._RESCPATH_ENV) is None:
			raise RescValueError(f"rescdir argument or environment variable({self._RESCPATH_ENV}) must be not None.")
		if not isinstance(trigger,str):
			raise RescTypeError("trigger must be string type.")
		def _register(func):
			def _wrapper(*args,**kwargs):
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
						key_filename=re.sub(r'~',f"{os.path.expanduser('~')}",key_path),
						timeout=timeout,
					)
				else:
					ssh = None
				filename = self._sourcefile(
					file=call_file,
					func=call_code,
					funcname=func.__name__,
					func_args=func_args,
					ssh=ssh,
				)

				self._crons_get(trigger,filename)
				self._crons_register()

			return _wrapper
		return _register
	
	def _sourcefile(self,file,func,funcname,func_args,ssh=None):
		resc_dir = os.getenv(self._RESCPATH_ENV)
		if not pathlib.Path(resc_dir).is_absolute():
			resc_dir = pathlib.Path(resc_dir).resolve()
		i=0
		if not os.path.isdir(f"{resc_dir}/rescs"):
			os.makedirs(f"{resc_dir}/rescs")

		if not isinstance(func_args["args"],tuple):
			raise RescTypeError('func_args["args"] must be tuple of argument.')
		if not isinstance(func_args["kwargs"],dict):
			raise RescTypeError('func_args["kwargs"] must be dict of keyword argument.')
		while True:
			resc_path = f"{resc_dir}/rescs"
			resc_key = f"{resc_path}/resc{i}.py"
			hash = hashlib.md5(resc_key.encode('utf-8')).hexdigest()
			filename = f"{resc_path}/resc{hash}.py"
			if not os.path.exists(filename):
				return self._source_write(filename,func,funcname,func_args,ssh)
			i+=1
	def _crons_get(self,trigger,triggerscript):
		if os.getenv(self._RESCOUTPUT_ENV) is not None:
			if not pathlib.Path(os.getenv(self._RESCOUTPUT_ENV)).is_absolute():
				output_path = f"{pathlib.Path(os.getenv(self._RESCOUTPUT_ENV)).resolve()}"
			else:
				output_path = f"{os.getenv(self._RESCOUTPUT_ENV)}"
			output = f' >{output_path} 2>&1'
		else:
			output = str()
		cron = Cron(f"python {triggerscript} {output}",trigger)
		self._crons.append(cron)
	def _crons_register(self):
		if not hasattr(self,"_crons"):
			raise RescAttributeError("_crons not found.")
		if not isinstance(self._crons,list):
			raise RescTypeError("_crons must be list.")
		if len(self._crons) == 0:
			return

		# register directive into crontable
		for cron in self._crons:
			cron.register()
	def _source_write(self,filename,func,funcname,func_args,ssh=None):
		iters = list()
		for line in func.split('\n'):
			match = re.match(r'^(?!(\s*)@).*$',line)
			if match is not None:
				iters.append(match)
#		for iter in iters:
#			print(iter)
		first_tab = re.match(r'^(?=\s)',iters[0].group())
		matchs = list()
		if first_tab is not None:
			matchs = [re.sub(f'^{first_tab.group()}','',x.group()) for x in iters]
			matchs = [x+'\n' for x in matchs]
		else:
			matchs = [x.group() for x in iters]
			matchs = [x+'\n' for x in matchs]
		with open(filename,"w") as sf:
			sf.write(self._import_resc)
#			if ssh is not None:
#				sf.write(self._import_others(ssh))
			sf.write(self._define_resc)
			matchs_str = "".join(matchs)
			sf.write(matchs_str[re.search(r'(?=.*)def',matchs_str).start():])
			if ssh is not None:
				sf.write(self._if_ssh_resc(ssh))
			else:
				sf.write(self._if_resc)
			args_str = str()
			if len(func_args["args"])>0:
				args_str = ",".join([str(x) if not isinstance(x,str) else f"\"{x}\"" for x in func_args["args"]])
				args_str += ","
			kwargs_str = str()
			if len(func_args["kwargs"])>0:
				for k,v in func_args["kwargs"].items():
					if isinstance(v,str):
						func_args["kwargs"][k] = f'\"{v}\"'
				kwargs_str = ",".join(["=".join([str(k),str(v)]) for k,v in func_args["kwargs"].items()])
			sf.write(f'\t{funcname}({args_str}{kwargs_str})\n')
		return filename
	
	@property
	def _if_resc(self):
		if_str = str()
		if_str += "if resc.over_one:\n"
		return if_str

	def _if_ssh_resc(self,ssh):
		if ssh is None:
			raise RescValueError("ssh must be not None.")
		if_ssh_str = str()
		if ssh.password is not None:
			autho_str = f"password=\"{ssh.password}\""
		else:
			autho_str = f"key_filename=\"{ssh.key_filename}\""
			
		if_ssh_str += f"""
ssh = SSH(
	ip=\"{ssh.ip}\",
	username=\"{ssh.username}\",
	{autho_str},
	timeout={ssh.timeout},
	)
if resc.over_one_ssh(ssh):
"""
		return if_ssh_str

	def over_one_ssh(self,ssh):
		client = ssh.connect
		if resc.__path__ is None or not isinstance(resc.__path__,list):
			raise RescValueError("resc package path is invalid.")
		if len(resc.__path__) != 1:
			raise RescValueError("resc path list is invalid.")
		package_path = resc.__path__[0]
		full_path = f"{package_path}/scripts/{self._SERVER_SCRIPT}"
		self._send_script(ssh,client,full_path)
		
		stdin,stdout,stderr = client.exec_command(f"bash ./{os.path.basename(full_path)}")
		if int(stdout.channel.recv_exit_status()) != 0:
			ssh.close(client)
			for err in stdout:
				print(err,end="")
			raise RescServerError(f"server {os.path.basename(full_path)} exit status {stdout.channel.recv_exit_status()}")

		print(self._resc_arg)	
		stdin,stdout,stderr = client.exec_command(f"PATH=$PATH:~/.local/bin resc {self._resc_arg}")
		status_code = int(stdout.channel.recv_exit_status())
		ssh.close(client)
		if status_code == 0:
			return False
		elif status_code == 1:
			for err in stderr:
				print(err,end="")
			return False
		else:
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

	def _send_script(self,ssh,connect,script_path):
		ssh.scpfile(connect,script_path)

	@property
	def _import_resc(self):
		import_str = str()
		dir = os.path.dirname(__file__)
		pardir = pathlib.Path(dir).resolve().parents[0]
		import_str += "import sys\n"
		import_str += f"sys.path.append(\"{pardir}\")\n"
		import_str += "from resc import Resc\n"
		import_str += "from resc import SSH\n"
		return import_str

	def _import_others(self,ssh):
		if ssh is None:
			raise RescValueError("ssh must be not None.")
		import_str = str()
		return import_str
	@property
	def _define_resc(self):
		define_str = str()
		define_str += f"\nresc=Resc(cpu={self._cpu_dict},memory={self._memory_dict},disk={self._disk_dict})\n"
		return define_str

__all__ = [
	Resc.__name__,
]

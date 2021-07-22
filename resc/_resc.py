from resc.cpu import CPUDetect
from resc.memory import MemoryDetect
from resc.disk import DiskDetect
import inspect
import hashlib
import os
import re

class RescTypeError(TypeError):
	pass
class RescKeyError(KeyError):
	pass

class Resc:
	def __init__(
		self,
		cpu=None,
		memory=None,
		disk=None,
	):
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
		retdic = dict()
		for x in self._checkers:
			retdic[x.resource] = x.check
		return retdic
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

	def register(self,trigger):
		if not isinstance(trigger,str):
			raise RescTypeError("trigger must be string type.")
		def _register(func):
			call_file = inspect.stack()[1].filename
			call_code = inspect.getsource(func.__code__)
			filename = self._sourcefile(call_file,call_code,func.__name__)
			print(filename)
			def _wrapper(*args,**kwargs):
				print(f"interval {trigger}")
				func(*args,**kwargs)
			return _wrapper
		return _register
	
	def _sourcefile(self,file,func,funcname):
		i=0
		if not os.path.isdir("rescs"):
			os.makedirs("rescs")
		while True:
			string = f"resc{i}.py"
			hash = hashlib.md5(string.encode('utf-8')).hexdigest()
			filename = f"rescs/resc{hash}.py"
			if not os.path.exists(filename):
				return self._source_write(filename,func,funcname)
			i+=1
	def _source_write(self,filename,func,funcname):
		iters = list()
		for line in func.split('\n'):
			match = re.match(r'^(?!(\s*)@).*$',line)
			if match is not None:
				iters.append(match)
#		for iter in iters:
#			print(iter)
		first_tab = re.match(r'^\s+',iters[0].group())
		if first_tab is not None:
			matchs = [re.sub(f'^{first_tab.group()}','',x.group()) for x in iters]
			matchs = [x+'\n' for x in matchs]
		with open(filename,"w") as sf:
			sf.write("".join(matchs))
			sf.write(f"{funcname}()\n")
		return filename

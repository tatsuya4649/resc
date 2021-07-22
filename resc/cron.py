from enum import Enum
import re
import subprocess

class CronScale(Enum):
	MIN={"name":"minute","min":0,"max":59}
	HOU={"name":"hour","min":0,"max":23}
	DAY={"name":"day","min":1,"max":31}
	MON={"name":"month","min":1,"max":12}
	WEE={"name":"week","min":0,"max":6}
class CronMode(Enum):
	INTERVAL="interval"
	SCHEDULE="schedule"

class CronTypeError(TypeError):
	pass
class CronAttributeError(AttributeError):
	pass
class CronValueError(ValueError):
	pass
class CronRegularExpressionError(ValueError):
	pass

class Cron:
	"""
	"""
	_CRON_RE = r'(([0-6]?[0-9]-[0-6]?[0-9])|((,?[0-6]?[0-9])+)|(\*))(/[0-6]?[0-9])?'
	def __init__(
		self,
		command,
		interval_str,
	):
		if not isinstance(command,str):
			raise CronTypeError("command must be str type.")
		self._command = command
		self._command = self._quote_replace()

		if interval_str is None:
			raise CronValueError("interval_str must be not None.")

		self._interval_str = interval_str
		self._str_to_lists()
		self._totalline = f"{self._interval_str} \"{self._command}\"\n"

	@property
	def interval_str(self):
		return self._interval_str
	@property
	def totalline(self):
		return self._totalline

	def _str_to_lists(self):
		self._intervals = list()
		template = self._CRON_RE

		results = re.finditer(template,self._interval_str)
		results = [i for i in results]
		if len(results) != 5:
			raise CronRegularExpressionError("invalid cron string")
		for res in results:
			# */10
			deleteblank = re.match(r"^\S+",res.group())
			if deleteblank is None:
				raise CronRegularExpressionError("invalid cron string")
			# *
			before_slash = deleteblank.group().split('/')[0]

			index = results.index(res)
			if len(before_slash.split('-'))>1:
				self._intervals.append({
					"interval":-1,
					"scale":CronMode.SCHEDULE,
					"mode":list(CronScale)[index],
					"from":before_slash.split('-')[0],
					"to":before_slash.split('-')[1],
				})
			else:
				self._intervals.append({
					"interval":int(before_slash) if before_slash != '*' else "*",
					"scale":CronMode.SCHEDULE,
					"mode":list(CronScale)[index],
				})
				
			# 10
			if len(deleteblank.group().split('/')) > 1:
				after_slash = deleteblank.group().split('/')[1]
				self._intervals.append({
					"interval":int(after_slash),
					"scale":CronMode.INTERVAL,
					"mode":list(CronScale)[index],
				})
				
	def _quote_replace(self):
		return self._command.replace('"','\\"')

	@property
	def _list(self):
		result = subprocess.Popen(["crontab","-l"],encoding="utf-8",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		comm = result.communicate()
		errout = comm[1]
		stdout = comm[0]
		if re.match(r'^no crontab',errout) is not None:
			return None
		else:
			return stdout
	def register(self):
		if self._list is None:
			input = self._totalline
		else:
			iter = re.finditer(r'.*\n',self._list)
			cronlists = [x.group() for x in iter]
			# delete duplication
			cronlists = list(set(cronlists))
			if self._totalline not in cronlists: 
				cronlists.append(self._totalline)
			input = "".join(list(set(cronlists)))	
		res = subprocess.run(["crontab"],input=input,encoding='utf-8')
		return res.returncode
	@property
	def list(self):
		lists = self._list
		if lists is None:
			return None

		iter = re.finditer(r'.*\n',lists)
		cronlists = [x.group() for x in iter]
		return cronlists
	@property
	def count(self):
		return len(self.list if self.list is not None else list())
	def delete(self):
		if self._list is None:
			return None
		else:
			iter = re.finditer(r'.*\n',self._list)
			cronlists = [x.group() for x in iter]
			# delete duplication
			cronlists = list(set(cronlists))
			if self._totalline in cronlists: 
				cronlists.remove(self._totalline)
			if len(cronlists) == 0:
				res = subprocess.run(["crontab","-r"])
				return res.returncode
			else:
				input = "".join(list(set(cronlists)))	
				res = subprocess.run(["crontab"],input=input,encoding='utf-8')
				return res.returncode

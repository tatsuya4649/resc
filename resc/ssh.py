import paramiko
import scp
import os

class SSH:
	_FORDEST="/var/resc/"
	def __init__(
		self,
		ip,
		username,
		password=None,
		key_filename=None,
		timeout=5,
		port=22,
	):
		self._ip = ip
		self._port = port
		self._username = username
		self._password = password
		self._key_filename = key_filename
		self._timeout = timeout
		self._startup_scripts = None
	
	@property
	def import_str(self):
		res = str()
		res += f"""
		import paramiko
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(policy.WarningPolocy())
		client.connect(
			{self._ip},
			username={self._username},
			key_filename={self._key_filename},
			timeout={self._timeout},
		)
		"""
	@property
	def ip(self):
		return self._ip
	@property
	def username(self):
		return self._username
	@property
	def password(self):
		return self._password
	@property
	def key_filename(self):
		return self._key_filename
	@property
	def timeout(self):	
		return self._timeout
	@property	
	def connect(self):
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(
			hostname=self._ip,
			port=self._port,
			username=self._username,
			password=self._password,
			key_filename=self._key_filename,
			timeout=self._timeout,
		)
		return client
	def close(self,client):
		client.close()

	def scpfile(self,connect,script_path):
		self._startup_scripts = f"~/.resc/{os.path.basename(script_path)}"
		with scp.SCPClient(connect.get_transport()) as s:
			s.put(script_path,self._startup_scripts)
	
	@property
	def startup_scripts(self):
			return self._startup_scripts
		

__all__ = [
	SSH.__name__,
]

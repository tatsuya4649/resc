import paramiko
import scp

class SSH:
	_FORDEST="/var/resc/"
	def __init__(
		self,
		ip,
		username,
		password=None,
		key_filename=None,
		timeout=5,
	):
		self._ip = ip
		self._username = username
		self._password = password
		self._key_filename = key_filename
		self._timeout = timeout
	
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
		client.set_missing_host_key_policy(policy.WarningPolocy())
		client.connect(
			{self._ip},
			username={self._username},
			key_filename={self._key_filename},
			timeout={self._timeout},
		)
		return client

	def send_bashfile(self,file,connect):
		with scp.SCPClient(connect.get_transport()) as scp:
			scp.put(file,self._FORDEST)
		

__all__ = [
	SSH
]

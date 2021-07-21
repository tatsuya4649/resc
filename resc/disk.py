import psutil
import os

def _disk_usage(path):
	if not isinstance(path,str):
		raise TypeError("path must be string type.")
	if not os.path.exists(path):
		raise FileNotFoundError(f"{path} not exists")
	return psutil.disk_usage(path)

def disk_percent(path):
	return _disk_usage(path).percent

def disk_free(path):
	return _disk_usage(path).free

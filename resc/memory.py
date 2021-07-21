import psutil

def memory_percent():
	return psutil.virtual_memory().percent

def memory_used():
	return psutil.virtual_memory().used

def memory_available():
	return psutil.virtual_memory().available

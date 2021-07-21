import psutil

def ave_cpu_percent(interval):
	if not isinstance(interval,float) and not isinstance(interval,int):
		raise TypeError("interval must by float or int type.")
	return psutil.cpu_percent(interval=float(interval),percpu=False)

def cpu_percent(interval):
	if not isinstance(interval,float) and not isinstance(interval,int):
		raise TypeError("interval must by float or int type.")
	return psutil.cpu_percent(interval=float(interval),percpu=True)

def cpuloadavg():
	return psutil.getloadavg()

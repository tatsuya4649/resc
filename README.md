
# Resource checker

Resc check resources(CPU,memory,disk) of target host(local or remote) and execute script.

# Usage

example Python code.

```
from resc import Resc

resc = Resc(
	cpu={"threshold": 80.0,"interval": 10},
	memory={"threshold": 90.0},
	disk={"threshold":75,"path":"/"},
)

@resc.register(
	trigger="* * * * *",	# crontab job time
	rescdir="rescs",	# output directory of compiled python script file
	outputfile="output",	# output file of crontab if it is fired when resource threshold is exceeded.(directory: ~/.resc/log/ + outputfile)
	ip="13.231.122.182",	# if check remote host,specify IP address
	username="ubuntu",	# if check remote host,remote host username
	call_first=True,			# call just now?
	key_path="~/.aws/ExampleSSH.pem", # if check remote host, key file path to connect remote host with SSH.
)
def hello():
	print("OVER RESOURCE!!!")

hello()
```

# Term

**threshold**(cpu):  threshold that is system-wide CPU utilization as a percentage.int or float type.

**interval**(cpu): interval is check interval time(s).int or float type.

**threshold**(memory): threshold that is system memory utilization as a percentage.int or float type.

**path**(disk): check the capacity of the partition according to the given path.

**threshold**(disk): threshold that is partition utilization which containes given path.


# How does that work?

1. Register decorator is a decorator to prepare for resource check using given threshold of resources,host information,etc.
2. Decorated function(above def hello()) is called function when resource threshold is exceeded.
3. Make new python script for crontab.(~/.resc/ + rescdir)
4. Register crontab with 3.python script and interval info(trigger argument of register decorator).

If call_first argument is False(default False), decorated function is not called until resources are exceeded.

WARNING: Because decorated function will be compiled, it must be coded as an independent scope.

## bad example. 

```
import math
class Bad:
	@classmethod
	def example(self):
		return "hello world"

def bad():
	# NameError: name 'math' is not defined
	math.floor(10.9)
	Bad.example()
```

## good example.

```
def good():
	import math
	class Bad:
		@classmethod
		def example(self):
			return "hello world"
	math.floor(10.9)
```

# Crontab

Crontab is a important element of this library.So, show 'man crontab or crontab -e' for detail of crontab

# Required

Python3,Crontab,and python library in requirements.txt.

import os
import re

from setuptools import setup

def _requires_from_file(filename):
	with open(filename,"r") as f:
		return f.read().splitlines()

def get_version(package):
    path = os.path.join(package,"__init__.py")
    with open(path,"r",encoding="utf-8") as f:
        init_py = f.read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]",init_py).group(1)


setup(
	install_requires=_requires_from_file("requirements.txt"),
    version=get_version("resc"),
)

from setuptools import setup

def _requires_from_file(filename):
	with open(filename,"r") as f:
		return f.read().splitlines()

setup(
	install_requires=_requires_from_file("requirements.txt"),
	package_data={
		"": ["scripts/*"],
	}
)

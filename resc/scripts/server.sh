#!/bin/bash

REPO='resc'
YUM_CMD=$(which yum)
APT_CMD=$(which apt)
SUDO_CMD=$(which sudo)
GIT_CMD=$(which git)
PYTHON_CMD=$(which python3)
PIP_CMD=$(which pip3)
PIP_RESC=resc
PIP_RESC_CMD="pip3 show $PIP_RESC >/dev/null 2>&1; echo $?"

function sudo_check(){
	if [ -z "$SUDO_CMD" ]; then
		SUDO=""
	else
		SUDO=sudo
	fi
}

function package_install(){
	if [ -z "$1" ]; then
		echo "package_system must have argument."
		exit 1
	fi
	sudo_check
	if [ -n "$YUM_CMD" ]; then
		$SUDO yum install -y "$@"
	elif [ -n "$APT_CMD" ]; then
		$SUDO apt install -y "$@"
	else
		echo "invalid package system."
		exit 1
	fi
}

function package_install_git(){
	sudo_check
	package_update
	if [ -n "$YUM_CMD" ]; then
		$SUDO yum install -y git
	elif [ -n "$APT_CMD" ]; then
		$SUDO apt install -y git
	else
		echo "invalid package system."
		exit 1
	fi
}

function package_install_python(){
	sudo_check
	package_update
	if [ -n "$YUM_CMD" ]; then
		$SUDO yum install -y epel-release
		$SUDO yum install -y python3
	elif [ -n "$APT_CMD" ]; then
		$SUDO apt install -y python3-pip
	else
		echo "invalid package system."
		exit 1
	fi
}
function package_install_pip(){
	sudo_check
	package_update
	if [ -n "$YUM_CMD" ]; then
		echo ""
	elif [ -n "$APT_CMD" ]; then
		$SUDO apt install -y python3-pip
	else
		echo "invalid package system."
		exit 1
	fi
}

function package_update(){
	sudo_check
	if [ -n "$YUM_CMD" ]; then
		$SUDO yum update
	elif [ -n "$APT_CMD" ]; then
		$SUDO apt update
	else
		echo "invalid package system."
		exit 1
	fi
}


if [ -z "$GIT_CMD" ]; then
	package_update
	package_install_git
fi
if [ -z "$PYTHON_CMD" ]; then
	package_install_python
	package_install_git
fi

if [ -z "$PIP_CMD" ]; then
	package_install_pip
fi
if [ -z "$PIP_CMD" ]; then
	echo "pip3 not found..."
	exit 1
fi

if [ "$PIP_RESC_CMD" -eq 0 ]; then
	echo "already have $PIP_RESC"
	exit 0
fi
pip3 install "$REPO"

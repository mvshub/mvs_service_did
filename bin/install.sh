#!/bin/sh

export DEBIAN_FRONTEND=noninteractive
APTOPTS="-qq -y --no-install-suggests --no-install-recommends"

apt-get update -y
apt-get install ${APTOPTS} wget sqlite3 python
apt-get autoremove && apt-get clean

# install setuptools
wget --no-check-certificate https://pypi.python.org/packages/source/s/setuptools/setuptools-12.0.3.tar.gz && tar -zxvf setuptools-12.0.3.tar.gz && cd setuptools-12.0.3 && python setup.py install && cd ..

# install pip
wget -q https://pypi.python.org/packages/source/p/pip/pip-1.3.1.tar.gz --no-check-certificate && tar -zxvf pip-1.3.1.tar.gz && cd pip-1.3.1 && python setup.py install && cd ..

# install flask
pip install flask flask-sqlalchemy sqlalchemy-utils

# do cleaning jobs at last, to decrease the size of docker image.

# remove source codes and scripts
rm -rf setuptools-12.0.3.tar.gz pip-1.3.1.tar.gz setuptools-12.0.3 pip-1.3.1

# remove temp and cached files
rm -rf /var/lib/apt/lists/*
rm -rf /tmp/* /var/tmp/*

# remove manual and doc
rm -rf /usr/share/doc/*
rm -rf /usr/share/man/*

# clear history
rm -rf ~/.bash_history

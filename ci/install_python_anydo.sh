#!/usr/bin/env bash
set -x
set -e

git clone --depth=50 --branch=master https://github.com/dustinbrown/python-anydo.git dustinbrown/python-anydo

cd dustinbrown/python-anydo
pip install .
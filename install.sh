#!/bin/bash

virtualenv env -p `which python3.4` --verbose

env/bin/pip install -r requirements.txt --verbose


# Manual install of facebook-sdk - No pip version only for python 2
git clone https://github.com/pythonforfacebook/facebook-sdk.git
cd facebook-sdk
../env/bin/python3.4 setup.py install
cd ..
rm -rf facebook-sdk
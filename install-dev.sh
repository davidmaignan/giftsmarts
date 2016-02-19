#!/bin/bash

if ! hash grunt 2>/dev/null; then
    npm install -g grunt@0.1.13
fi

if ! hash bower 2>/dev/null; then
    npm install -g grunt-cli@1.5.2
fi

npm install --verbose
bower install --verbose
gem install sass --verbose

virtualenv env -p `which python3.4` --verbose

env/bin/pip install -r requirements.txt --verbose

# Manual install of facebook-sdk - No pip version only for python 2
git clone https://github.com/pythonforfacebook/facebook-sdk.git
cd facebook-sdk
../env/bin/python3.4 setup.py install
cd ..
rm -rf facebook-sdk

# Redis installation
curl -O http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
rm redis-stable.tar.gz
cd redis-stable
make
cd ..
mv redis-stable redis

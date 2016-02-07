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
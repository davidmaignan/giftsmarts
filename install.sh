#!/bin/bash

virtualenv env -p `which python3.4` --verbose

env/bin/pip install -r requirements.txt --verbose
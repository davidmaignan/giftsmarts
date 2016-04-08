#!/bin/bash
#

export FLASK_ENV="dev"

env/bin/celery -A app.config.config.celery worker --loglevel=debug

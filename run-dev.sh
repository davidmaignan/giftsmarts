#!/bin/bash
#
PID=$(pgrep -f "runserver|celery|redis")
for i in ${PID};
do
    echo ${i}
    kill ${i}
done

export FLASK_ENV="dev"

redis/src/redis-server > logs/redis.log 2>&1 &
env/bin/python manage.py runserver -d -r > logs/server.log 2>&1 &
env/bin/celery -A app.config.config.celery worker --loglevel=debug > logs/celery.log 2>&1  &

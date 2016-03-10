#!/bin/bash
#
PID=$(pgrep -f "runserver|celery|redis|nodemon")
for i in ${PID};
do
    echo kill: ${i}
    kill ${i}
done
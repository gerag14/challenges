#!/bin/bash

if [ "$1" == "makemigrations" ]
then
    shift
    msg="$@"
    exec alembic revision --autogenerate -m "$msg"
elif [ "$1" == "migrate" ]
then
    exec python manage.py migrate
elif [ "$1" == "shell" ]
then
    exec ipython
elif [ "$1" == "bash" ]
then
    exec bash
elif [ "$1" == "test" ]
then
    shift
    msg="$@"
    exec pytest --cov=app --cov-report=term-missing "${@}"
elif [ "$1" == "tests" ]
then
    shift
    msg="$@"
    exec pytest --cov=app --cov-report=term-missing
else
    exec python main.py
fi

echo "Fin entrypoint..."

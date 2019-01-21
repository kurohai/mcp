#!/usr/bin/env bash


cd /app

if [[ ! -f "./venv/bin/activate" ]];
then
    virtualenv venv
    pip install -r ./requirements-dev.txt
fi

. ./venv/bin/activate

echo "FLASK_HOST: $FLASK_HOST"
echo "FLASK_PORT: $FLASK_PORT"
echo "FLASK_DEBUG: $FLASK_DEBUG"
echo "FLASK_APP: $FLASK_APP"

# exec ./venv/bin/gunicorn -b ${FLASK_HOST}:${FLASK_PORT} --access-logfile - --error-logfile - mcp.wsgi:app
exec ./venv/bin/flask run --port ${FLASK_PORT} --host ${FLASK_HOST} --debugger --reload

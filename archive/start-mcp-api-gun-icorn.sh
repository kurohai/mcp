#!/bin/bash

. ./.venv/bin/activate

FLASK_PORT=9004
FLASK_HOST="0.0.0.0"
FLASK_DEBUG="True"
# RUNAPP="True"

# flask db upgrade
# flask translate compile
# gunicorn -b :9004 --access-logfile - --error-logfile - mcp.wsgi:app
gunicorn -b ${FLASK_HOST}:${FLASK_PORT} --access-logfile - --error-logfile - mcp.wsgi:app

#!/bin/sh

. ./.venv/bin/activate

 FLASK_PORT=9004
 FLASK_HOST="0.0.0.0"
 FLASK_DEBUG="False"
 RUNAPP="True"

# flask db upgrade
# flask translate compile
gunicorn -b :9004 --access-logfile - --error-logfile - mcp.wsgi:app

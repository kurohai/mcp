#!/bin/sh

cd /app

. /app/venv/bin/activate
# flask db upgrade
# flask translate compile
exec ./venv/bin/gunicorn -b :8087 --access-logfile - --error-logfile - mcp.wsgi:app

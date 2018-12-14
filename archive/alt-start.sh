#!/bin/sh


source venv/bin/activate
# flask db upgrade
# flask translate compile
exec gunicorn -b :8087 --access-logfile - --error-logfile - mcp.wsgi:app

#! /usr/bin/env bash
set -e

# If there's a prestart.sh script in the /app directory, run it before starting
PRE_START_PATH=/app/prestart.sh
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    source $PRE_START_PATH
else
    echo "There is no script $PRE_START_PATH"
fi

# Start Supervisor, with Nginx and uWSGI
# exec uwsgi
# exec /usr/bin/supervisord -c /app/supervisord.ini
# exec /app/.venv/bin/uwsgi --ini /app/uwsgi-develop.ini
source /app/.venv/bin/activate
exec /app/.venv/bin/python /app/mcp/tuya_controller.py

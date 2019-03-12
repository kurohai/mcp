#!/usr/bin/env bash


cd /app

if [[ -e "./redo" ]];
then
    echo "creating virtual env"
    virtualenv venv
    echo "activation venv..."
    . ./venv/bin/activate
    echo "install packages from requirements.txt"
    ./venv/bin/pip install -r ./requirements.txt
fi

if [[ ! -e "./venv/bin/flask" ]];
then
    echo -en "\n\n\nFLASK NOT FOUND IN VENV"
    ./venv/bin/pip install -r ./requirements.txt
fi

RELOAD=${FLASK_RELOAD}



. ./venv/bin/activate

echo "FLASK_HOST: ${MYSQL_USERNAME}"
echo "FLASK_HOST: ${MYSQL_PASSWORD}"
echo "FLASK_HOST: ${MYSQL_HOSTNAME}"
echo "FLASK_HOST: ${MYSQL_DATABASE}"




echo "FLASK_HOST: $FLASK_HOST"
echo "FLASK_PORT: $FLASK_PORT"
echo "FLASK_DEBUG: $FLASK_DEBUG"
echo "FLASK_APP: $FLASK_APP"
echo "RELOAD: ${RELOAD}"

# exec ./venv/bin/gunicorn -b ${FLASK_HOST}:${FLASK_PORT} --access-logfile --error-logfile mcp.wsgi:app
# exec ./venv/bin/flask run --port ${FLASK_PORT} --host ${FLASK_HOST} --debugger --reload &

#export FLASK_APP=${FLASK_APP_02}
# exec ./venv/bin/flask run --port ${FLASK_PORT} --host ${FLASK_HOST} --debugger ${RELOAD}

# pkill -f supervisord
# ./venv/bin/supervisorctl -c ./supervisord.conf shutdown

# exec ./venv/bin/supervisord  --nodaemon -c ./supervisord.conf
exec ./venv/bin/python ./manage_mastercontrol.py quick --port=9002


# exec ./venv/bin/supervisorctl -c ./supervisord.conf start mcp-api



# supergo="$(ps -eF | egrep -v grep | egrep supervisor)"

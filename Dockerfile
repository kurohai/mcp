FROM ubuntu:18.04
# FROM python:2.7-alpine

RUN apt-get update; apt-get install -y python-pyaes python2.7 python-pip

RUN mkdir /app
WORKDIR /app
RUN pip install virtualenv
RUN virtualenv venv
RUN ls -halF ./venv/bin/
RUN . /app/venv/bin/activate

COPY requirements.txt /app/requirements.txt

# RUN python -m venv venv

RUN venv/bin/pip install -U pip

RUN venv/bin/pip install pyaes==1.6.1

RUN venv/bin/pip install -r requirements.txt

RUN venv/bin/pip install gunicorn

COPY ./ /app/



RUN chmod +x start.sh
# RUN chmod +x entrypoint.sh

ENV FLASK_APP mcp/tuya_controller.py

# RUN chown -R microblog:microblog ./
# USER microblog

EXPOSE 8087
ENTRYPOINT ["./start.sh"]

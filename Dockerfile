FROM ubuntu:18.04


RUN apt-get update; apt-get install -y python-pyaes python2.7 python-pip

RUN mkdir /app
WORKDIR /app

RUN pip install virtualenv
RUN virtualenv venv
RUN . venv/bin/activate

COPY ./requirements-dev.txt requirements.txt

RUN venv/bin/pip install -U pip

RUN venv/bin/pip install pyaes==1.6.1

RUN venv/bin/pip install -r requirements.txt

RUN venv/bin/pip install gunicorn

COPY ./start.sh /app/start.sh

RUN chmod a+x start.sh

RUN find ./ -type f -maxdepth 3 -exec chmod a+rx {} \;
RUN find ./ -type d -maxdepth 3 -exec chmod a+rxs {} \;

EXPOSE 8087
ENTRYPOINT ["./start.sh"]

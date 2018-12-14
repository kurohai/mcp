FROM python:2.7-alpine


RUN mkdir /app
WORKDIR /app
RUN virtualenv venv

COPY requirements.txt /app/requirements.txt

# RUN python -m venv venv

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

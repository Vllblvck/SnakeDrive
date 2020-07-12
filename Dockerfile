FROM python:3.8.3-alpine

RUN adduser -D snakedrive

WORKDIR /home/snakedrive

RUN apk update 
RUN apk add gcc
RUN apk add musl-dev
RUN apk add libffi-dev
RUN apk add openssl-dev

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY snakedrive.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP snakedrive.py

RUN chown -R snakedrive:snakedrive ./
USER snakedrive

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]

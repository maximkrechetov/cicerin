FROM python:3.7-slim

RUN bash -c "echo 'deb http://deb.debian.org/debian sid main' >> /etc/apt/sources.list"

WORKDIR /app

ADD requirements.txt /app
RUN pip3 install -r requirements.txt

ENV FLASK_APP ciceron:app 

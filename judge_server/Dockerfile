FROM python:3.7-alpine3.8

MAINTAINER Chihiro Iha <ryubi.102395@gmail.com>

RUN mkdir /app && \
    apk add --no-cache --update postgresql-dev musl-dev libpq gcc && \
    pip install -U pip
WORKDIR /app
COPY requirements.txt ./
ADD src ./

RUN pip install -r requirements.txt

FROM python:3.7.2-alpine3.9

MAINTAINER Taichi Uchihara <hoge.uchihara@gmail.com>

RUN \
  apk add --no-cache postgresql-dev musl-dev libpq gcc && \
  pip install -U pip --proxy http://cproxy.okinawa-ct.ac.jp:8080 && \
  mkdir /app

WORKDIR /app
ADD requirements.txt /app

RUN  pip install -r requirements.txt --proxy http://cproxy.okinawa-ct.ac.jp:8080

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]

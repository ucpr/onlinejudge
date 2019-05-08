FROM python:3.7.2-alpine3.9

MAINTAINER Chihiro Iha

RUN mkdir /runner && \
    apk add gcc libc-dev
ADD ./main.py ./judge_result.py /runner/
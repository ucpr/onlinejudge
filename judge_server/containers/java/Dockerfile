FROM python:3.7.2-alpine3.9

MAINTAINER Chihiro Iha

RUN mkdir /runner && \
    apk add openjdk8

ENV JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk
ENV PATH="$JAVA_HOME/bin:${PATH}"

ADD ./main.py ./judge_result.py /runner/
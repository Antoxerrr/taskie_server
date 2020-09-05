# Временный Dockerfile
FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
ADD . /app

RUN pip install pipenv
RUN pipenv install
RUN ls /app
FROM python:3.11.4-alpine
LABEL maintainer="anton_komarov_qa@ukr.net"

ENV PYTHONBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

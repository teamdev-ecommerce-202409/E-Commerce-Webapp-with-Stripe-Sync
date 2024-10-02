FROM ubuntu:24.04

RUN apt update && apt upgrade -y
ENV TZ=Asia/Tokyo
RUN apt install -y tzdata
RUN apt install -y --no-install-recommends mysql-server

RUN mkdir /django
RUN mkdir /django/logs
WORKDIR /django

RUN apt install -y python3.12 python3-pip python3-venv
RUN apt install -y pkg-config
RUN apt install -y libmysqlclient-dev

COPY requirements.txt /django
COPY .env /django
COPY docker-entrypoint.sh /django

RUN python3 -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

WORKDIR /django/src
RUN chmod +x /django/docker-entrypoint.sh
ENTRYPOINT ["/django/docker-entrypoint.sh"]

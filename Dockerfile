FROM ubuntu:24.04

RUN mkdir /django
RUN mkdir -p /django/logs/debug
RUN mkdir -p /django/logs/info
RUN mkdir -p /django/logs/warning
RUN mkdir -p /django/logs/error
RUN mkdir -p /django/logs/critical
WORKDIR /django

RUN apt update && apt upgrade -y
RUN apt install -y python3.12 python3-pip python3-venv
RUN apt install -y pkg-config libmysqlclient-dev libjpeg-dev zlib1g-dev  # Pillowに必要な依存関係を追加
RUN apt install -y libpng-dev libfreetype6-dev  # 追加で必要な画像ライブラリをインストール

COPY requirements.txt /django
COPY .env /django
COPY docker-entrypoint.sh /django
COPY wait-for-it.sh /django

RUN python3 -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

WORKDIR /django/src
RUN chmod +x /django/docker-entrypoint.sh
RUN chmod +x /django/wait-for-it.sh
ENTRYPOINT ["/django/docker-entrypoint.sh"]

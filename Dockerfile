FROM ubuntu:24.04

# 必要なパッケージをインストール
# RUN apt-get update && apt-get install -y python3.12 python3-pip python3-venv nginx mysql-client
RUN apt-get update && apt-get install -y python3.12 python3-pip python3-venv nginx mysql-client pkg-config libmysqlclient-dev

# アプリケーションのセットアップ
RUN mkdir /django
WORKDIR /django
COPY requirements.txt ./
# COPY .env ./
COPY docker-entrypoint.sh /django

# Python環境の設定
RUN python3 -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

# Nginxの設定ファイルをコピー
COPY nginx/nginx.conf /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default  # デフォルト設定を無効化

# ポートの公開
EXPOSE 80 8080

# エントリーポイントスクリプトの実行
ENTRYPOINT ["/django/docker-entrypoint.sh"]
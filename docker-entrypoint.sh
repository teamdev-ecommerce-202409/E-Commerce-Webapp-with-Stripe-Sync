#!/bin/bash

# 環境に応じて処理を分岐
if [ "$DJANGO_ENV" = "production" ]; then
    # RDSを使用している場合の処理 (本番環境)
    until mysqladmin ping -h"${RDS_HOST}" -u"${RDS_USER}" -p"${RDS_PASSWORD}" --silent; do
        echo 'Waiting for RDS MySQL to be ready...'
        sleep 1
    done

    /django/venv/bin/python3 manage.py migrate
    nginx -g 'daemon off;'
else
    # 開発環境の処理
    /django/venv/bin/python3 manage.py runserver 0.0.0.0:8080
fi
#!/bin/bash
if [ ! -d "/var/lib/mysql/mysql" ]; then
    echo "Initializing MySQL data directory..."
    mysqld --initialize-insecure --user=mysql --datadir=/var/lib/mysql
fi

mysqld &

until mysqladmin ping --silent; do
    echo 'Waiting for mysqld to be ready...'
    sleep 1
done

if /django/venv/bin/python3 manage.py createdb; then
    echo "Database created successfully."
else
    echo "Failed to create database." >&2
    exit 1
fi

if /django/venv/bin/python3 manage.py migrate; then
    echo "Migration done successfully."
else
    echo "Failed to migrate." >&2
    exit 1
fi

if /django/venv/bin/python3 manage.py runserver 0.0.0.0:8080; then
    echo "Server start on 0.0.0.0:8080"
else
    echo "Failed to start server." >&2
    exit 1
fi

exec "$@"

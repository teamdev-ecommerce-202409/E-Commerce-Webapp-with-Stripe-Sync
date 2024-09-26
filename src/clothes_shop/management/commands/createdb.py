import os
from pathlib import Path

import environ
import MySQLdb
from django.core.management.base import BaseCommand
from MySQLdb import OperationalError

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))


class Command(BaseCommand):
    help = "Create database"

    def handle(self, *args, **options):
        rootUserPassword = env("MYSQL_ROOT_PASSWORD")
        dbName = env("MYSQL_DB_NAME")
        testDbName = env("MYSQL_TEST_DB_NAME")
        appUser = env("MYSQL_APP_USER")
        appUserPassword = env("MYSQL_APP_USER_PASSWORD")
        dbHost = env("MYSQL_HOST")

        print("Checking if the database exists...")

        # パスワードなしで接続を試みる
        try:
            db = MySQLdb.connect(host=dbHost, user="root")
            cursor = db.cursor()
            print("Connected without password.")
        except OperationalError:
            # パスワードありで接続を試みる
            try:
                db = MySQLdb.connect(host=dbHost, user="root", passwd=rootUserPassword)
                cursor = db.cursor()
                print("Connected with password.")
            except OperationalError as e:
                print(f"Failed to connect to MySQL server: {e}")
                return

        # データベースの存在を確認
        cursor.execute(f"SHOW DATABASES LIKE '{dbName}'")
        result = cursor.fetchone()
        db.close()

        if result:
            print(f"Database '{dbName}' already exists. Skipping creation.")
            return

        print("Creating database and user...")

        # rootユーザーのパスワード設定とデータベース作成
        try:
            # パスワードなしで再度接続を試みる
            db = MySQLdb.connect(host=dbHost, user="root")
            cursor = db.cursor()
            print("Connected without password for database creation.")
        except OperationalError:
            # パスワードありで接続
            db = MySQLdb.connect(host=dbHost, user="root", passwd=rootUserPassword)
            cursor = db.cursor()
            print("Connected with password for database creation.")

        # 初回起動時のみ root ユーザーのパスワードを設定
        if rootUserPassword and not result:
            cursor.execute(
                "ALTER USER 'root'@'localhost' "
                f"IDENTIFIED WITH mysql_native_password BY '{rootUserPassword}'"
            )
            print("Set root user password.")

        # データベースとユーザーの作成
        cursor.execute(f"CREATE DATABASE {dbName}")
        cursor.execute(f"CREATE USER '{appUser}'@'%' IDENTIFIED BY '{appUserPassword}'")
        cursor.execute(f"GRANT ALL PRIVILEGES ON {dbName}.* TO '{appUser}'@'%'")
        cursor.execute(f"GRANT ALL PRIVILEGES ON {testDbName}.* TO '{appUser}'@'%'")
        cursor.execute("FLUSH PRIVILEGES")
        db.close()
        print("Database and user created successfully.")

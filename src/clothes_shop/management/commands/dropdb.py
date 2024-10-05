import os
from pathlib import Path

import environ
import MySQLdb
from django.core.management.base import BaseCommand

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))


class Command(BaseCommand):
    help = "Drop database"

    def handle(self, *args, **options):
        print("Drop database!")
        rootUserPassword = env("MYSQL_ROOT_PASSWORD")
        dbName = env("MYSQL_DB_NAME")
        db = MySQLdb.connect(host="localhost", user="root", passwd=rootUserPassword)
        cursor = db.cursor()
        sql = f"DROP DATABASE {dbName}"
        cursor.execute(sql)
        db.close()

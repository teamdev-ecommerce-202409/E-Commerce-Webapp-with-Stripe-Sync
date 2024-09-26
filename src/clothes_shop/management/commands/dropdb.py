import MySQLdb
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Drop database"

    def handle(self, *args, **options):
        print("Drop database!")
        db = MySQLdb.connect(host="mysql", user="root", passwd="root")
        cursor = db.cursor()
        sql = "DROP DATABASE django-db"
        cursor.execute(sql)
        db.close()

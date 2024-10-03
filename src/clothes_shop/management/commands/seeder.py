import datetime
import random

from django.core.management.base import BaseCommand
from faker import Faker

from clothes_shop.models import Brand, ClothesType, Product, Size, Target


class Command(BaseCommand):
    help = "Seeds the database with product data using only Faker"

    def handle(self, *args, **kwargs):
        fake = Faker("ja_JP")

        size_name_list = ["S", "M", "L", "XL", "XXL"]
        target_name_list = ["メンズ", "レディース", "キッズ"]
        cloth_type_name_list = ["シャツ", "ズボン", "ジャケット", "アウター"]
        brand_name_list = ["CHANEL", "NIKE", "UNIQLO", "GU", "SHEIN"]

        for name in size_name_list:
            Size.objects.create(name=name)

        for name in target_name_list:
            Target.objects.create(name=name)

        for name in cloth_type_name_list:
            ClothesType.objects.create(name=name)

        for name in brand_name_list:
            Brand.objects.create(name=name)

        size_list = Size.objects.all()
        target_list = Target.objects.all()
        clothes_type_list = ClothesType.objects.all()
        brand_list = Brand.objects.all()

        product_data_count = 100
        for _ in range(product_data_count):
            Product.objects.create(
                size=random.choice(size_list),
                target=random.choice(target_list),
                clothes_type=random.choice(clothes_type_list),
                brand=random.choice(brand_list),
                name=fake.word(),
                description=fake.sentence(),
                category="服",
                price=random.randint(1, 10000),
                release_date=datetime.datetime.strptime("2018-12-05", "%Y-%m-%d"),
                stock_quantity=random.randint(0, 100),
            )

        print("Successfully seeded the database using Faker")

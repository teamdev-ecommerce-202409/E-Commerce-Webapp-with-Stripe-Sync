from datetime import datetime

from django.test import TestCase

from clothes_shop.models import Brand, ClothesType, Product, Size, Target


class ProductModelTest(TestCase):

    def setUp(self):
        self.size = Size.objects.create(name="XL")
        self.target = Target.objects.create(name="メンズ")
        self.cloth_type = ClothesType.objects.create(name="シャツ")
        self.brand = Brand.objects.create(name="NIKE")
        self.product = Product.objects.create(
            size=self.size,
            target=self.target,
            clothes_type=self.cloth_type,
            brand=self.brand,
            name="テスト用につくったシャツ",
            description="てすと",
            category="服",
            price=100,
            release_date=datetime.strptime("2018-12-05", "%Y-%m-%d"),
            stock_quantity=500,
            is_deleted=False,
        )

    def test_product_creation(self):
        self.assertEqual(self.product.size, self.size)
        self.assertEqual(self.product.target, self.target)
        self.assertEqual(self.product.clothes_type, self.cloth_type)
        self.assertEqual(self.product.brand, self.brand)
        self.assertEqual(self.product.name, "テスト用につくったシャツ")
        self.assertEqual(self.product.description, "てすと")
        self.assertEqual(self.product.category, "服")
        self.assertEqual(self.product.price, 100)
        self.assertEqual(self.product.release_date, datetime.strptime("2018-12-05", "%Y-%m-%d"))
        self.assertEqual(self.product.stock_quantity, 500)
        self.assertEqual(self.product.is_deleted, False)

    def test_product_str_method(self):
        self.assertEqual(str(self.product), "テスト用につくったシャツ")

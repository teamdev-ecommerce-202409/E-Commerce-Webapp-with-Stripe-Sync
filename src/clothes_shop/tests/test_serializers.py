import datetime

from django.test import TestCase

from clothes_shop.models import Brand, ClothesType, Product, Size, Target
from clothes_shop.serializers import ProductSerializer


class ProductSerializerTest(TestCase):

    def setUp(self):
        self.size = Size.objects.create(name="XL")
        self.target = Target.objects.create(target_type="メンズ")
        self.cloth_type = ClothesType.objects.create(name="シャツ")
        self.brand = Brand.objects.create(name="NIKE")
        self.product = Product.objects.create(
            size="XL",
            target="メンズ",
            clothes_type="シャツ",
            brand="NIKE",
            name="テスト用につくったシャツ",
            description="てすと",
            category="服",
            price=100,
            release_date=datetime.strptime("2018-12-05", "%Y-%m-%d"),
            stock_quantity=500,
            is_deleted=False,
        )

    def test_product_serializer_contains_expected_fields(self):
        """シリアライザが期待されるフィールドを含んでいるかテスト"""
        serializer = ProductSerializer(self.product)
        data = serializer.data
        self.assertEqual(
            set(data.keys()),
            set(
                [
                    "id",
                    "name",
                    "description",
                    "price",
                    "stock_quantity",
                    "release_date",
                    "size",
                    "target",
                    "clothes_type",
                    "brand",
                    "category",
                    "created_at",
                    "updated_at",
                ]
            ),
        )

    def test_product_serializer_field_content(self):
        """シリアライザが正しい内容をシリアライズできるかテスト"""
        serializer = ProductSerializer(self.product)
        data = serializer.data
        self.assertEqual(data["size"], self.product.size)
        self.assertEqual(data["target"], self.product.target)
        self.assertEqual(data["clothes_type"], self.product.clothes_type)
        self.assertEqual(data["brand"], self.product.brand)
        self.assertEqual(data["name"], self.product.name)
        self.assertEqual(data["description"], self.product.description)
        self.assertEqual(float(data["price"]), self.product.price)
        self.assertEqual(int(data["stock_quantity"]), self.product.stock_quantity)
        self.assertEqual(data["release_date"], self.product.release_date)
        self.assertEqual(data["category"], self.product.category)

    def test_product_serializer_valid_data(self):
        """シリアライザが正しいデータからオブジェクトを作成できるかテスト"""
        valid_data = {
            "name": "test",
            "description": "hello",
            "price": 100.02,
            "stock_quantity": 10,
            "release_date": datetime.strptime("2018-12-05", "%Y-%m-%d"),
            "size": "S",
            "target": "レディース",
            "clothes_type": "ジャケット",
            "brand": "CHANEL",
            "category": "服",
        }
        serializer = ProductSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        product = serializer.save()
        self.assertEqual(product.name, valid_data["name"])
        self.assertEqual(product.description, valid_data["description"])
        self.assertEqual(product.price, float(valid_data["price"]))
        self.assertEqual(product.stock_quantity, int(valid_data["stock_quantity"]))
        self.assertEqual(product.release_date, valid_data["release_date"])
        self.assertEqual(product.size, valid_data["size"])
        self.assertEqual(product.target, valid_data["target"])
        self.assertEqual(product.clothes_type, valid_data["clothes_type"])
        self.assertEqual(product.brand, valid_data["brand"])
        self.assertEqual(product.category, valid_data["category"])

    def test_product_serializer_invalid_data(self):
        """無効なデータがバリデーションエラーを引き起こすかテスト"""
        invalid_data = {
            "name": "test",
            "description": "hello",
            "price": "100.02",
            "stock_quantity": 10,
            "release_date": datetime.strptime("2018-12-05", "%Y-%m-%d"),
            "size": "S",
            "target": "レディース",
            "clothes_type": "ジャケット",
            "brand": "CHANEL",
            "category": "服",
        }
        serializer = ProductSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("stock_quantity", serializer.errors)

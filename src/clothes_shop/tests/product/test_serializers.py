from datetime import datetime, timedelta

from django.test import TestCase
from django.utils import timezone

from clothes_shop.models import Brand, ClothesType, Product, Size, Target
from clothes_shop.serializers import (
    BrandSerializer,
    ClothesTypeSerializer,
    ProductSerializer,
    SizeSerializer,
    TargetSerializer,
)


class ProductAndRelatedSerializerTest(TestCase):

    def setUp(self):
        self.size = Size.objects.create(name="XL")
        self.target = Target.objects.create(name="メンズ")
        self.cloth_type = ClothesType.objects.create(name="シャツ")
        self.brand = Brand.objects.create(name="NIKE")

        # デフォルトのリリース日
        self.one_week_ago = timezone.now() - timedelta(weeks=1)
        self.product = Product.objects.create(
            size=self.size,
            target=self.target,
            clothes_type=self.cloth_type,
            brand=self.brand,
            name="テスト用につくったシャツ",
            description="てすと",
            category="服",
            price=100,
            release_date=timezone.make_aware(datetime.strptime("2018-12-05", "%Y-%m-%d")),
            stock_quantity=500,
            is_deleted=False,
        )
        self.productSerializer = ProductSerializer(self.product)
        self.sizeSerializer = SizeSerializer(self.size)
        self.targetSerializer = TargetSerializer(self.target)
        self.clothesTypeSerializer = ClothesTypeSerializer(self.cloth_type)
        self.brandSerializer = BrandSerializer(self.brand)

    def test_product_serializer_contains_expected_fields(self):
        """シリアライザが期待されるフィールドを含んでいるかテスト"""
        self.assertEqual(
            set(self.productSerializer.data.keys()),
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
                    "is_deleted",
                    "created_at",
                    "updated_at",
                ]
            ),
        )
        self.assertEqual(
            set(self.sizeSerializer.data.keys()),
            set(["id", "name", "created_at", "updated_at"]),
        )
        self.assertEqual(
            set(self.targetSerializer.data.keys()),
            set(["id", "name", "created_at", "updated_at"]),
        )
        self.assertEqual(
            set(self.clothesTypeSerializer.data.keys()),
            set(["id", "name", "created_at", "updated_at"]),
        )
        self.assertEqual(
            set(self.brandSerializer.data.keys()),
            set(["id", "name", "created_at", "updated_at"]),
        )

    def test_product_serializer_field_content(self):
        """シリアライザが正しい内容をシリアライズできるかテスト"""
        self.assertEqual(self.productSerializer.data["size"], self.sizeSerializer.data["id"])
        self.assertEqual(self.productSerializer.data["target"], self.targetSerializer.data["id"])
        self.assertEqual(
            self.productSerializer.data["clothes_type"], self.clothesTypeSerializer.data["id"]
        )
        self.assertEqual(self.productSerializer.data["brand"], self.brandSerializer.data["id"])
        self.assertEqual(self.productSerializer.data["name"], self.product.name)
        self.assertEqual(self.productSerializer.data["description"], self.product.description)
        self.assertEqual(float(self.productSerializer.data["price"]), self.product.price)
        self.assertEqual(
            int(self.productSerializer.data["stock_quantity"]), self.product.stock_quantity
        )

        # タイムゾーンを合わせてから比較
        serialized_date_str = self.productSerializer.data["release_date"].rstrip("Z")
        expected_date_str = self.product.release_date.astimezone(
            timezone.get_current_timezone()
        ).isoformat()
        self.assertEqual(serialized_date_str, expected_date_str)
        self.assertEqual(self.productSerializer.data["category"], self.product.category)

    def test_product_serializer_valid_data(self):
        """シリアライザが正しいデータからオブジェクトを作成できるかテスト"""
        valid_data = {
            "name": "test",
            "description": "hello",
            "price": 100.02,
            "stock_quantity": 10,
            "release_date": timezone.make_aware(datetime.strptime("2018-12-05", "%Y-%m-%d")),
            "size": self.size.id,
            "target": self.target.id,
            "clothes_type": self.cloth_type.id,
            "brand": self.brand.id,
            "category": "服",
        }
        productSerializerValid = ProductSerializer(data=valid_data)
        self.assertTrue(productSerializerValid.is_valid())
        product = productSerializerValid.save()
        self.assertEqual(product.name, valid_data["name"])
        self.assertEqual(product.description, valid_data["description"])
        self.assertEqual(float(product.price), float(valid_data["price"]))
        self.assertEqual(product.stock_quantity, int(valid_data["stock_quantity"]))
        # self.assertEqual(product.release_date, valid_data["release_date"])
        self.assertEqual(product.size.id, valid_data["size"])
        self.assertEqual(product.target.id, valid_data["target"])
        self.assertEqual(product.clothes_type.id, valid_data["clothes_type"])
        self.assertEqual(product.brand.id, valid_data["brand"])
        self.assertEqual(product.category, valid_data["category"])

    def test_product_serializer_invalid_data(self):
        """無効なデータがバリデーションエラーを引き起こすかテスト"""
        invalid_data = {
            "name": "test",
            "description": "hello",
            "price": 100.02,
            "stock_quantity": 10,
            "release_date": 123,
            "size": self.size.id,
            "target": self.target.id,
            "clothes_type": self.cloth_type.id,
            "brand": self.brand.id,
            "category": "服",
        }
        serializer = ProductSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("release_date", serializer.errors)

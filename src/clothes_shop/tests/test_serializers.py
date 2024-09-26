from django.test import TestCase

from clothes_shop.models import Clothes
from clothes_shop.serializers import ClothesSerializer


class ClothesSerializerTest(TestCase):

    def setUp(self):
        self.cloth = Clothes.objects.create(
            name="T-shirt", price=1500.00, description="A comfortable cotton T-shirt"
        )

    def test_clothes_serializer_contains_expected_fields(self):
        """シリアライザが期待されるフィールドを含んでいるかテスト"""
        serializer = ClothesSerializer(self.cloth)
        data = serializer.data
        self.assertEqual(set(data.keys()), set(["id", "name", "price", "description"]))

    def test_clothes_serializer_field_content(self):
        """シリアライザが正しい内容をシリアライズできるかテスト"""
        serializer = ClothesSerializer(self.cloth)
        data = serializer.data
        self.assertEqual(data["name"], self.cloth.name)
        self.assertEqual(float(data["price"]), self.cloth.price)
        self.assertEqual(data["description"], self.cloth.description)

    def test_clothes_serializer_valid_data(self):
        """シリアライザが正しいデータからオブジェクトを作成できるかテスト"""
        valid_data = {"name": "Jeans", "price": "2500.00", "description": "Comfortable denim jeans"}
        serializer = ClothesSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        cloth = serializer.save()
        self.assertEqual(cloth.name, valid_data["name"])
        self.assertEqual(cloth.price, float(valid_data["price"]))
        self.assertEqual(cloth.description, valid_data["description"])

    def test_clothes_serializer_invalid_data(self):
        """無効なデータがバリデーションエラーを引き起こすかテスト"""
        invalid_data = {
            "name": "",
            "price": "hooge",
            "description": 100,
        }
        serializer = ClothesSerializer(data=invalid_data)
        print(invalid_data["description"])
        print(isinstance(invalid_data["description"], str))
        print(serializer)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertIn("price", serializer.errors)
        self.assertIn("description", serializer.errors)

import logging
import random
from datetime import datetime, timedelta

from django.urls import reverse
from django.utils import timezone
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from clothes_shop.models import (
    Brand,
    CartItem,
    ClothesType,
    Product,
    Size,
    Target,
    User,
)

logger = logging.getLogger(__name__)


class CartItemListCreateViewTests(APITestCase):
    def setUp(self):
        fake = Faker("ja_JP")
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
            release_date=timezone.make_aware(datetime.strptime("2018-12-05", "%Y-%m-%d")),
            stock_quantity=500,
            is_deleted=False,
        )
        self.user = User.objects.create(
            name=fake.name(),
            email_address=fake.email(),
            role="registered",
            email_validated_at=timezone.now(),
            address=fake.address(),
        )
        self.quantity = random.randint(1, 5)
        self.cartItem = CartItem.objects.create(
            user=self.user, product=self.product, quantity=self.quantity
        )
        self.list_url = reverse("clothes_shop:cartitem-list-create")

    def test_get_value_error(self):
        query_params = {"error": "hogehoge"}
        response = self.client.get(self.list_url, query_params=query_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expectedMsg = "userIdを設定してください。"
        self.assertEqual(response.data["message"], expectedMsg)

    def test_post_value_error_wihtout_params(self):
        data = {"error": "hogehoge"}
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expectedMsg = "userId、product_idを設定してください。"
        self.assertEqual(response.data["message"], expectedMsg)

    def test_post_value_error_notExist_user(self):
        data = {"user_id": 9999, "product_id": self.product.id}
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expectedMsg = "指定のuser_id:9999は存在しません。"
        self.assertEqual(response.data["message"], expectedMsg)

    def test_post_value_error_notExist_product(self):
        data = {"user_id": self.user.id, "product_id": 9999}
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expectedMsg = "指定のproduct_id:9999は存在しません。"
        self.assertEqual(response.data["message"], expectedMsg)

    def test_delete_value_error_wihtout_params(self):
        data = {"error": "hogehoge"}
        response = self.client.delete(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expectedMsg = "userId、product_idを設定してください。"
        self.assertEqual(response.data["message"], expectedMsg)

    def test_delete_value_error_notExist_user(self):
        data = {"user_id": 9999, "product_id": self.product.id}
        response = self.client.delete(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expectedMsg = "指定のuser_id:9999は存在しません。"
        self.assertEqual(response.data["message"], expectedMsg)

    def test_delete_value_error_notExist_product(self):
        data = {"user_id": self.user.id, "product_id": 9999}
        response = self.client.delete(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        expectedMsg = "指定のproduct_id:9999は存在しません。"
        self.assertEqual(response.data["message"], expectedMsg)

    # def test_post_invalid_serializer(self):
    # postロジックを考えてから解放
    #     data = {
    #         "user_pk": "test",
    #         "product_pk": "hello",
    #         "error_quantity": "服",
    #     }
    #     response = self.client.post(self.list_url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

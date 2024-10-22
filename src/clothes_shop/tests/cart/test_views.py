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
from clothes_shop.serializers import CartItemSerializer


class CartItemTests(APITestCase):
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

    def test_get_cartItems_by_User(self):
        response = self.client.get(self.list_url, {"user": self.user.id})
        cartItems = CartItem.objects.filter(user_id=self.user.id)

        serializer = CartItemSerializer(cartItems, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

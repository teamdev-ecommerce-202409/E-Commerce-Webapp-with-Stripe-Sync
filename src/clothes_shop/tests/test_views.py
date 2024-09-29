import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from clothes_shop.models import Brand, ClothesType, Product, Size, Target
from clothes_shop.serializers import ProductListSerializer, ProductSerializer


class ProductTests(APITestCase):

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
        self.list_url = reverse("clothes_shop:product-list")
        self.detail_url = reverse("clothes_shop:product-detail", kwargs={"pk": self.product.id})

    def test_get__list(self):
        response = self.client.get(self.list_url)
        product = Product.objects.all()
        serializer = ProductListSerializer(product, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get__individual(self):
        response = self.client.get(self.detail_url)
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_cloth(self):
        data = {
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
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product_created = Product.objects.get(id=response.data["id"])
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(product_created.name, "test")
        self.assertEqual(product_created.description, "test_create_cloth")
        self.assertEqual(product_created.price, 100.02)
        self.assertEqual(product_created.stock_quantity, 10)
        self.assertEqual(product_created.release_date, datetime.strptime("2018-12-05", "%Y-%m-%d"))
        self.assertEqual(product_created.size, "S")
        self.assertEqual(product_created.target, "レディース")
        self.assertEqual(product_created.clothes_type, "ジャケット")
        self.assertEqual(product_created.brand, "CHANEL")
        self.assertEqual(product_created.category, "服")

    def test_update_cloth(self):
        data = {
            "name": "updated_product",
            "description": "hello",
            "price": 9000,
            "stock_quantity": 1780,
            "release_date": datetime.strptime("2016-12-05", "%Y-%m-%d"),
            "size": "M",
            "target": "メンズ",
            "clothes_type": "コート",
            "brand": "MIZUNO",
            "category": "服",
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(self.product.name, "updated_self.product")
        self.assertEqual(self.product.description, "hello")
        self.assertEqual(self.product.price, 9000)
        self.assertEqual(self.product.stock_quantity, 1780)
        self.assertEqual(self.product.release_date, datetime.strptime("2016-12-05", "%Y-%m-%d"))
        self.assertEqual(self.product.size, "M")
        self.assertEqual(self.product.target, "メンズ")
        self.assertEqual(self.product.clothes_type, "コート")
        self.assertEqual(self.product.brand, "MIZUNO")
        self.assertEqual(self.product.category, "服")

    def test_delete_cloth(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

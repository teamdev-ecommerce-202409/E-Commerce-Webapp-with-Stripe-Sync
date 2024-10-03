from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from clothes_shop.models import Brand, ClothesType, Product, Size, Target
from clothes_shop.serializers import ProductSerializer


class ProductTests(APITestCase):

    def setUp(self):
        self.size = Size.objects.create(name="XL")
        self.target = Target.objects.create(name="メンズ")
        self.cloth_type = ClothesType.objects.create(name="シャツ")
        self.brand = Brand.objects.create(name="NIKE")
        self.product_1 = Product.objects.create(
            size=self.size,
            target=self.target,
            clothes_type=self.cloth_type,
            brand=self.brand,
            name="テスト用につくったシャツ１",
            description="てすと",
            category="服",
            price=100,
            release_date=datetime.strptime("2018-12-05", "%Y-%m-%d"),
            stock_quantity=500,
            is_deleted=False,
        )
        self.product_2 = Product.objects.create(
            size=self.size,
            target=self.target,
            clothes_type=self.cloth_type,
            brand=self.brand,
            name="テスト用につくったシャツ２",
            description="てすと",
            category="服",
            price=100,
            release_date=datetime.strptime("2018-12-05", "%Y-%m-%d"),
            stock_quantity=500,
            is_deleted=False,
        )
        self.list_url = reverse("clothes_shop:product-list")
        self.detail_url = reverse("clothes_shop:product-detail", kwargs={"pk": self.product_1.id})

    # フィルタリング機能のテストは煩雑になるため、別ファイルに切り出す
    # def test_get_list(self):
    #     response = self.client.get(self.list_url)
    #     product = Product.objects.all()
    #     serializer = ProductSerializer(product, many=True)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data, serializer.data)

    def test_get_individual(self):
        response = self.client.get(self.detail_url)
        product = Product.objects.get(pk=self.product_1.id)
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
            "size": self.size.id,
            "target": self.target.id,
            "clothes_type": self.cloth_type.id,
            "brand": self.brand.id,
            "category": "服",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product_created = Product.objects.get(id=response.data["id"])
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(product_created.name, "test")
        self.assertEqual(product_created.description, "hello")
        self.assertEqual(float(product_created.price), 100.02)
        self.assertEqual(product_created.stock_quantity, 10)
        # self.assertEqual(product_created.release_date, datetime.strptime("2018-12-05", "%Y-%m-%d"))
        self.assertEqual(product_created.size.name, "XL")
        self.assertEqual(product_created.target.name, "メンズ")
        self.assertEqual(product_created.clothes_type.name, "シャツ")
        self.assertEqual(product_created.brand.name, "NIKE")
        self.assertEqual(product_created.category, "服")

    def test_update_cloth(self):
        data = {
            "name": "updated_product",
            "description": "hello",
            "price": 9000,
            "stock_quantity": 1780,
            "release_date": datetime.strptime("2016-12-05", "%Y-%m-%d"),
            "size": self.size.id,
            "target": self.target.id,
            "clothes_type": self.cloth_type.id,
            "brand": self.brand.id,
            "category": "服",
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product_1.refresh_from_db()
        self.assertEqual(self.product_1.name, "updated_product")
        self.assertEqual(self.product_1.description, "hello")
        self.assertEqual(self.product_1.price, 9000)
        self.assertEqual(self.product_1.stock_quantity, 1780)
        # self.assertEqual(self.product_1.release_date, datetime.strptime("2016-12-05", "%Y-%m-%d"))
        self.assertEqual(self.product_1.size.name, "XL")
        self.assertEqual(self.product_1.target.name, "メンズ")
        self.assertEqual(self.product_1.clothes_type.name, "シャツ")
        self.assertEqual(self.product_1.brand.name, "NIKE")
        self.assertEqual(self.product_1.category, "服")

    def test_delete_cloth(self):
        product_count_total = 2
        self.assertEqual(Product.objects.count(), product_count_total)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), product_count_total - 1)

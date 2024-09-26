from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from clothes_shop.models import Clothes
from clothes_shop.serializers import ClothesSerializer


class ClothesTests(APITestCase):

    def setUp(self):
        self.cloth = Clothes.objects.create(name="T-shirt", price=1000, description="hoge")
        self.list_url = reverse("clothes_shop:list")
        self.detail_url = reverse("clothes_shop:detail", kwargs={"pk": self.cloth.pk})

    def test_get_clothes_list(self):
        response = self.client.get(self.list_url)
        clothes = Clothes.objects.all()
        serializer = ClothesSerializer(clothes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_cloth(self):
        data = {"name": "Jeans", "price": 5000, "description": "test_create_cloth"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Clothes.objects.count(), 2)
        self.assertEqual(Clothes.objects.get(id=response.data["id"]).name, "Jeans")
        self.assertEqual(Clothes.objects.get(id=response.data["id"]).price, 5000)
        self.assertEqual(
            Clothes.objects.get(id=response.data["id"]).description, "test_create_cloth"
        )

    def test_update_cloth(self):
        data = {"name": "Updated T-shirt", "price": 1500}
        response = self.client.put(self.detail_url, data)
        self.cloth.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.cloth.name, "Updated T-shirt")
        self.assertEqual(self.cloth.price, 1500)

    def test_delete_cloth(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Clothes.objects.count(), 0)

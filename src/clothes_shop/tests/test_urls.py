from django.test import TestCase
from django.urls import resolve, reverse

from clothes_shop.views import product_detail, product_list


class TestsUrls(TestCase):
    def test_list_url(self):
        url = reverse("clothes_shop:product-list")
        self.assertEqual(resolve(url).func, product_list)

    def test_detail_url(self):
        url = reverse("clothes_shop:product-detail", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func, product_detail)

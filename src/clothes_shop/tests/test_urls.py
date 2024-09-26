from django.test import TestCase
from django.urls import resolve, reverse

from clothes_shop.views import clothes_detail, clothes_list


class TestsUrls(TestCase):
    def test_list_url(self):
        url = reverse("clothes_shop:list")
        self.assertEqual(resolve(url).func, clothes_list)

    def test_detail_url(self):
        url = reverse("clothes_shop:detail", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func, clothes_detail)

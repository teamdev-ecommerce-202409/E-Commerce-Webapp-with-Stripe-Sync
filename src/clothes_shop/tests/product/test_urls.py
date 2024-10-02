from django.test import TestCase
from django.urls import resolve, reverse

from clothes_shop.views import (
    ProductDetailView,
    ProductListFilteredView,
    ProductListView,
)


class TestsUrls(TestCase):
    def test_list_url(self):
        url = reverse("clothes_shop:product-list")
        self.assertEqual(resolve(url).func.view_class, ProductListView)

    def test_detail_url(self):
        url = reverse("clothes_shop:product-detail", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, ProductDetailView)

    def test_filtered_list_url(self):
        url = reverse("clothes_shop:product-list-filtered")
        self.assertEqual(resolve(url).func.view_class, ProductListFilteredView)

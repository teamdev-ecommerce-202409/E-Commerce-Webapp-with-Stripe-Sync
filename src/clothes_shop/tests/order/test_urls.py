from django.urls import resolve, reverse
from django.test import TestCase
from clothes_shop.views import OrderListCreateView, OrderDetailView

class OrderUrlsTest(TestCase):

    def test_order_list_create_url(self):
        url = reverse("clothes_shop:order-list-create")
        self.assertEqual(resolve(url).func.view_class, OrderListCreateView)

    def test_order_detail_url(self):
        url = reverse("clothes_shop:order-detail", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, OrderDetailView)

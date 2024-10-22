from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from clothes_shop.models import Order, OrderItem, Size, User, Product, Size, Target, ClothesType, Brand

class OrderListCreateViewTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create(
            name="テストユーザー",
            email_address="testuser@example.com",
            role="customer",
            address="123 テストストリート"
        )
        self.order_list_url = reverse("clothes_shop:order-list-create")
    
    def test_get_order_list(self):
        response = self.client.get(self.order_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_post_create_order(self):
        order_data = {
            "user": self.user.id,
            "order_status": "pending",
            "total_price": 150.00
        }
        response = self.client.post(self.order_list_url, data=order_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class OrderDetailViewTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create(
            name="テストユーザー",
            email_address="testuser@example.com",
            role="customer",
            address="123 テストストリート"
        )

        self.size = Size.objects.create(name="L")
        self.target = Target.objects.create(name="メンズ")
        self.clothes_type = ClothesType.objects.create(name="シャツ")
        self.brand = Brand.objects.create(name="UNIQLO")
        
        self.product = Product.objects.create(
            size=self.size,
            target=self.target,
            clothes_type=self.clothes_type,
            brand=self.brand,
            name="Test Product",
            description="Test Description",
            category="Test Category",
            price=100.00,
            stock_quantity=10,
            release_date="2024-01-01"
        )

        self.order = Order.objects.create(
            user=self.user,
            order_status="pending",
            total_price=100.00
        )
        self.order_detail_url = reverse("clothes_shop:order-detail", kwargs={"pk": self.order.id})
    
    def test_get_order_detail(self):
        response = self.client.get(self.order_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

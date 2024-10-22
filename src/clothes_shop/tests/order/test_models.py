from django.test import TestCase
from clothes_shop.models import Order, User

class OrderModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create(
            name="テストユーザー",
            email_address="testuser@example.com",
            role="customer",
            address="123 テストストリート"
        )
        self.order = Order.objects.create(
            user=self.user,
            order_status="pending",
            total_price=100.00
        )
    
    def test_order_creation(self):
        self.assertEqual(self.order.user.name, "テストユーザー")
        self.assertEqual(self.order.order_status, "pending")
        self.assertEqual(self.order.total_price, 100.00)
    
    def test_order_str_method(self):
        self.assertEqual(str(self.order), f"Order object ({self.order.id})")

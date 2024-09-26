from django.test import TestCase

from clothes_shop.models import Clothes


class ClothesModelTest(TestCase):

    def setUp(self):
        self.cloth = Clothes.objects.create(
            name="T-shirt", price=1500.00, description="A comfortable cotton T-shirt"
        )

    def test_clothes_creation(self):
        self.assertEqual(self.cloth.name, "T-shirt")
        self.assertEqual(self.cloth.price, 1500.00)
        self.assertEqual(self.cloth.description, "A comfortable cotton T-shirt")
        self.assertIsInstance(self.cloth.name, str)
        self.assertIsInstance(self.cloth.price, float)
        self.assertIsInstance(self.cloth.description, str)

    def test_clothes_str_method(self):
        self.assertEqual(str(self.cloth), "T-shirt")

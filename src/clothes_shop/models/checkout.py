from django.db import models

from clothes_shop.models.user import User


class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_checkout_session_id = models.CharField(max_length=255, unique=True)
    shipping_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

from rest_framework import serializers

from clothes_shop.models.checkout import Checkout


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ("user", "stripe_checkout_session_id", "shipping_date")

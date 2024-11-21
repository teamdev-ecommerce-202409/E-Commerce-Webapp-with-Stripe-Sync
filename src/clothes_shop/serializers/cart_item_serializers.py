from rest_framework import serializers


class CartItemSerializer(serializers.Serializer):
    product_id = serializers.CharField(max_length=255)
    amount = serializers.IntegerField()


class CartItemListSerializer(serializers.ListSerializer):
    child = CartItemSerializer()
    allow_empty = False

from rest_framework import serializers

from .models import (
    Brand,
    CartItem,
    Clothes,
    ClothesType,
    Favorite,
    Order,
    OrderItem,
    Payment,
    Product,
    Rating,
    Shipping,
    Size,
    Target,
    User,
    WishList,
)


# Clothes Serializer
class ClothesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothes
        fields = ("id", "name", "price", "description")

    def validate_description(self, value):
        if not isinstance(self.initial_data.get("description"), str):
            raise serializers.ValidationError("Description must be a string.")
        return value


# Product Serializer (for detail view)
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "description",
            "price",
            "stock_quantity",
            "release_date",
            "size",
            "target",
            "clothes_type",
            "brand",
        )


# Product List Serializer (for listing products)
class ProductListSerializer(serializers.ListSerializer):
    child = ProductSerializer()

    def create(self, validated_data):
        return [Product(**item) for item in validated_data]


# Order Serializer (for detail view)
class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.StringRelatedField(many=True)

    class Meta:
        model = Order
        fields = ("id", "user", "order_date", "order_status", "total_price", "order_items")


# Order List Serializer (for listing orders)
class OrderListSerializer(serializers.ListSerializer):
    child = OrderSerializer()

    def create(self, validated_data):
        return [Order(**item) for item in validated_data]


# Rating Serializer (for detail view)
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("id", "user", "product", "rating", "comment", "created_at")


# Rating List Serializer (for listing ratings)
class RatingListSerializer(serializers.ListSerializer):
    child = RatingSerializer()

    def create(self, validated_data):
        return [Rating(**item) for item in validated_data]


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "user_name", "email_address", "role", "address")


# Favorite Serializer
class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ("user", "product")


# WishList Serializer
class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ("user", "product", "is_public")


# CartItem Serializer
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ("user", "product", "quantity")


# OrderItem Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("order", "product", "quantity", "unit_price")


# Payment Serializer
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("order", "payment_date", "payment_option", "payment_status")


# Shipping Serializer
class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = (
            "order",
            "shipping_tracking_number",
            "shipping_date",
            "shipping_address",
            "address_code",
        )


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ("id", "size_name", "created_at", "updated_at")


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ("id", "target_type", "created_at", "updated_at")


class ClothesTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothesType
        fields = ("id", "clothes_type_name", "created_at", "updated_at")


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("id", "brand_name", "created_at", "updated_at")

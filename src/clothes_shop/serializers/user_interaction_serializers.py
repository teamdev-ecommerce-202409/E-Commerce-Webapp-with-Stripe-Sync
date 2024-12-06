from rest_framework import serializers

from clothes_shop.models.product import Product
from clothes_shop.models.user_interaction import Favorite, Review, WishList
from clothes_shop.serializers.product_serializers import ProductSerializer


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "id",
            "user",
            "product",
            "rating",
            "comment",
            "created_at",
            "updated_at",
        )


class FavoriteSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)
    product_pk = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = Favorite
        fields = ("user", "product", "product_pk")

    def get_product(self, obj: Favorite):
        return ProductSerializer(obj.product).data


class WishListSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)
    product_pk = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = WishList
        fields = ("user", "product", "product_pk", "is_public")

    def get_product(self, obj: WishList):
        return ProductSerializer(obj.product).data


class AddressSerializer(serializers.Serializer):
    state = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=100)
    line1 = serializers.CharField(max_length=255)
    line2 = serializers.CharField(max_length=255, required=False, allow_blank=True)
    postal_code = serializers.CharField(max_length=20)

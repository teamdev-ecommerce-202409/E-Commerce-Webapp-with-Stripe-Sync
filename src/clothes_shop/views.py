from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
from .serializers import (
    BrandSerializer,
    CartItemSerializer,
    ClothesSerializer,
    ClothesTypeSerializer,
    FavoriteSerializer,
    OrderItemSerializer,
    OrderSerializer,
    PaymentSerializer,
    ProductSerializer,
    RatingSerializer,
    ShippingSerializer,
    SizeSerializer,
    TargetSerializer,
    UserSerializer,
    WishListSerializer,
)


@api_view(["GET", "POST"])
def clothes_list(request):
    """
    List all clothes, or create a cloth.
    """
    if request.method == "GET":
        clothes = Clothes.objects.all()
        serializer = ClothesSerializer(clothes, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ClothesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT", "DELETE"])
def clothes_detail(request, pk):
    """
    Update or delete a cloth.
    """
    try:
        cloth = Clothes.objects.get(pk=pk)
    except Clothes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = ClothesSerializer(cloth, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        cloth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# # Clothes API Views

# class ClothesListCreateView(generics.ListCreateAPIView):
#     queryset = Clothes.objects.all()
#     serializer_class = ClothesSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             self.perform_create(serializer)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ClothesDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Clothes.objects.all()
#     serializer_class = ClothesSerializer

#     def get_object(self):
#         return get_object_or_404(Clothes, pk=self.kwargs.get('pk'))

# Product API Views


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_object(self):
        return get_object_or_404(Product, pk=self.kwargs.get("pk"))


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs.get("pk"))


class RatingListCreateView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class RatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_object(self):
        return get_object_or_404(Rating, pk=self.kwargs.get("pk"))


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs.get("pk"))


class FavoriteListCreateView(generics.ListCreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class FavoriteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_object(self):
        return get_object_or_404(Favorite, pk=self.kwargs.get("pk"))


class WishListListCreateView(generics.ListCreateAPIView):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer


class WishListDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer

    def get_object(self):
        return get_object_or_404(WishList, pk=self.kwargs.get("pk"))


class CartItemListCreateView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_object(self):
        return get_object_or_404(CartItem, pk=self.kwargs.get("pk"))


class OrderItemListCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def get_object(self):
        return get_object_or_404(OrderItem, pk=self.kwargs.get("pk"))


class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_object(self):
        return get_object_or_404(Payment, pk=self.kwargs.get("pk"))


class ShippingListCreateView(generics.ListCreateAPIView):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer


class ShippingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer

    def get_object(self):
        return get_object_or_404(Shipping, pk=self.kwargs.get("pk"))


class SizeListCreateView(generics.ListCreateAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class SizeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

    def get_object(self):
        return get_object_or_404(Size, pk=self.kwargs.get("pk"))


class TargetListCreateView(generics.ListCreateAPIView):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer


class TargetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

    def get_object(self):
        return get_object_or_404(Target, pk=self.kwargs.get("pk"))


class ClothesTypeListCreateView(generics.ListCreateAPIView):
    queryset = ClothesType.objects.all()
    serializer_class = ClothesTypeSerializer


class ClothesTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ClothesType.objects.all()
    serializer_class = ClothesTypeSerializer

    def get_object(self):
        return get_object_or_404(ClothesType, pk=self.kwargs.get("pk"))


class BrandListCreateView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get_object(self):
        return get_object_or_404(Brand, pk=self.kwargs.get("pk"))


@api_view(["GET"])
def category_list(request):
    """
    Retrieve all category data: Sizes, Targets, Clothes Types, and Brands.
    """
    sizes = Size.objects.all()
    targets = Target.objects.all()
    clothes_types = ClothesType.objects.all()
    brands = Brand.objects.all()

    size_serializer = SizeSerializer(sizes, many=True)
    target_serializer = TargetSerializer(targets, many=True)
    clothes_type_serializer = ClothesTypeSerializer(clothes_types, many=True)
    brand_serializer = BrandSerializer(brands, many=True)

    # すべてのカテゴリデータをまとめて返す
    data = {
        "sizeCatgory": size_serializer.data,
        "targetCatgory": target_serializer.data,
        "typeCatgory": clothes_type_serializer.data,
        "brandCatgory": brand_serializer.data,
    }

    return Response(data)

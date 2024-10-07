from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Brand,
    CartItem,
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


class ProductListView(APIView):
    def get(self, request):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def get_object(self, pk):
        try:
            product = Product.objects.get(pk=pk)
            return product
        except Product.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        product = self.get_object(kwargs.get("pk"))
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        product = self.get_object(kwargs.get("pk"))
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        product = self.get_object(kwargs.get("pk"))
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs.get("pk"))


class RatingListCreateView(generics.ListCreateAPIView):
    serializer_class = RatingSerializer

    def get_queryset(self):
        product_id = self.request.query_params.get("productId")

        if product_id:
            return Rating.objects.filter(product_id=product_id)

        return Rating.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        avg_rating = queryset.aggregate(average=Avg("rating"))["average"]

        if avg_rating is None:
            avg_rating = 0

        serializer = self.get_serializer(queryset.order_by("-created_at"), many=True)

        response_data = {"average_rating": avg_rating, "comments": serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)


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


class CategoryListView(APIView):
    def get(self, request):

        # 全４種のカテゴリのデータを全て返す
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

        return Response(data, status=status.HTTP_200_OK)

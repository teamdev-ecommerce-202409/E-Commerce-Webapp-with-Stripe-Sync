from django.shortcuts import get_object_or_404
from django.utils import timezone
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
        # Home画面からフィルタした製品のリストを取得する

        # クエリパラメータの取得
        size_id = request.query_params.get("size")
        target_id = request.query_params.get("target")
        clothes_type_id = request.query_params.get("clothes_type")
        brand_id = request.query_params.get("brand")
        keyword = request.query_params.get("keyword")

        # フィルタの作成
        filters = {}

        # is_deleted のパラメータ取得
        is_deleted_param = request.query_params.get("is_deleted")

        if is_deleted_param is None:
            # is_deletedがパラメータにない→デフォルトでFalse
            filters["is_deleted"] = False
        else:
            # is_deletedがパラメータにある→フィルタに設定
            filters["is_deleted"] = (
                is_deleted_param.lower() == "true"
            )  # パラメータをいったん小文字にしてから比較することで表記ゆれを調整

        # release_date のパラメータ取得
        release_date_param = request.query_params.get("release_date")

        if release_date_param is None:
            # release_dateがパラメータにない→デフォルトで現在時刻
            filters["release_date__lt"] = timezone.now()
        else:
            # release_dateがパラメータにある→フィルタに設定
            # 文字列を日付に変換
            try:
                # パラメーターをdatetimeに変更
                release_date = timezone.datetime.fromisoformat(release_date_param)
                filters["release_date__lt"] = release_date
            except ValueError:
                # パラメーターをdatetimeに変更するのを失敗＝フォーマットが間違っている
                return Response(
                    {
                        "error": "フォーマットエラー。ISO format (e.g., 2023-09-30T10:00:00)を使用してください"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if size_id:
            filters["size_id"] = size_id
        if target_id:
            filters["target_id"] = target_id
        if clothes_type_id:
            filters["clothes_type_id"] = clothes_type_id
        if brand_id:
            filters["brand_id"] = brand_id

        # フィルタを適用してProductオブジェクトを取得
        products = Product.objects.filter(**filters)

        # keywordのフィルタ追加
        if keyword:
            # 製品名か説明にキーワードが入ることを条件に追加
            products = products.filter(name__icontains=keyword) | products.filter(
                description__icontains=keyword
            )

        # シリアライズしてレスポンスを返す
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

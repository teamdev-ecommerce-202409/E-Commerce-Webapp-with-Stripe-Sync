import logging

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.exceptions import APIException, NotFound
from rest_framework.pagination import PageNumberPagination
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
    Review,
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
    ReviewListSerializer,
    ReviewSerializer,
    ShippingSerializer,
    SizeSerializer,
    TargetSerializer,
    UserSerializer,
    WishListSerializer,
)

logger = logging.getLogger(__name__)


class ProductListView(APIView):
    def get(self, request):
        size_ids = request.query_params.getlist("size[]")
        target_ids = request.query_params.getlist("target[]")
        clothes_type_ids = request.query_params.getlist("clothes_type[]")
        brand_ids = request.query_params.getlist("brand[]")
        keyword = request.query_params.get("keyword")
        is_deleted_param = request.query_params.get("is_deleted")
        release_date_param = request.query_params.get("release_date")

        filters = {}
        if size_ids:
            filters["size_id__in"] = size_ids
        if target_ids:
            filters["target_id__in"] = target_ids
        if clothes_type_ids:
            filters["clothes_type_id__in"] = clothes_type_ids
        if brand_ids:
            filters["brand_id__in"] = brand_ids

        if is_deleted_param is None:
            filters["is_deleted"] = False
        else:
            filters["is_deleted"] = is_deleted_param.lower() == "true"

        if release_date_param is None:
            filters["release_date__lt"] = timezone.now()
        else:
            try:
                release_date = timezone.datetime.fromisoformat(release_date_param)
                filters["release_date__lt"] = release_date
            except ValueError:
                errMsg = (
                    "フォーマットエラー。ISO format (e.g., 2023-09-30T10:00:00)を使用してください。"
                )
                logger.error(errMsg)
                return Response(
                    {"message": errMsg},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        products = Product.objects.filter(**filters).order_by("-release_date")

        if keyword:
            products = products.filter(name__icontains=keyword) | products.filter(
                description__icontains=keyword
            )

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_products = paginator.paginate_queryset(products, request)

        serializer = ProductSerializer(paginated_products, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid() is False:
            logger.error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    def get_product(self, pk):
        try:
            product = Product.objects.get(pk=pk)
            return product
        except Product.DoesNotExist:
            errMsg = f"指定されたID {pk} に紐づく製品が存在しません。"
            logger.error(errMsg)
            raise NotFound(detail=errMsg)
        except Exception as e:
            errMsg = f"想定外のエラーが発生しました: {str(e)}"
            logger.error(errMsg)
            raise APIException(detail=errMsg)

    def get(self, request, *args, **kwargs):
        product = self.get_product(kwargs.get("pk"))
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        product = self.get_product(kwargs.get("pk"))
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if not serializer.is_valid():
            logger.error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        product = self.get_product(kwargs.get("pk"))
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


class ProductReviewListView(generics.ListAPIView):
    serializer_class = ReviewListSerializer

    def get_queryset(self):
        product_id = self.kwargs["product_id"]
        return Review.objects.filter(product_id=product_id)


class UserProductReviewDetailView(APIView):
    def get_product(self, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            return product
        except Product.DoesNotExist:
            errMsg = f"指定されたID {product_id} に紐づく製品が存在しません。"
            logger.error(errMsg)
            raise NotFound(detail=errMsg)
        except Exception as e:
            errMsg = f"想定外のエラーが発生しました: {str(e)}"
            logger.error(errMsg)
            raise APIException(detail=errMsg)

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            errMsg = f"指定されたID {user_id} に紐づくユーザーが存在しません。"
            logger.error(errMsg)
            raise NotFound(detail=errMsg)
        except Exception as e:
            errMsg = f"想定外のエラーが発生しました: {str(e)}"
            logger.error(errMsg)
            raise APIException(detail=errMsg)

    def get(self, request, *args, **kwargs):
        product = self.get_product(kwargs["product_id"])
        user = self.get_user(kwargs["user_id"])
        review = Review.objects.filter(user_id=user.id, product_id=product.id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        product = self.get_product(kwargs["product_id"])
        user = self.get_user(kwargs["user_id"])
        data = {
            "user_id": user.id,
            "product_id": product.id,
            "rating": request.data["rating"],
            "comment": request.data["comment"],
        }
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid() is False:
            logger.error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        product = self.get_product(kwargs["product_id"])
        user = self.get_user(kwargs["user_id"])
        review = Review.objects.filter(user_id=user.id, product_id=product.id)
        if review.count != 1:
            errMsg = (
                f"指定されたレビュー(user_id:{user.id},product_id:{product.id})は存在しません。"
            )
            logger.error(errMsg)
            return Response(errMsg, status=status.HTTP_400_BAD_REQUEST)
        data = {
            "rating": request.data["rating"],
            "comment": request.data["comment"],
        }
        serializer = ReviewSerializer(review, data=data, partial=True)
        if serializer.is_valid() is False:
            logger.error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        product = self.get_product(kwargs["product_id"])
        user = self.get_user(kwargs["user_id"])
        review = Review.objects.filter(user_id=user.id, product_id=product.id)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserReviewListView(generics.ListAPIView):
    serializer_class = ReviewListSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Review.objects.filter(user_id=user_id)


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

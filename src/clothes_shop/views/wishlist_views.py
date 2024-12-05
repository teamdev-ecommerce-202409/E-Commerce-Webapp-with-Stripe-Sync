import logging

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from clothes_shop.models.product import Product
from clothes_shop.models.user_interaction import WishList
from clothes_shop.serializers.user_interaction_serializers import WishListSerializer

logger = logging.getLogger(__name__)


class WishListListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        filters = {}
        filters["user_id"] = user_id
        wishs = WishList.objects.filter(**filters).order_by("-created_at")

        logger.warning("-------------------------------------")
        logger.warning(request.user.is_authenticated)
        logger.warning(request.user.id)
        logger.warning(user_id)
        logger.warning("-------------------------------------")

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_products = paginator.paginate_queryset(wishs, request)

        serializer_data = WishListSerializer(paginated_products, many=True).data

        return paginator.get_paginated_response(serializer_data)

    def post(self, request):
        user_id = request.user.id
        product_id = request.data.get("product_id")
        wish = request.data.get("wish")
        is_public = request.data.get("is_public")

        if not product_id:
            errMsg = "product_idを設定してください。"
            logger.error(errMsg)
            raise NotFound(detail=errMsg)

        try:
            Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            errMsg = f"指定のproduct_id:{product_id}は存在しません。"
            logger.error(errMsg)
            raise NotFound(detail=errMsg)

        if wish:
            WishList.objects.get_or_create(
                user_id=user_id, product_id=product_id, is_public=is_public
            )
            return Response(
                {"message": f"product_id:{product_id}をWishListに追加しました。", "wish": True},
                status=status.HTTP_200_OK,
            )
        else:
            WishList.objects.filter(user_id=user_id, product_id=product_id).delete()
            return Response(
                {"message": f"product_id:{product_id}をWishListから削除しました。", "wish": False},
                status=status.HTTP_200_OK,
            )


class WishListDetailPublicView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get("userId")
        if not user_id:
            raise NotFound(detail="User ID がありません.")

        wishs = WishList.objects.filter(user_id=user_id, is_public=True)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_products = paginator.paginate_queryset(wishs, request)

        serializer_data = WishListSerializer(paginated_products, many=True).data
        return paginator.get_paginated_response(serializer_data)


class WishListDetailPrivateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get("userId")
        if not user_id:
            raise NotFound(detail="User ID がありません.")

        if request.user.id != user_id:
            raise NotFound(detail="作成者しか閲覧できません.")

        wishs = WishList.objects.filter(user_id=user_id)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_products = paginator.paginate_queryset(wishs, request)

        serializer_data = WishListSerializer(paginated_products, many=True).data
        return paginator.get_paginated_response(serializer_data)

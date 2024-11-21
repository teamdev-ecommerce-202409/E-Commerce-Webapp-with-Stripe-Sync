import logging

from django.utils.timezone import now
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from clothes_shop.models.checkout import Checkout
from clothes_shop.permissions import IsAdmin, IsCustomer, IsGuest
from clothes_shop.serializers.cart_item_serializers import (
    CartItemListSerializer,
    CartItemSerializer,
)
from clothes_shop.serializers.checkout_serializers import CheckoutSerializer
from clothes_shop.services.stripe_service import CheckoutData, StripeService
from clothes_shop.views.product_views import get_product
from clothes_shop.views.user_views import get_user

logger = logging.getLogger(__name__)
striep_service = StripeService()


class StripeCheckoutView(APIView):
    permission_classes = [IsAuthenticated & (IsCustomer | IsGuest)]

    def post(self, request):
        """決済のためにStripeチェックアウト画面のURLを返す"""
        serializer = CartItemListSerializer(data=request.data)
        if serializer.is_valid() is False:
            logger.error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data
        checkout_instances = [
            CartItemSerializer(data=checkout_data) for checkout_data in validated_data
        ]
        checkout_data_list: list[CheckoutData] = []
        for checkout_instance in checkout_instances:
            checkout_instance.is_valid()
            product_id = checkout_instance.validated_data["product_id"]
            amount = checkout_instance.validated_data["amount"]
            product = get_product(product_id)
            stripe_product_id = product.stripe_product_id
            checkout_data_list.append(CheckoutData(stripe_product_id, amount))
        role = request.user.role
        stripe_customer_id = request.user.stripe_customer_id
        redirect_url = striep_service.checkout(
            stripe_customer_id=stripe_customer_id if role != "guest" else None,
            checkout_data_list=checkout_data_list,
        )
        data = {"url": redirect_url}
        return Response(data, status=status.HTTP_200_OK)


class StripeCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated & (IsCustomer | IsAdmin)]

    def get(self, request):
        """チェックアウトデータをStripeから取得"""
        checkout_session_id = request.data["checkout_session_id"]
        data = striep_service.get_checkout_session(checkout_session_id)
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):
        """Stripeで決済時に作成されるsession-idをDB登録"""
        user_id = request.data["user_id"]
        checkout_session_id = request.data["checkout_session_id"]
        serializer = CheckoutSerializer(
            data={
                "user": user_id,
                "stripe_checkout_session_id": checkout_session_id,
                "shipping_date": None,
            }
        )
        if not serializer.is_valid():
            logger.error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """配送日時を記録"""
        checkout_session_id = request.data["checkout_session_id"]
        checkout = Checkout.objects.filter(stripe_checkout_session_id=checkout_session_id)
        checkout.shipping_date = now()
        checkout.save()
        return

    def __is_customer_user_id(self, user_id: str) -> bool:
        user = get_user(user_id)
        return user.role == "customer"

    def __is_admin_user_id(self, user_id: str) -> bool:
        user = get_user(user_id)
        return user.role == "admin"


class StripeCheckoutItemsView(APIView):
    permission_classes = [IsAuthenticated & (IsCustomer | IsAdmin)]

    def get(self, request):
        """チェックアウトした製品のデータをStripeから取得"""
        checkout_session_id = request.data["checkout_session_id"]
        data = striep_service.get_checkout_items(checkout_session_id)
        return Response(data=data, status=status.HTTP_200_OK)


class StripeCheckoutListView(APIView):
    permission_classes = [IsAuthenticated & (IsCustomer | IsAdmin)]

    def post(self, request):
        """チェックアウト一覧"""
        stripe_customer_id = request.data["stripe_customer_id"]
        starting_after = request.data["starting_after"]
        data = striep_service.get_checkout_list(stripe_customer_id, starting_after)
        return Response(data=data, status=status.HTTP_200_OK)

import logging

from rest_framework import status
from rest_framework.exceptions import APIException, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from clothes_shop.models.cart import CartItem
from clothes_shop.models.order import Order
from clothes_shop.permissions import IsAdmin, IsCustomer, IsGuest
from clothes_shop.serializers.cart_item_serializers import (
    CartItemListSerializer,
    CartItemSerializer,
)
from clothes_shop.serializers.order_serializers import (
    OrderItemSerializer,
    OrderSerializer,
)
from clothes_shop.services.stripe_service import (
    CheckoutData,
    CheckoutSession,
    StripeService,
)
from clothes_shop.views.product_views import get_product

logger = logging.getLogger(__name__)
striep_service = StripeService()


def get_order(id: int) -> Order:
    try:
        order = Order.objects.get(pk=id)
        return order
    except Order.DoesNotExist:
        errMsg = f"指定されたID {id} に紐づくオーダーが存在しません。"
        logger.error(errMsg)
        raise NotFound(detail=errMsg)
    except Exception as e:
        errMsg = f"想定外のエラーが発生しました: {str(e)}"
        logger.error(errMsg)
        raise APIException(detail=errMsg)


class StripeCheckoutView(APIView):
    permission_classes = [IsAuthenticated & (IsCustomer | IsGuest)]

    def __checkout(
        self, role: str, customer_id: str, cart_item_serializer: CartItemSerializer
    ) -> CheckoutSession:
        checkout_data_list: list[CheckoutData] = []
        for checkout_instance in cart_item_serializer:
            checkout_instance.is_valid()
            product_id = checkout_instance.validated_data["product_id"]
            amount = checkout_instance.validated_data["amount"]
            product = get_product(product_id)
            stripe_product_id = product.stripe_product_id
            checkout_data_list.append(CheckoutData(stripe_product_id, amount))
        checkoutSession = striep_service.checkout(
            stripe_customer_id=customer_id if role != "guest" else None,
            checkout_data_list=checkout_data_list,
        )
        return checkoutSession

    def __clear_cart(self, user_id: int) -> None:
        CartItem.objects.filter(user_id=user_id).delete()
        return None

    def __create_order(
        self, user_id: int, checkout_session_id: str, cart_item_serializer: CartItemSerializer
    ) -> str:
        order_data = {
            "user_pk": user_id,
            "stripe_checkout_session_id": checkout_session_id,
            "order_status": "pending",
            "total_price": 0,
        }
        total_price = 0
        order_item_data_list = []
        for checkout_instance in cart_item_serializer:
            checkout_instance.is_valid()
            product_id = checkout_instance.validated_data["product_id"]
            amount = checkout_instance.validated_data["amount"]
            product = get_product(product_id)
            order_item_data = {"product": product, "quantity": amount, "unit_price": product.price}
            order_item_data_list.append(order_item_data)
            total_price += amount * product.price

        order_data["total_price"] = total_price
        order_serializer = OrderSerializer(data=order_data)
        if not order_serializer.is_valid():
            logger.error(order_serializer.errors)
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        order_serializer.save()
        order = order_serializer.instance

        for i in range(len(order_item_data_list)):
            order_item_data_list[i]["order"] = get_order(order.id)

        items_serializer = OrderItemSerializer(data=cart_item_serializer, many=True)
        if items_serializer.is_valid():
            order = items_serializer.save()
        return order.id

    def post(self, request):
        """決済のためにStripeチェックアウト画面のURLを返す"""
        serializer = CartItemListSerializer(data=request.data)
        if serializer.is_valid() is False:
            logger.error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data

        cart_item_serializer = [
            CartItemSerializer(data=checkout_data) for checkout_data in validated_data
        ]
        role = request.user.role
        stripe_customer_id = request.user.stripe_customer_id
        checkout_session = self.__checkout(
            role=role, customer_id=stripe_customer_id, cart_item_serializer=cart_item_serializer
        )

        order_id = self.__create_order(
            request.user.id, checkout_session.checkout_session_id, cart_item_serializer
        )
        self.__clear_cart(request.user.id)
        data = {"order_id": order_id, "url": checkout_session.url}
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        """決済時に発行されるチェックアウトセッションIDをOrderに紐付ける"""
        order_id = request.data["order_id"]
        stripe_checkout_session_id = request.data["stripe_checkout_session_id"]
        Order.objects.filter(pk=order_id).update(
            stripe_checkout_session_id=stripe_checkout_session_id, order_status="confirmed"
        )
        return Response(status=status.HTTP_200_OK)


class StripeCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated & (IsCustomer | IsAdmin)]

    def get(self, request):
        """チェックアウトデータをStripeから取得"""
        checkout_session_id = request.data["checkout_session_id"]
        data = striep_service.get_checkout_session(checkout_session_id)
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):
        """Stripeで決済時に作成されるsession-idをDB登録"""
        order_id = request.data["order_id"]
        checkout_session_id = request.data["checkout_session_id"]
        order = Order.objects.filter(id=order_id)
        order.stripe_checkout_session_id = checkout_session_id
        order.save()
        return Response(status=status.HTTP_200_OK)


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

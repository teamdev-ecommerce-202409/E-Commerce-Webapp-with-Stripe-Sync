from datetime import datetime, timedelta

from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from clothes_shop.models import Brand, ClothesType, Product, Size, Target
from clothes_shop.serializers import ProductSerializer


class ProductTests(APITestCase):

    def setUp(self):

        # Sizeのバリエーション
        self.size_m = Size.objects.create(name="M")
        self.size_xl = Size.objects.create(name="XL")

        # Targetのバリエーション
        self.target_mens = Target.objects.create(name="メンズ")
        self.target_womens = Target.objects.create(name="レディース")

        # ClothesTypeのバリエーション
        self.cloth_type_shirt = ClothesType.objects.create(name="シャツ")
        self.cloth_type_pants = ClothesType.objects.create(name="パンツ")

        # Brandのバリエーション
        self.brand_nike = Brand.objects.create(name="NIKE")
        self.brand_adidas = Brand.objects.create(name="ADIDAS")

        # デフォルトのリリース日
        one_week_ago = timezone.now() - timedelta(weeks=1)

        # 製品ver.0 ※論理削除
        self.product_0 = Product.objects.create(
            size=self.size_m,
            target=self.target_mens,
            clothes_type=self.cloth_type_shirt,
            brand=self.brand_nike,
            name="論理削除された製品",
            description="てすと",
            category="服",
            price=100,
            release_date=one_week_ago,
            stock_quantity=500,
            is_deleted=True,
        )

        # 以下、is_deleted=False
        # 製品ver.1 ※release_dateが未来
        self.product_1 = Product.objects.create(
            size=self.size_m,
            target=self.target_mens,
            clothes_type=self.cloth_type_shirt,
            brand=self.brand_nike,
            name="未来のリリース日の製品",
            description="てすと",
            category="服",
            price=100,
            release_date=timezone.now() + timedelta(days=1),
            stock_quantity=500,
            is_deleted=False,
        )
        # 以下、※release_dateが過去
        # 製品ver.2 サイズがxl
        self.product_2 = Product.objects.create(
            size=self.size_xl,
            target=self.target_mens,
            clothes_type=self.cloth_type_shirt,
            brand=self.brand_nike,
            name="サイズXL",
            description="てすと",
            category="服",
            price=100,
            release_date=one_week_ago,
            stock_quantity=500,
            is_deleted=False,
        )
        # 製品ver.3 対象がレディース
        self.product_3 = Product.objects.create(
            size=self.size_m,
            target=self.target_womens,
            clothes_type=self.cloth_type_shirt,
            brand=self.brand_nike,
            name="レディース",
            description="てすと",
            category="服",
            price=100,
            release_date=one_week_ago,
            stock_quantity=500,
            is_deleted=False,
        )
        # 製品ver.4 服の種類がパンツ
        self.product_4 = Product.objects.create(
            size=self.size_m,
            target=self.target_mens,
            clothes_type=self.cloth_type_pants,
            brand=self.brand_nike,
            name="服の種類がパンツ",
            description="てすと",
            category="服",
            price=100,
            release_date=one_week_ago,
            stock_quantity=500,
            is_deleted=False,
        )

        # 製品ver.5 ブランドがアディダス
        self.product_5 = Product.objects.create(
            size=self.size_m,
            target=self.target_mens,
            clothes_type=self.cloth_type_shirt,
            brand=self.brand_adidas,
            name="アディダス",
            description="てすと",
            category="服",
            price=100,
            release_date=one_week_ago,
            stock_quantity=500,
            is_deleted=False,
        )

        # 製品ver.6 製品名にキーワード
        self.product_5 = Product.objects.create(
            size=self.size_m,
            target=self.target_mens,
            clothes_type=self.cloth_type_shirt,
            brand=self.brand_adidas,
            name="テスト用につくったキーワード服１",
            description="てすと",
            category="服",
            price=100,
            release_date=one_week_ago,
            stock_quantity=500,
            is_deleted=False,
        )

        # 製品ver.7 商品説明にキーワード
        self.product_5 = Product.objects.create(
            size=self.size_m,
            target=self.target_mens,
            clothes_type=self.cloth_type_shirt,
            brand=self.brand_adidas,
            name="商品説明にkeyword",
            description="てすキーワードと",
            category="服",
            price=100,
            release_date=one_week_ago,
            stock_quantity=500,
            is_deleted=False,
        )

        # 製品ver.8 ブランドがアディダスでレディース
        self.product_5 = Product.objects.create(
            size=self.size_m,
            target=self.target_womens,
            clothes_type=self.cloth_type_shirt,
            brand=self.brand_adidas,
            name="ブランドがアディダスでレディース",
            description="てすと",
            category="服",
            price=100,
            release_date=one_week_ago,
            stock_quantity=500,
            is_deleted=False,
        )
        self.filered_list_url = reverse("clothes_shop:product-list-filtered")

    # 以下、ProductListFilteredViewのテスト
    def test_get_filtered_list_no_filters(self):
        # フィルタなしでリクエスト
        response = self.client.get(self.filered_list_url)
        product = Product.objects.filter(is_deleted=False, release_date__lt=timezone.now())
        serializer = ProductSerializer(product, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_filtered_list_by_size(self):
        # sizeフィルタでリクエスト サイズがxlのものを検索
        response = self.client.get(self.filered_list_url, {"size": self.size_xl.id})
        product = Product.objects.filter(
            size=self.size_xl, is_deleted=False, release_date__lt=timezone.now()
        )
        serializer = ProductSerializer(product, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_filtered_list_by_target(self):
        # メンズフィルタでリクエスト
        response = self.client.get(self.filered_list_url, {"target": self.target_mens.id})
        product = Product.objects.filter(
            target=self.target_mens, is_deleted=False, release_date__lt=timezone.now()
        )
        serializer = ProductSerializer(product, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_filtered_list_by_clothes_type(self):
        # ずぼんフィルタでリクエスト
        response = self.client.get(
            self.filered_list_url, {"clothes_type": self.cloth_type_pants.id}
        )
        product = Product.objects.filter(
            clothes_type=self.cloth_type_pants, is_deleted=False, release_date__lt=timezone.now()
        )
        serializer = ProductSerializer(product, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_filtered_list_by_brand(self):
        # ブランドNIKEでリクエスト
        response = self.client.get(self.filered_list_url, {"brand": self.brand_nike.id})
        product = Product.objects.filter(
            brand=self.brand_nike, is_deleted=False, release_date__lt=timezone.now()
        )
        serializer = ProductSerializer(product, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_filtered_list_by_combined_filters(self):
        # サイズM、ターゲットがメンズ、服の種類がシャツでフィルタ
        response = self.client.get(
            self.filered_list_url,
            {
                "size": self.size_m.id,
                "target": self.target_mens.id,
                "clothes_type": self.cloth_type_shirt.id,
            },
        )
        product = Product.objects.filter(
            size=self.size_m,
            target=self.target_mens,
            clothes_type=self.cloth_type_shirt,
            is_deleted=False,
            release_date__lt=timezone.now(),
        )
        serializer = ProductSerializer(product, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_filtered_list_by_keyword_in_name_or_description(self):
        # キーワードがnameまたはdescriptionに含まれる製品のリストを取得
        response = self.client.get(
            self.filered_list_url,
            {"keyword": "キーワード"},
        )
        product = Product.objects.filter(
            (Q(name__icontains="キーワード") | Q(description__icontains="キーワード")),
            is_deleted=False,
            release_date__lt=timezone.now(),
        )
        serializer = ProductSerializer(product, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_filtered_list_by_multiple_filters(self):
        # 複数フィルタでリクエスト　ブランドがアディダスでレディース
        response = self.client.get(
            self.filered_list_url,
            {
                "target": self.target_womens.id,
                "brand": self.brand_adidas.id,
            },
        )
        product = Product.objects.filter(
            target=self.target_womens,
            brand=self.brand_adidas,
            is_deleted=False,
            release_date__lt=timezone.now(),
        )
        serializer = ProductSerializer(product, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

User = get_user_model()
token_generator = PasswordResetTokenGenerator()  # Token generator

class AuthAPITestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # クラス全体で使われるテスト用のユーザーを作成し、そのユーザーに対するJWTトークンも生成
        cls.user = User.objects.create_user(
            username="testuser", 
            email="test@example.com", 
            password="password123", 
            is_active=True
        )
        # cls.token = RefreshToken.for_user(cls.user).access_token
        # アクセストークンとリフレッシュトークンを取得
        refresh = RefreshToken.for_user(cls.user)
        cls.access_token = refresh.access_token
        cls.refresh_token = refresh  # ここでリフレッシュトークンを保持

    def test_register_user(self):
        """ユーザー登録APIのテスト"""
        url = reverse('register')
        data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
            "username": "newuser"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.json())
        self.assertEqual(response.json().get("message"), "ユーザー登録が完了し、確認メールが送信されました。")

    def test_logout(self):
        """ログアウトAPIのテスト"""
        url = reverse('logout')
        # headers = {'Authorization': f'Bearer {self.token}'}
        # HTTP_AUTHORIZATION ヘッダーにリフレッシュトークンを渡す
        # response = self.client.post(url, HTTP_AUTHORIZATION=f'Bearer {self.refresh_token}')

        # リクエストボディでリフレッシュトークンを渡す
        data = {
            'refresh_token': str(self.refresh_token)  # ← 修正箇所
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("message"), "ログアウトしました。")

    def test_send_confirmation_email(self):
        """メール確認送信APIのテスト"""
        url = reverse('send_confirmation_email')
        data = {"email": self.user.email}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data["message"], "メールが送信されました")
        self.assertEqual(response.json().get("message"), "メールが送信されました")

    def test_confirm_email(self):
        """メール確認APIのテスト"""
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        # token = self.user.tokens_generator.make_token(self.user)
        token = token_generator.make_token(self.user)
        url = reverse('account_confirm_email', args=[uid, token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset(self):
        """パスワードリセットAPIのテスト"""
        url = reverse('password_reset')
        data = {"email": self.user.email}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data["message"], "パスワードリセットメールが送信されました。")
        self.assertEqual(response.json().get("message"), "パスワードリセットメールが送信されました。")

    def test_password_reset_confirm(self):
        """パスワードリセット確認APIのテスト"""
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        # token = self.user.tokens_generator.make_token(self.user)
        token = token_generator.make_token(self.user)
        url = reverse('password_reset_confirm', args=[uid, token])
        data = {"new_password": "newpassword123"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data["message"], "パスワードがリセットされました。")
        self.assertEqual(response.json().get("message"), "パスワードがリセットされました。")
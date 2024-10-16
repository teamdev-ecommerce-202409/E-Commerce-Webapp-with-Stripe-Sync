from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from unittest.mock import patch  # モック用
from libs.email_utils import send_email

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
        # アクセストークンとリフレッシュトークンを取得
        refresh = RefreshToken.for_user(cls.user)
        cls.access_token = refresh.access_token
        cls.refresh_token = refresh  # ここでリフレッシュトークンを保持

    @patch('djangopj.views.send_email')
    def test_register_user(self, mock_send_email):
        """ユーザー登録APIのテスト"""
        url = reverse('register')
        data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
            "username": "newuser"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 新しく作成されたユーザーを取得
        new_user = User.objects.get(email="newuser@example.com")
    
        # mock_send_email が新しいユーザーと "confirmation" を引数に呼び出されているか確認
        mock_send_email.assert_called_once_with(new_user, "confirmation")

    def test_logout(self):
        """ログアウトAPIのテスト"""
        url = reverse('logout')
        
        # リクエストボディでリフレッシュトークンを渡す
        data = {
            'refresh_token': str(self.refresh_token) 
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("message"), "ログアウトしました。")

    @patch('djangopj.views.send_email')
    def test_send_confirmation_email(self, mock_send_email):
        """メール確認送信APIのテスト"""
        mock_send_email.return_value = None
        url = reverse('send_confirmation_email')
        data = {"email": self.user.email}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("message"), "メールが送信されました")
        mock_send_email.assert_called_once_with(self.user, "confirmation")
    
    @patch('djangopj.views.send_email')
    def test_send_confirmation_email_failure(self, mock_send_email):
        """メール送信失敗時のテスト"""
        mock_send_email.side_effect = Exception("メール送信エラー")
        url = reverse('send_confirmation_email')
        data = {"email": self.user.email}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_confirm_email(self):
        """メール確認APIのテスト"""
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = token_generator.make_token(self.user)
        url = reverse('account_confirm_email', args=[uid, token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('djangopj.views.send_email')
    def test_password_reset(self, mock_send_email):
        """パスワードリセットAPIのテスト"""
        mock_send_email.return_value = None
        url = reverse('password_reset')
        data = {"email": self.user.email}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("message"), "パスワードリセットメールが送信されました。")
        mock_send_email.assert_called_once_with(self.user, "reset")

    def test_password_reset_confirm(self):
        """パスワードリセット確認APIのテスト"""
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = token_generator.make_token(self.user)
        url = reverse('password_reset_confirm', args=[uid, token])
        data = {"new_password": "newpassword123"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("message"), "パスワードがリセットされました。")
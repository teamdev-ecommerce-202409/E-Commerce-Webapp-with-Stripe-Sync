from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from libs.email_utils import send_email
import json

User = get_user_model()
token_generator = PasswordResetTokenGenerator()

class RegisterUserView(APIView): # ユーザー登録API
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        username = data.get("username")
        
        # ユーザーを作成
        user = User.objects.create_user(email=email, password=password, username=username, role='guest')
        user.is_active = False  # メール確認が完了するまで無効
        user.save()

        # メール送信
        # send_confirmation_email(user)
        send_email(user, "confirmation")
        return JsonResponse({"message": "ユーザー登録が完了し、確認メールが送信されました。"}, status=201)

class LogoutView(APIView): # ログアウトAPI
    def post(self, request, *args, **kwargs):
        # ヘッダーからではなく、リクエストボディからリフレッシュトークンを取得
        token = request.data.get('refresh_token') 

        if token:
            refresh_token = RefreshToken(token)
            refresh_token.blacklist()
            return JsonResponse({"message": "ログアウトしました。"}, status=200)
        else:
            return JsonResponse({"message": "リフレッシュトークンが見つかりません。"}, status=400)

class SendConfirmationEmailView(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)  # リクエストボディからJSONデータを取得
        user = User.objects.get(email=data.get("email"))  # メールアドレスでユーザー取得
        try:
            send_email(user, "confirmation")
        except Exception as e:
            return JsonResponse({"message": "メール送信に失敗しました。"}, status=500)
        return JsonResponse({"message": "メールが送信されました"}, status=200)

class CustomConfirmEmailView(APIView):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return HttpResponse('無効なトークンです。', status=400)

        if token_generator.check_token(user, token):
            user.is_verified = True
            user.is_active = True  # メール確認後にユーザーを有効化
            user.role = "registered"  # roleフィールドを"registered"に設定
            user.save()
            return HttpResponse('メール確認が完了しました。', status=200)
        else:
            return HttpResponse('無効なトークンです。', status=400)

# パスワードリセットAPI
class PasswordResetView(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        email = data.get("email")
        user = User.objects.get(email=email)
        # パスワードリセットトークンを生成し、メールを送信
        try:
            send_email(user, "reset")
        except Exception as e:
            return JsonResponse({"message": "パスワードリセットメールの送信に失敗しました。"}, status=500)
        return JsonResponse({"message": "パスワードリセットメールが送信されました。"}, status=200)

class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return JsonResponse({"message": "無効なリンクです。"}, status=400)

        if token_generator.check_token(user, token):
            data = json.loads(request.body)
            new_password = data.get("new_password")
            user.set_password(new_password)
            user.save()
            return JsonResponse({"message": "パスワードがリセットされました。"}, status=200)
        else:
            return JsonResponse({"message": "無効なトークンです。"}, status=400)

class UserListView(APIView):
    def get(self, request):
        users = User.objects.all().values('id', 'email', 'username', 'is_active','password','auth_token', 'date_joined','user_permissions')
        return Response(list(users), status=200)
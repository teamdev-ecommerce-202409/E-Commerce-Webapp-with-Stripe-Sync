import os
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator

token_generator = PasswordResetTokenGenerator()

def send_email(user, email_type="confirmation"):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)

    if email_type == "confirmation":
        base_url = os.getenv("CONFIRMATION_URL", "http://127.0.0.1:8081")
        url = f'{base_url}/api/auth/registration/account-confirm-email/{uid}/{token}/'
        subject = 'Confirm your email'
        message = f'Please click the following link to verify your email: {url}'
    elif email_type == "reset":
        base_url = os.getenv("RESET_URL", "http://127.0.0.1:8081")
        url = f'{base_url}/api/auth/password/reset/confirm/{uid}/{token}/'
        subject = 'Password Reset Request'
        message = f'Click the link to reset your password: {url}'

    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    except Exception as e:
        print(f"Failed to send {email_type} email: {e}")
        raise
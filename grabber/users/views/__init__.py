from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.response import Response

from grabber.settings import ACCESS_TOKEN_AGE, REFRESH_TOKEN_AGE, FRONTEND_URL
from grabber.settings import JWT_SECURE, JWT_HTTP_ONLY, JWT_SAME_SITE

FRONTEND_URL = FRONTEND_URL

token_generator = PasswordResetTokenGenerator()
User = get_user_model()

def set_default_jwt_cookies(response: Response, access_token: str, refresh_token: str) -> Response:
    response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=JWT_HTTP_ONLY,
                samesite=JWT_SAME_SITE,
                secure=JWT_SECURE,  # включить True при использовании HTTPS
                max_age=ACCESS_TOKEN_AGE,
    )

     # 🔁 refresh_token: используется для обновления access_token
    response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=JWT_HTTP_ONLY,
                samesite=JWT_SAME_SITE,
                secure=JWT_SECURE,
                max_age=REFRESH_TOKEN_AGE,
    )

    return response

def set_null_jwt_cookies(response: Response) -> Response:
    response.set_cookie(
        key='access_token',
        value='',
        max_age=0,
        httponly=JWT_HTTP_ONLY,
        samesite=JWT_SAME_SITE,
        secure=JWT_SECURE,  # или True, если HTTPS
        path='/'
    )

    response.set_cookie(
        key='refresh_token',
        value='',
        max_age=0,
        httponly=JWT_HTTP_ONLY,
        samesite=JWT_SAME_SITE,
        secure=JWT_SECURE,
        path='/'
    )
    return response
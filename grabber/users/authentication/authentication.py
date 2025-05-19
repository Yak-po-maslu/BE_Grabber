from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, AuthenticationFailed
from django.urls import reverse


class JWTAuthFromCookie(JWTAuthentication):
    def authenticate(self, request):

        login_url = reverse("users:login")
        register_url = reverse("users:register")
        refresh_url = reverse("users:refresh")
        # Пропускаем аутентификацию для пути логина и регистрации
        if request.path in [login_url, register_url, refresh_url]:
            return None

        access_token = request.COOKIES.get("access_token")
        if access_token is None:
            raise AuthenticationFailed("Access token expired or not provided")

        try:
            validated_token = self.get_validated_token(access_token)
        except TokenError:
            return AuthenticationFailed(detail="Access token expired")

        return self.get_user(validated_token), validated_token

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from django.urls import reverse


class JWTAuthFromCookie(JWTAuthentication):
    def authenticate(self, request):

        login_url = reverse("users:login")
        register_url = reverse("users:register")
        # Пропускаем аутентификацию для пути логина и регистрации
        if request.path in [login_url, register_url]:
            return None

        access_token = request.COOKIES.get("access_token")
        if access_token is None:
            return None

        try:
            validated_token = self.get_validated_token(access_token)
        except TokenError:
            return None  # Возвращаем None, если токен невалиден

        return self.get_user(validated_token), validated_token

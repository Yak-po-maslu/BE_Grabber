from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError


class JWTAuthFromCookie(JWTAuthentication):
    def authenticate(self, request):
        # Пропускаем аутентификацию для пути логина и регистрации
        if request.path in ['/api/login/', '/api/register/']:
            return None

        access_token = request.COOKIES.get("access_token")
        if access_token is None:
            return None

        try:
            validated_token = self.get_validated_token(access_token)
        except TokenError:
            return None  # Возвращаем None, если токен невалиден

        return self.get_user(validated_token), validated_token

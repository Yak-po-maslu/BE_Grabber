import re

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, AuthenticationFailed
from django.urls import reverse


class JWTAuthFromCookie(JWTAuthentication):
    def authenticate(self, request):

        login_url = reverse("users:login")
        register_url = reverse("users:register")
        refresh_url = reverse("users:refresh")
        swagger_url = reverse("schema-swagger-ui")
        main_page_ads_url = reverse("main-page-ads")
        categories_url = reverse("categories-list")
        filters_ads_url = reverse("ad-list")
        get_one_ad = 'api/ads/(?P<ad_id>[0-9]+)/\\Z'


        allowed_urls = [
                        login_url,
                        register_url,
                        refresh_url,
                        swagger_url,
                        main_page_ads_url,
                        categories_url,
                        filters_ads_url,
                        get_one_ad,
                        ]

        def is_allowed_path(path):
            return any(re.match(pattern, path) for pattern in allowed_urls)


        # Пропускаем аутентификацию для пути логина и регистрации
        if is_allowed_path(request.path):
            return None

        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")

        if access_token is None and refresh_token is None:
            return None


        if access_token is None and refresh_token:
            raise AuthenticationFailed("Access token expired or not provided")

        try:
            validated_token = self.get_validated_token(access_token)
        except TokenError:
            return AuthenticationFailed(detail="Access token expired")

        return self.get_user(validated_token), validated_token

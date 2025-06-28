import re

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, AuthenticationFailed
from django.urls import reverse


class JWTAuthFromCookie(JWTAuthentication):
    def authenticate(self, request):

        # exact paths
        allowed_paths = [
            reverse("users:login"),
            reverse("users:register"),
            reverse("users:refresh"),
            reverse("schema-swagger-ui"),
            reverse("main-page-ads"),
            reverse("categories-list"),
            reverse("ad-list"),
            reverse('newsletter-subscribe')
        ]

        # regex patterns
        allowed_regex_patterns = [
            r'^/api/ads/(?P<ad_id>[0-9]+)/$',
        ]

        def is_allowed_path(path):
            if path in allowed_paths:
                return True
            return any(re.match(pattern, path) for pattern in allowed_regex_patterns)

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

from tokenize import TokenError

from adrf.views import APIView as AsyncAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from . import JWT_SECURE, JWT_HTTP_ONLY, JWT_SAME_SITE, ACCESS_TOKEN_AGE


class AsyncCookieViewRefresh(AsyncAPIView):
    async def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({'error': 'Refresh token not provided'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
        except TokenError as e:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)

        response = Response({'message': 'Access token refreshed'}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=JWT_HTTP_ONLY,
            samesite=JWT_SAME_SITE,
            secure=JWT_SECURE,
            max_age=ACCESS_TOKEN_AGE,
        )
        return response
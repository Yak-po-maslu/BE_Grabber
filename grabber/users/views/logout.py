from adrf.views import APIView as AsyncAPIView
from rest_framework import status
from rest_framework.response import Response

from . import set_null_jwt_cookies


class AsyncCookieViewLogout(AsyncAPIView):
    async def post(self, request):
        response = Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        # Устанавливаем "пустые" куки с коротким временем жизни (1 секунда)
        response = set_null_jwt_cookies(response)

        return response
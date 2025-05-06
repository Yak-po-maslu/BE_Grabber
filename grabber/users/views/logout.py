from adrf.views import APIView as AsyncAPIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from . import set_null_jwt_cookies


@swagger_auto_schema(
    method='post',
    responses={200: "Logged out successfully."},

)
@action(detail=True, methods=['post'], url_path='logout')
class AsyncCookieViewLogout(AsyncAPIView):
    async def post(self, request):
        response = Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        # Устанавливаем "пустые" куки с коротким временем жизни (1 секунда)
        response = set_null_jwt_cookies(response)

        return response
from adrf.views import APIView as AsyncAPIView
from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers.serializers import UserLoginSerializer
from users.utils.getUserData import get_user_data
from . import CustomUser, set_default_jwt_cookies
from drf_yasg.utils import swagger_auto_schema


class AsyncCookieViewLogin(AsyncAPIView):
    permission_classes = [AllowAny]
    """
    Асинхронный логин с установкой токенов в куки.
    """

    @swagger_auto_schema(
        method='post',
        request_body=UserLoginSerializer,
        responses={200: "Login Success. Data of login user"},

    )
    @action(detail=True, methods=['post'], url_path='login')
    async def post(self, request):
        # 1. Получаем данные из запроса
        serializer = UserLoginSerializer(data=request.data)
        is_valid = await sync_to_async(serializer.is_valid)()

        if not is_valid:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        email = validated_data['email']
        password = validated_data['password']


        # 2. Аутентификация пользователя через sync_to_async
        user = await sync_to_async(authenticate)(request, username=email, password=password)


        # 3. Если пользователь не найден — ошибка
        if user is None:
            return Response(
                {'error': 'Incorrect username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # 4. Генерация JWT-токенов
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        await sync_to_async(update_last_login)(CustomUser, user)

        # 5. Создание ответа и установка токенов в куки
        response = Response({'message': 'Login successful!'}, status=status.HTTP_200_OK)


        response = set_default_jwt_cookies(response, access_token, refresh_token)
        response.data = await sync_to_async(get_user_data)(user)
        return response

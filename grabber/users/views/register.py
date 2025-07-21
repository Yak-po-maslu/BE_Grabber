from adrf.views import APIView as AsyncAPIView
from asgiref.sync import sync_to_async
from django.contrib.auth.models import update_last_login
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from . import CustomUser, set_default_jwt_cookies
from ..serializers.serializers import UserRegisterSerializer
from ..utils.getUserData import get_user_data



class AsyncCookieViewRegister(AsyncAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        method='post',
        request_body=UserRegisterSerializer,
        responses={201: "Sign up success!"},

    )
    @action(detail=True, methods=['post'], url_path='register')
    async def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        is_valid = await sync_to_async(serializer.is_valid)()

        if not is_valid:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #Save user
        user = await sync_to_async(serializer.save)()

        # 🔐 Генерируем JWT-токены
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        await sync_to_async(update_last_login)(CustomUser, user)

        # 📤 Отправляем ответ с куками
        response = Response({'message': 'Sign up success!'}, status=status.HTTP_201_CREATED)

        response = set_default_jwt_cookies(response, access_token, refresh_token)

        response.data = await sync_to_async(get_user_data)(user)

        return response
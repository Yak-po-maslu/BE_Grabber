from datetime import datetime, timedelta
from time import timezone
from .utils.getUserData import get_user_data
from django.contrib.auth.models import update_last_login
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from asgiref.sync import sync_to_async
from adrf.views import APIView as AsyncAPIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.permissions import IsAuthenticated, AllowAny
from grabber.settings import JWT_SECURE, JWT_HTTP_ONLY, JWT_SAME_SITE
from .models import CustomUser
from .serializers.serializers import UserProfileSerializer, UserRegisterSerializer, UserLoginSerializer
from grabber.settings import ACCESS_TOKEN_AGE, REFRESH_TOKEN_AGE
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .serializers.reset_password import UserResetSerializer
from grabber.settings import FRONTEND_URL
from typing import cast




token_generator = PasswordResetTokenGenerator()

User = get_user_model()

class AsyncResetPasswordView(AsyncAPIView):
    permission_classes = [AllowAny]

    async def post(self, request):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        if not all([uidb64, token, new_password]):
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = await sync_to_async(User.objects.get)(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)

        if not token_generator.check_token(user, token):
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        # Обновление пароля
        user.set_password(new_password)
        await sync_to_async(user.save)()

        return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)


class AsyncForgotPasswordView(AsyncAPIView):
    permission_classes = [AllowAny]

    async def post(self, request):
        serializer = UserResetSerializer(data=request.data)
        is_valid = await sync_to_async(serializer.is_valid)()

        if not is_valid:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        email = validated_data['email']

        try:
            user = cast(CustomUser, await sync_to_async(User.objects.get)(email=email))
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Генерация токена
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        reset_url = f"{FRONTEND_URL}/reset-password/{uid}/{token}"

        # Отправка письма (асинхронно или sync_to_async)
        subject = "Password Reset Request"
        message = f"Use the link below to reset your password:\n{reset_url}"
        await sync_to_async(user.email_user)(
            subject=subject,
            message=message,
            from_email=None,
        )

        return Response({'message': 'Password reset link has been sent to your email.'}, status=status.HTTP_200_OK)


class UserProfileView(AsyncAPIView):

    permission_classes = [IsAuthenticated]
    async def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    async def patch(self, request):
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True  # частичное обновление
        )

        is_valid = await sync_to_async(serializer.is_valid)()

        if is_valid:
            await sync_to_async(serializer.save)()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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

class AsyncCookieViewLogout(AsyncAPIView):
    async def post(self, request):
        response = Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        # Устанавливаем "пустые" куки с коротким временем жизни (1 секунда)
        response.set_cookie(
            key='access_token',
            value='',
            max_age=0,
            httponly=JWT_HTTP_ONLY,
            samesite=JWT_SAME_SITE,
            secure=JWT_SECURE,  # или True, если HTTPS
            path='/'
        )

        response.set_cookie(
            key='refresh_token',
            value='',
            max_age=0,
            httponly=JWT_HTTP_ONLY,
            samesite=JWT_SAME_SITE,
            secure=JWT_SECURE,
            path='/'
        )

        return response

class AsyncCookieViewLogin(AsyncAPIView):
    permission_classes = [AllowAny]
    """
    Асинхронный логин с установкой токенов в куки.
    """

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
        user = await sync_to_async(authenticate)(email=email, password=password)

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

        await sync_to_async(update_last_login)(User, user)

        # 5. Создание ответа и установка токенов в куки
        response = Response({'message': 'Login successful!'}, status=status.HTTP_200_OK)

        # 🔒 access_token: живёт недолго, используется в каждом запросе
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=JWT_HTTP_ONLY,
            samesite=JWT_SAME_SITE,
            secure=JWT_SECURE,  # включить True при использовании HTTPS
            max_age=ACCESS_TOKEN_AGE,
        )

        # 🔁 refresh_token: используется для обновления access_token
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=JWT_HTTP_ONLY,
            samesite=JWT_SAME_SITE,
            secure=JWT_SECURE,
            max_age=REFRESH_TOKEN_AGE,
        )

        response.data = get_user_data(user)
        return response


class AsyncCookieViewRegister(AsyncAPIView):
    permission_classes = [AllowAny]
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

        await sync_to_async(update_last_login)(User, user)

        # 📤 Отправляем ответ с куками
        response = Response({'message': 'Sign up success!'}, status=status.HTTP_201_CREATED)

        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=JWT_HTTP_ONLY,
            samesite=JWT_SAME_SITE,
            secure=JWT_SECURE,
            max_age=ACCESS_TOKEN_AGE,
        )
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=JWT_HTTP_ONLY,
            samesite=JWT_SAME_SITE,
            secure=JWT_SECURE,
            max_age=REFRESH_TOKEN_AGE,
        )

        response.data = get_user_data(user)

        return response



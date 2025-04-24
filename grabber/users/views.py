from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
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
from .serializers import UserProfileSerializer


User = get_user_model()

class UserProfileView(AsyncAPIView):
    permission_classes = [IsAuthenticated]

    async def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    async def put(self, request):
        # Асинхронна валідація і збереження
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
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
            secure=JWT_SECURE
        )
        return response
class MeView(AsyncAPIView):
    permission_classes = [IsAuthenticated]

    async def get(self, request):
        user = request.user
        return Response({
            "email": user.email,
            "id": user.id,
            "joined": user.date_joined,
        })
class AsyncCookieViewLogout(AsyncAPIView):
    async def post(self, request):
        response = Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response


class AsyncCookieViewLogin(AsyncAPIView):
    permission_classes = [AllowAny]
    """
    Асинхронный логин с установкой токенов в куки.
    """

    async def post(self, request):
        # 1. Получаем данные из запроса
        data = request.data
        #username = data.get('email')
        email = data.get('email')
        password = data.get('password')

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
            secure=JWT_SECURE  # включить True при использовании HTTPS
        )

        # 🔁 refresh_token: используется для обновления access_token
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=JWT_HTTP_ONLY,
            samesite=JWT_SAME_SITE,
            secure=JWT_SECURE
        )

        return response


class AsyncCookieViewRegister(AsyncAPIView):
    permission_classes = [AllowAny]
    async def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')


        # 🚫 Проверка, существует ли такой пользователь
        user_exists = await sync_to_async(User.objects.filter(email=email).exists)()
        if user_exists:
            return Response({'error': 'User with this email already existed!'}, status=status.HTTP_400_BAD_REQUEST)

        # 🧠 Проверка валидности пароля (например, минимальная длина)
        try:
            await sync_to_async(validate_password)(password)
        except ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Создаём пользователя
        user = await sync_to_async(User.objects.create_user)(
            email=email,
            password=password,
        )

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
            secure=JWT_SECURE
        )
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=JWT_HTTP_ONLY,
            samesite=JWT_SAME_SITE,
            secure=JWT_SECURE
        )

        return response



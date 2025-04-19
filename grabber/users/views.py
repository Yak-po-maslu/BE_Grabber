from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch') #for debug
class AsyncCookieView(APIView):
    """
    Асинхронный логин с установкой токенов в куки.
    """

    async def login(self, request):
        # 1. Получаем данные из запроса
        data = request.data
        email = data.get('email')
        password = data.get('password')

        # 2. Аутентификация пользователя через sync_to_async
        user = await sync_to_async(authenticate)(email=email, password=password)

        # 3. Если пользователь не найден — ошибка
        if user is None:
            return Response(
                {'error': 'Неверное имя пользователя или пароль'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # 4. Генерация JWT-токенов
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # 5. Создание ответа и установка токенов в куки
        response = Response({'message': 'Успешный вход'}, status=status.HTTP_200_OK)

        # 🔒 access_token: живёт недолго, используется в каждом запросе
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            samesite='Lax',
            secure=False  # включить True при использовании HTTPS
        )

        # 🔁 refresh_token: используется для обновления access_token
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            samesite='Lax',
            secure=False
        )

        return response

    async def register(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        # 🚫 Проверка, существует ли такой пользователь
        user_exists = await sync_to_async(User.objects.filter(email=email).exists)()
        if user_exists:
            return Response({'error': 'Пользователь с таким именем уже существует'}, status=status.HTTP_400_BAD_REQUEST)

        # 🧠 Проверка валидности пароля (например, минимальная длина)
        try:
            await sync_to_async(validate_password)(password)
        except ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Создаём пользователя
        user = await sync_to_async(User.objects.create_user)(

            email=email,
            password=password
        )

        # 🔐 Генерируем JWT-токены
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # 📤 Отправляем ответ с куками
        response = Response({'message': 'Регистрация успешна'}, status=status.HTTP_201_CREATED)

        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            samesite='Lax',
            secure=False
        )
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            samesite='Lax',
            secure=False
        )

        return response



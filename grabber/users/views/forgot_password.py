from typing import cast

from adrf.views import APIView as AsyncAPIView
from asgiref.sync import sync_to_async
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import User, FRONTEND_URL, token_generator
from ..models import CustomUser
from ..serializers.reset_password import UserResetSerializer


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

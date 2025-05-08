from typing import cast

from adrf.views import APIView as AsyncAPIView
from asgiref.sync import sync_to_async
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import CustomUser, F_URL, token_generator
from ..models import CustomUser
from ..serializers.forgot_password import UserForgetPassword


class AsyncForgotPasswordView(AsyncAPIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        method='post',
        request_body=UserForgetPassword,
        responses={200: "Password reset link has been sent to your email."},

    )
    @action(detail=True, methods=['post'], url_path='forgot_password')
    async def post(self, request):
        serializer = UserForgetPassword(data=request.data)
        is_valid = await sync_to_async(serializer.is_valid)()

        if not is_valid:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        email = validated_data['email']

        try:
            user = cast(CustomUser, await sync_to_async(CustomUser.objects.get)(email=email))
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Генерация токена
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        reset_url = f"{F_URL}/reset-password/{uid}/{token}"

        # Отправка письма (асинхронно или sync_to_async)
        subject = "Password Reset Request"
        message = f"Use the link below to reset your password:\n{reset_url}"
        await sync_to_async(user.email_user)(
            subject=subject,
            message=message,
            from_email=None,
        )

        return Response({'message': 'Password reset link has been sent to your email.'}, status=status.HTTP_200_OK)

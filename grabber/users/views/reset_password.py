from adrf.views import APIView as AsyncAPIView
from asgiref.sync import sync_to_async
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import User, token_generator


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


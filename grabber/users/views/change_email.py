from adrf.views import APIView as AsyncAPIView
from asgiref.sync import sync_to_async
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from ..serializers.change_email import ChangeEmailValidator

class ChangeEmailView(AsyncAPIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Заміна email",
        operation_description="Заміна email за умови введення поточного email, нового email та пароля користувача.",
        request_body=ChangeEmailValidator,
        responses={
            200: openapi.Response(description="Email успішно змінено"),
            400: openapi.Response(description="Помилка валідації"),
            401: openapi.Response(description="Несанкціонований доступ"),
        }
    )
    async def post(self, request):
        serializer = ChangeEmailValidator(data=request.data, context={'request': request})

        # is_valid - синхронний, тому викликаємо асинхронно
        is_valid = await sync_to_async(serializer.is_valid)(raise_exception=False)
        if not is_valid:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # save - синхронний, викликаємо через sync_to_async
        await sync_to_async(serializer.save)()

        return Response({'detail': 'Email updated successfully.'}, status=status.HTTP_200_OK)

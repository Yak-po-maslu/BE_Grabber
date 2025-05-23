from adrf.views import APIView
from asgiref.sync import sync_to_async
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..serializers.change_password import ChangePasswordValidator

class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Зміна пароля",
        operation_description="Дозволяє автентифікованому користувачу змінити пароль, вказавши поточний та новий пароль.",
        request_body=ChangePasswordValidator,
        responses={
            200: openapi.Response(description="Пароль успішно змінено"),
            400: openapi.Response(description="Помилка валідації"),
            401: openapi.Response(description="Несанкціонований доступ"),
        }
    )
    async def post(self, request):
        serializer = ChangePasswordValidator(data=request.data, context={'request': request})
        await sync_to_async(serializer.is_valid)(raise_exception=True)
        await sync_to_async(serializer.save)()

        return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)




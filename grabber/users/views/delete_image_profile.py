from adrf.views import APIView
from asgiref.sync import sync_to_async
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from . import CustomUser


User = CustomUser
class DeleteImageProfile(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Видалення фото профілю",
        operation_description="Видаляє фото профілю автентифікованого користувача.",
        responses={
            204: openapi.Response(description="Фото успішно видалено"),
            401: openapi.Response(description="Неавторизований доступ"),
        }
    )
    async def delete(self, request):
        user = request.user
        user.user_photo = ''
        await sync_to_async(user.save)()

        return Response({"details":"User photo is deleted successfully."},status=status.HTTP_204_NO_CONTENT)
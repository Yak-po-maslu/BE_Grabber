from adrf.views import APIView
from asgiref.sync import sync_to_async
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from ads.models import SubCategory
from users.permissions.permissions import IsAdminOrModerator


class DeleteSubCategoryAPIView(APIView):
    permission_classes = [IsAdminOrModerator]

    @swagger_auto_schema(
        operation_summary="Видалення підкатегорії",
        operation_description="Видаляє підкатегорію за її `id`.",
        responses={204: "Deleted", 404: "Підкатегорію не знайдено"}
    )
    async def delete(self, request, subcategory_id):
        subcategory = await sync_to_async(SubCategory.objects.filter(id=subcategory_id).first)()
        if not subcategory:
            return Response({"error": "Підкатегорію не знайдено"}, status=status.HTTP_404_NOT_FOUND)

        await sync_to_async(subcategory.delete)()
        return Response(status=status.HTTP_204_NO_CONTENT)

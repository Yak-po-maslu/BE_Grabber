from asgiref.sync import sync_to_async
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from users.permissions.permissions import IsAdminOrModerator
from ..models import Category

from ..serializers.category import CategorySerializer
from adrf.views import APIView

class EditCategoryAPIView(APIView):
    permission_classes = (IsAdminOrModerator,)

    @swagger_auto_schema(
        operation_summary="Редагування категорії",
        operation_description="Оновлює існуючу категорію за її `id`. Часткове оновлення поля `name`.",
        request_body=CategorySerializer,
        responses={
            200: CategorySerializer,
            404: "Категорію не знайдено"
        }
    )
    async def patch(self, request, category_id):
        category: Category = await sync_to_async(Category.objects.filter(id=category_id).first)()

        if not category:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data, partial=True)
        await sync_to_async(serializer.is_valid)(raise_exception=True)
        await sync_to_async(serializer.save)()

        return Response(serializer.data, status=status.HTTP_200_OK)



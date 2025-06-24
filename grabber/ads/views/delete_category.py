from typing import cast

from adrf.views import APIView
from asgiref.sync import sync_to_async
from rest_framework import status
from rest_framework.response import Response

from users.permissions.permissions import IsAdminOrModerator
from users.models import CustomUser
from ..models import Category
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class DeleteCategoryView(APIView):
    permission_classes = (IsAdminOrModerator,)

    @swagger_auto_schema(
        operation_description="Видаляє категорію. Доступ мають лише адміністратори та модератори.",
        manual_parameters=[
            openapi.Parameter(
                'category_id', openapi.IN_PATH,
                description="ID категорії",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            204: 'Категорію успішно видалено',
            400: 'Помилка при видаленні',
            403: 'Недостатньо прав для видалення',
            404: 'Категорію не знайдено',
        }
    )
    async def delete(self, request, category_id):
        user = cast(CustomUser, request.user)
        user_status = user.role

        if user_status in ['admin', 'moderator']:
            try:
                category = await sync_to_async(Category.objects.get)(id=category_id)
                await sync_to_async(category.delete)()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Category.DoesNotExist:
                return Response({"detail": "Категорію не знайдено"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Недостатньо прав"}, status=status.HTTP_403_FORBIDDEN)

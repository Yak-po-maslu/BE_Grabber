from adrf.views import APIView
from asgiref.sync import sync_to_async
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from ads.models import SubCategory
from ads.serializers.subcategory import SubCategorySerializer
from users.permissions.permissions import IsAdminOrModerator


class EditSubCategoryAPIView(APIView):
    permission_classes = [IsAdminOrModerator]

    @swagger_auto_schema(
        operation_summary="Редагування підкатегорії",
        operation_description="Оновлює існуючу підкатегорію за її `id`. Можливе часткове оновлення.",
        request_body=SubCategorySerializer,
        responses={200: SubCategorySerializer, 404: "Підкатегорію не знайдено"}
    )
    async def patch(self, request, subcategory_id):
        subcategory = await sync_to_async(SubCategory.objects.filter(id=subcategory_id).first)()
        if not subcategory:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SubCategorySerializer(subcategory, data=request.data, partial=True)
        await sync_to_async(serializer.is_valid)(raise_exception=True)
        await sync_to_async(serializer.save)()
        return Response(serializer.data, status=status.HTTP_200_OK)

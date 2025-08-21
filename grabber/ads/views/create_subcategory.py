from adrf.views import APIView
from asgiref.sync import sync_to_async
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from ads.serializers.subcategory import SubCategorySerializer
from users.permissions.permissions import IsAdminOrModerator


class CreateSubCategoryAPIView(APIView):
    permission_classes = [IsAdminOrModerator]

    @swagger_auto_schema(
        operation_summary="Створення підкатегорії",
        operation_description="Створює нову підкатегорію, вказавши `name`, `description`, `image` і `category` (id категорії)",
        request_body=SubCategorySerializer,
        responses={201: SubCategorySerializer}
    )
    async def post(self, request):
        serializer = SubCategorySerializer(data=request.data)
        await sync_to_async(serializer.is_valid)(raise_exception=True)
        await sync_to_async(serializer.save)()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

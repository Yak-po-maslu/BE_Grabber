from adrf.views import APIView
from asgiref.sync import sync_to_async
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


from ads.serializers.category import CategorySerializer
from users.permissions.permissions import IsAdminOrModerator

class CreateCategoryAPIView(APIView):
    permission_classes = [IsAdminOrModerator]


    @swagger_auto_schema(
        operation_summary="Створення категорії",
        operation_description="Створює нову категорію оголошень із назвою в полі `name`",
        request_body=CategorySerializer,
        responses={201: CategorySerializer}
    )
    async def post(self, request):
        serializer = CategorySerializer(data=request.data)
        await sync_to_async(serializer.is_valid)(raise_exception=True)

        await sync_to_async(serializer.save)()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

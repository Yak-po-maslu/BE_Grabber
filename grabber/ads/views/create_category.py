from adrf.views import APIView
from asgiref.sync import sync_to_async
from rest_framework import status
from rest_framework.response import Response

from ads.models import Category
from ads.serializers.category import CategorySerializer
from users.permissions.permissions import IsAdminOrModerator


class CreateCategoryAPIView(APIView):
    permission_classes = [IsAdminOrModerator]

    async def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        await sync_to_async(Category.objects.create)(**serializer.validated_data)
        # must impl serializer.save() and add to urls and test
        return Response(serializer.data, status=status.HTTP_201_CREATED)

from adrf.views import APIView
from asgiref.sync import sync_to_async
from rest_framework import status
from rest_framework.response import Response

from ads.models import Category
from ads.serializers.category import CategorySerializer


class GetCategoriesAPIView(APIView):
    async def get(self, request):
        categories = await sync_to_async(list)(Category.objects.all())
        serializer = CategorySerializer(instance=categories, many=True)

        return Response(data = serializer.data, status=status.HTTP_200_OK)

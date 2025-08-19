from adrf.views import APIView
from asgiref.sync import sync_to_async
from rest_framework.response import Response
from rest_framework import status
from ads.models import SubCategory
from ads.serializers.subcategory import SubCategorySerializer


class GetSubCategoriesAPIView(APIView):
    async def get(self, request):
        category_id = request.query_params.get("category_id")

        if category_id:
            subcategories = await sync_to_async(list)(
                SubCategory.objects.filter(category_id=category_id)
            )
        else:
            subcategories = await sync_to_async(list)(SubCategory.objects.all())

        serializer_data = await sync_to_async(
            lambda: SubCategorySerializer(subcategories, many=True).data
        )()
        return Response(serializer_data, status=status.HTTP_200_OK)

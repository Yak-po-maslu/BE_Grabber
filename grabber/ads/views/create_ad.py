from adrf.views import APIView
from asgiref.sync import sync_to_async
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from services.upload_one_image import UploadOneImage
from . import user_has_permissions
from ..models import Ad, Category
from ..serializers.ad import AdSerializer
from ..serializers.create_ad import CreateAdsSerializer


import logging

logger = logging.getLogger('ads')

class AsyncCreateAdsView(APIView):
    permission_classes = (IsAuthenticated, user_has_permissions.IsSellerOrAdminOrModerator)
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
        consumes=["multipart/form-data"],
        request_body=CreateAdsSerializer,
        responses={201: "Created"},
        manual_parameters=[
            openapi.Parameter(
                name="images",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_FILE),
                description="Список зображень",
                required=True,
                collectionFormat='multi',  # важный параметр для списков в multipart
            ),
            openapi.Parameter(
                name="category_name",
                in_=openapi.IN_FORM,  # Параметр передаётся в строке запроса (например, ?category_name=books)
                description="Название категории для фильтрации",
                required=True,
                type=openapi.TYPE_STRING,
                example="books"
            )
        ],
    )
    async def post(self, request):
        serializer = CreateAdsSerializer(data=request.data)
        await sync_to_async(serializer.is_valid)(raise_exception=True)

        category_name = request.data.get('category_name')
        if category_name:
            try:
                category = await sync_to_async(Category.objects.get)(name=category_name)
            except Category.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND,
                                data={'detail': f'category with name {category_name} not found'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'detail':"category name is required"})


        image_files = request.FILES.getlist("images")

        if not image_files or len(image_files) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'detail': 'Необхідно завантажити хоча б одне зображення'})

        if image_files:
            try:
                UploadOneImage.images_upload_validation(request)
                image_paths = await UploadOneImage.get_image_paths(request)
            except Exception:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'exception on upload images'})
            print("FILES:", image_paths)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'images is required'})

        ad = Ad(**serializer.validated_data, images=image_paths, category=category, user=request.user)

        result = serializer.data
        result['images'] = image_paths
        result['category'] = category.name
        result['user_id'] = request.user.id
        result['user_email'] = request.user.email
        result['ad_id'] = ad.id


        await sync_to_async(ad.save)()
        response_data = await sync_to_async(lambda : AdSerializer(ad).data)()
        return Response(data=response_data, status=status.HTTP_201_CREATED)


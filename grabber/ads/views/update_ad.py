from typing import cast
from xmlrpc.client import Fault

from adrf.views import APIView
from asgiref.sync import sync_to_async
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from services.upload_one_image import UploadOneImage
from users.permissions.permissions import IsSellerOrAdminOrModerator
from users.models import CustomUser
from ..models import Ad, Category
from ..serializers.ad import AdSerializer
from ..serializers.create_ad import CreateAdsSerializer
from ..serializers.update_ad_serializer import UpdateAdSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UpdateAdView(APIView):
    permission_classes = (IsSellerOrAdminOrModerator,)
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Оновлює оголошення. Продавці можуть редагувати лише свої оголошення. Модератори та адміністратори — будь-яке.",
        consumes=["multipart/form-data"],

        manual_parameters=[
            openapi.Parameter(
                'ad_id', openapi.IN_PATH,
                description="ID оголошення",
                required=True,
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name="images",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_FILE),
                description="Список зображень",
                required=False,
                collectionFormat='multi',  # важный параметр для списков в multipart
            ),
            openapi.Parameter(
                name="category_name",
                in_=openapi.IN_FORM,  # Параметр передаётся в строке запроса (например, ?category_name=books)
                description="Название категории для фильтрации",
                required=False,
                type=openapi.TYPE_STRING,
                example="books"
            )
        ],
        request_body=UpdateAdSerializer,
        responses={
            200: 'Оголошення успішно оновлено',
            400: 'Помилка при оновленні',
            403: 'Недостатньо прав',
        },


    )
    async def patch(self, request, ad_id):
        user = cast(CustomUser, request.user)
        user_status = user.role
        result = {}

        try:
            if user_status in ['moderator', 'admin']:
                ad = await sync_to_async(Ad.objects.get)(id=ad_id)
            elif user_status == 'seller':
                ad = await sync_to_async(Ad.objects.get)(id=ad_id, user=user)
            else:
                return Response({"detail": "Недостатньо прав"}, status=status.HTTP_403_FORBIDDEN)
        except Ad.DoesNotExist:
            return Response({"detail": "Оголошення не знайдено"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CreateAdsSerializer(ad, data=request.data, partial=True)

        if serializer.is_valid():
            result = serializer.validated_data
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        category_name = request.data.get('category_name')
        if category_name:
            try:
                category = await sync_to_async(Category.objects.get)(name=category_name)
                result['category'] = category
            except Category.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND,
                                data={'detail':f'category with name {category_name} not found'})


        image_files = request.FILES.getlist('images')

        if image_files:
            try:
                UploadOneImage.images_upload_validation(request)
                image_paths = await UploadOneImage.get_image_paths(request)
                result['images'] = image_paths
            except Exception:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'detail': 'exception on upload images'})
            print("FILES:", image_paths)

            # Обновляем только поля, которые пришли
        for field, value in result.items():
            setattr(ad, field, value)

        await sync_to_async(ad.save)()
        response_data = await sync_to_async(lambda : AdSerializer(ad).data)()

        return Response(response_data, status=status.HTTP_200_OK)


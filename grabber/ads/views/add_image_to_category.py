from adrf.views import APIView
from asgiref.sync import sync_to_async
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from users.permissions.permissions import IsAdminOrModerator
from rest_framework.response import Response
from services.upload_one_image import UploadOneImage
from ..models import Category
from serializers.upload_image import UploadedImageSerializer


class AddImageToCategoryAPIView(APIView):
    permission_classes = [IsAdminOrModerator]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Upload an image to a category",
        manual_parameters=[
            openapi.Parameter(
                name="image",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="The image file to upload",
                required=True,
            ),
        ],
        responses={
            201: openapi.Response(
                description="Uploaded successfully",
                schema=UploadedImageSerializer
            ),
            400: "Bad Request",
        },
        consumes=["multipart/form-data"],
    )
    async def post(self, request, category_id):
        try:
          category = await sync_to_async(Category.objects.get)(id=category_id)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'},status=status.HTTP_404_NOT_FOUND )

        # use image upload service
        image_path = await UploadOneImage.upload(request.data)

        category.image = image_path
        await sync_to_async(category.save)()

        return Response({'image_url': image_path}, status=status.HTTP_201_CREATED)

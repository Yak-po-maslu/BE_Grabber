from adrf.views import APIView
from asgiref.sync import sync_to_async
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from users.permissions.permissions import IsAdminOrModerator
from services.upload_one_image import UploadOneImage
from ads.models import SubCategory
from ads.serializers.upload_image_serializer import UploadedImageSerializer


class AddImageToSubCategoryAPIView(APIView):
    permission_classes = [IsAdminOrModerator]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Upload an image to a subcategory",
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
    async def post(self, request, subcategory_id):
        try:
            subcategory = await sync_to_async(SubCategory.objects.get)(id=subcategory_id)
        except SubCategory.DoesNotExist:
            return Response({'error': 'Subcategory not found'}, status=status.HTTP_404_NOT_FOUND)

        image_path = await UploadOneImage.upload(request.data)
        subcategory.image = image_path
        await sync_to_async(subcategory.save)()

        return Response({'image_url': image_path}, status=status.HTTP_201_CREATED)

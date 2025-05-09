from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from adrf.views import APIView
from asgiref.sync import sync_to_async
from ..serializers.upload_image import UploadedImageSerializer

class ImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Upload an image",
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
    async def post(self, request):
        serializer = UploadedImageSerializer(data=request.data)
        if serializer.is_valid():
            await sync_to_async(serializer.save)()
            return Response(
                {"message": "Image uploaded successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

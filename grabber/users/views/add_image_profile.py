from adrf.views import APIView
from asgiref.sync import sync_to_async
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from serializers.upload_image import UploadedImageSerializer
from services.upload_one_image import UploadOneImage


class AddImageProfileView(APIView):
    permission_classes = [IsAuthenticated]
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
        user = request.user
        image_path = await UploadOneImage.upload(request.data)
        user.user_photo = image_path
        await sync_to_async(user.save)()

        return Response({"image_url":image_path}, status=status.HTTP_201_CREATED)



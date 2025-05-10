from adrf.views import APIView
from asgiref.sync import sync_to_async
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from services.upload_one_image import UploadOneImage
from . import user_has_permissions
from ..models import Ad
from serializers.upload_image import UploadedImageSerializer


class AddImageToAdsAPIView(APIView):
    permission_classes = [IsAuthenticated, user_has_permissions.IsSellerOrAdminOrModerator]
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
    async def post(self, request, ad_id):
        try:
          ad = await sync_to_async(Ad.objects.get)(id=ad_id,user=request.user)
        except Ad.DoesNotExist:
            return Response({'error': 'Ad not found or access denied'},status=status.HTTP_404_NOT_FOUND )

        # use image upload service
        image_path = await UploadOneImage.upload(request.data)

        ad.images.append(image_path)

        await sync_to_async(ad.save)()

        return Response({'image_url': image_path}, status=status.HTTP_201_CREATED)

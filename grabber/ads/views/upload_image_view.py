from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ads.models import Ad
from ads.services.image_upload import upload_image_and_get_url

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB

class UploadImageView(APIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_summary="Завантажити зображення",
        operation_description="Завантаження зображення (JPEG, PNG, до 5MB) для оголошення. Не більше 10 фото на одне оголошення.",
        manual_parameters=[
            openapi.Parameter(
                name='image',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description='Файл зображення (jpeg/png, до 5MB)'
            ),
            openapi.Parameter(
                name='ad_id',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_INTEGER,
                required=True,
                description='ID оголошення, до якого додається зображення'
            ),
        ],
        responses={
            201: openapi.Response(description="URL зображення", examples={
                "application/json": {"url": "http://localhost:8000/media/uploads/example.jpg"}
            }),
            400: "Помилка: невірний формат, великий розмір або перевищено 10 фото",
            404: "Оголошення не знайдено"
        }
    )
    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image')
        ad_id = request.data.get('ad_id')

        if not image_file:
            return Response({'error': 'No image uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        if not ad_id:
            return Response({'error': 'Missing ad_id'}, status=status.HTTP_400_BAD_REQUEST)

        # Перевірка на існування оголошення
        try:
            ad = Ad.objects.get(pk=ad_id)
        except Ad.DoesNotExist:
            return Response({'error': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)

        # Перевірка кількості фото
        current_images = ad.images if isinstance(ad.images, list) else []
        if len(current_images) >= 10:
            return Response({'error': 'You can upload up to 10 images per ad'}, status=status.HTTP_400_BAD_REQUEST)

        # Перевірка розміру
        if image_file.size > MAX_IMAGE_SIZE:
            return Response({'error': 'Image size exceeds 5MB'}, status=status.HTTP_400_BAD_REQUEST)

        # Перевірка типу
        if image_file.content_type not in ['image/jpeg', 'image/png']:
            return Response({'error': 'Invalid image format. Only JPEG and PNG allowed'}, status=status.HTTP_400_BAD_REQUEST)

        # Зберігаємо зображення
        image_url = upload_image_and_get_url(image_file, request)

        # Додаємо URL до оголошення
        current_images.append(image_url)
        ad.images = current_images
        ad.save()

        return Response({'url': image_url}, status=status.HTTP_201_CREATED)
class DeleteAdImageView(APIView):
    @swagger_auto_schema(
        operation_summary="Видалити зображення оголошення",
        operation_description="Видаляє вказане зображення з оголошення за ad_id та image_url.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['ad_id', 'image_url'],
            properties={
                'ad_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID оголошення'),
                'image_url': openapi.Schema(type=openapi.TYPE_STRING, description='URL зображення для видалення'),
            },
        ),
        responses={
            200: openapi.Response(description="Зображення видалено"),
            400: "Помилка запиту",
            404: "Оголошення не знайдено",
        },
    )
    def delete(self, request, *args, **kwargs):
        ad_id = request.data.get('ad_id')
        image_url = request.data.get('image_url')

        if not ad_id or not image_url:
            return Response({'error': 'ad_id and image_url are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ad = Ad.objects.get(id=ad_id)
        except Ad.DoesNotExist:
            return Response({'error': 'Ad not found'}, status=status.HTTP_404_NOT_FOUND)

        if image_url not in ad.images:
            return Response({'error': 'Image not found in ad'}, status=status.HTTP_400_BAD_REQUEST)

        ad.images.remove(image_url)

        ad.save()
        return Response({'message': 'Image deleted'}, status=status.HTTP_200_OK)
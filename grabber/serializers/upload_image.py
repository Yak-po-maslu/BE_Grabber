from rest_framework import serializers
from PIL import Image
import io

from ads.models import UploadedImageV1

MAX_IMAGE_SIZE_MB = 5
ALLOWED_TYPES = ['image/jpeg', 'image/png']


class UploadedImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = UploadedImageV1
        fields = ['id', 'image', 'uploaded_at']

    def validate_image(self, image):
        # Размер
        if image.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
            raise serializers.ValidationError(f"Максимальний розмір зображення — {MAX_IMAGE_SIZE_MB}MB.")

        # MIME-тип (можно улучшить через imghdr или Pillow)
        if image.content_type not in ALLOWED_TYPES:
            raise serializers.ValidationError(f"Дозволені тільки {ALLOWED_TYPES}.")

        # Доп. проверка — можно ли открыть как изображение
        try:
            img = Image.open(image)
            img.verify()
        except Exception:
            raise serializers.ValidationError("Файл не є дійсним зображенням.")

        return image

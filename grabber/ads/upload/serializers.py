from rest_framework import serializers
from .models import UploadedImage

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ('image',)

    def validate_image(self, value):
        # Перевірка розміру (максимум 2MB)
        max_size = 2 * 1024 * 1024  # 2 мегабайти
        if value.size > max_size:
            raise serializers.ValidationError("Максимальний розмір зображення — 2MB.")

        # Перевірка MIME-типу
        valid_mime_types = ['image/jpeg', 'image/png']
        if hasattr(value, 'content_type'):
            if value.content_type not in valid_mime_types:
                raise serializers.ValidationError("Дозволені тільки JPEG та PNG зображення.")
        else:
            raise serializers.ValidationError("Не вдалося визначити тип файлу.")

        return value

from asgiref.sync import sync_to_async
from django.db import DatabaseError
from serializers.upload_image import UploadedImageSerializer
from rest_framework.exceptions import ValidationError

class UploadOneImage:
    @staticmethod
    async def upload(data):
        serializer = UploadedImageSerializer(data=data)
        is_valid = await sync_to_async(serializer.is_valid)(raise_exception=True)

        if not is_valid:
            raise ValidationError(serializer.errors)

        try:
            image_instance = await sync_to_async(serializer.save)()
            image_path = image_instance.image.url
            return image_path
        except DatabaseError as db_error:
            raise db_error
        except Exception as e:
            raise e





from asgiref.sync import sync_to_async
from django.db import DatabaseError
from serializers.upload_image import UploadedImageSerializer
from rest_framework.exceptions import ValidationError

class UploadOneImage:
    @staticmethod
    async def upload(data):
        serializer = UploadedImageSerializer(data=data)
        print('data', data)
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

    @staticmethod
    def images_upload_validation(request):
        images = request.FILES.getlist("images")

        if not images:
            raise Exception("Потрібно завантажити хоча б одне зображення.")
        if len(images) > 5:
            raise Exception("Максимум 5 зображень.")

        for image in images:
            if not image or image == "undefined":
                raise Exception("Поле зображення не може бути пустим.")

        return images

    @staticmethod
    async def get_image_paths(request):
        # 1) Забираем именно файлы из request.FILES
        image_files = request.FILES.getlist('images')  # Список InMemoryUploadedFile
        print('image_f:',image_files)
        image_paths = []
        errors = []
        if not image_files:
            return image_paths

        for image in image_files:
            # image — это уже InMemoryUploadedFile, его можно сразу передавать дальше
            try:
                print("image:",image)
                path = await UploadOneImage.upload({'image': image})
                image_paths.append(path)
            except Exception as e:
                errors.append(e)

        if errors:
            # Можно либо вернуть ошибки, либо исключить плохие изображения
            raise ValidationError({"errors": errors})

        return image_paths



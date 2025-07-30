from ..models import UploadedImageV1

def upload_image_and_get_url(image_file, request):
    """
    Зберігає зображення (локально або у хмарі) та повертає абсолютний URL.
    """
    uploaded = UploadedImageV1.objects.create(image=image_file)
    return request.build_absolute_uri(uploaded.image.url)

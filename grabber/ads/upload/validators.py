from django.core.exceptions import ValidationError
from PIL import Image

def validate_image(file):
    max_size = 5 * 1024 * 1024  # 5MB
    if file.size > max_size:
        raise ValidationError("Image size exceeds 5MB")

    try:
        img = Image.open(file)
        if img.format not in ('JPEG', 'PNG'):
            raise ValidationError("Only JPEG and PNG images are allowed")
    except Exception:
        raise ValidationError("Invalid image")

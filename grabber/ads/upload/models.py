from django.db import models
from .validators import validate_image

def upload_to(instance, filename):
    return f'uploads/{filename}'

class UploadedImage(models.Model):
    image = models.ImageField(upload_to=upload_to, validators=[validate_image])
    uploaded_at = models.DateTimeField(auto_now_add=True)

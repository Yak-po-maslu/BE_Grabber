from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")

    def __str__(self):
        return self.name

class Ad(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    images = models.JSONField(default=list)  # масив шляхів до фото
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ads')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey( Category,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  related_name='ads',
                                  verbose_name="Category") # ✅ поле категорії
    rejection_reason = models.TextField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    
    is_recommended = models.BooleanField(default=False)

    moderated_by = models.ForeignKey(
        'users.CustomUser',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='moderated_ads'
    )
    moderated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title



class UploadedImageV1(models.Model):
    image = models.ImageField(upload_to='uploads/', )  # путь в бакете
    uploaded_at = models.DateTimeField(auto_now_add=True)

class AdView(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    session_key = models.CharField(max_length=40, null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('ad', 'ip_address')  # Один просмотр с IP
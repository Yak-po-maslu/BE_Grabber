from django.db import models
from django.db import models
from django.conf import settings

class Ad(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.JSONField(default=list)  # масив шляхів до фото
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ads')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)
    
    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories",
        verbose_name="Parent Category"
    )
    name = models.CharField(max_length=100, verbose_name="Subcategory Name")
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)

    class Meta:
        unique_together = ("category", "name")
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"

    def __str__(self):
        return f"{self.category.name} -> {self.name}"

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
    location = models.CharField(max_length=255, blank=True, null=True)
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

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # для сортування

    def __str__(self):
        return self.question
class FavoriteAd(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_ads')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'ad')

class Review(models.Model):
    product = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1-5, наприклад
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  # Один користувач = один відгук на товар

class ProductComment(models.Model):
    product_id = models.IntegerField()
    user_name = models.CharField(max_length=50)
    rating = models.PositiveSmallIntegerField()
    comment_text = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} ({self.rating}★): {self.comment_text[:20]}"
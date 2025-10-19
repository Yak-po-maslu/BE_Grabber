from django.db import models
from django.conf import settings
from django.utils.text import slugify

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
    images = models.JSONField(default=list)  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ads')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey( Category,
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  related_name='ads',
                                  verbose_name="Category") 
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ads',
        verbose_name="Subcategory"
    )
    rejection_reason = models.TextField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    is_popular = models.BooleanField(default=False)
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

    def add_view(self):
        """Додає перегляд і робить оголошення популярним, якщо переглядів достатньо"""
        POPULAR_THRESHOLD = 3  # minimum number of views for popularity
        self.views += 1
        if self.views >= POPULAR_THRESHOLD:
            self.is_popular = True
        self.save(update_fields=['views', 'is_popular'])

class UploadedImageV1(models.Model):
    image = models.ImageField(upload_to='uploads/', )  
    uploaded_at = models.DateTimeField(auto_now_add=True)

class AdView(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    session_key = models.CharField(max_length=40, null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('ad', 'ip_address')  

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True) 

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
    rating = models.PositiveSmallIntegerField()  
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')  # One user = one review per product

class ProductComment(models.Model):
    product_id = models.IntegerField()
    user_name = models.CharField(max_length=50)
    rating = models.PositiveSmallIntegerField()
    comment_text = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} ({self.rating}★): {self.comment_text[:20]}"
    
class Attribute(models.Model):
    TEXT = "text"
    NUMBER = "number"
    BOOLEAN = "bool"
    CHOICE = "choice"       # single value from the list
   # If multiple values are needed, you can also add MULTICHOICE = "multichoice" here

    TYPE_CHOICES = [
        (TEXT, "Text"),
        (NUMBER, "Number"),
        (BOOLEAN, "Boolean"),
        (CHOICE, "Choice"),
    ]

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="attributes"
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, db_index=True)
    type = models.CharField(max_length=12, choices=TYPE_CHOICES, default=TEXT)

    # additionally — for frontend:
    unit = models.CharField(max_length=20, blank=True, default="")
    is_filterable = models.BooleanField(default=True)
    is_required = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("category", "slug")
        ordering = ("sort_order", "id")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name}:{self.name}"


class AttributeOption(models.Model):
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="options"
    )
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=100)  
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("attribute", "value")
        ordering = ("sort_order", "id")

    def __str__(self):
        return f"{self.attribute.slug} = {self.label}"


class AdAttributeValue(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="attributes")
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value_text = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    value_number = models.DecimalField(max_digits=14, decimal_places=4, blank=True, null=True, db_index=True)
    value_bool = models.BooleanField(blank=True, null=True, db_index=True)
    option = models.ForeignKey(
        AttributeOption, null=True, blank=True, on_delete=models.SET_NULL, related_name="ad_values"
    )

    class Meta:
        unique_together = ("ad", "attribute")
        indexes = [
            models.Index(fields=["attribute", "value_text"]),
            models.Index(fields=["attribute", "value_number"]),
            models.Index(fields=["attribute", "value_bool"]),
            models.Index(fields=["attribute", "option"]),
        ]

    def __str__(self):
        return f"{self.ad_id}:{self.attribute.slug}"
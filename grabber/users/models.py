from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
from django.db import models
from django.conf import settings
from ads.models import Ad

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        BUYER = "buyer", "Покупець"
        SELLER = "seller", "Продавесь"
        MODERATOR = "moderator", "Модератор"
        ADMIN = "admin", "Адмін"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.SELLER,
    )
    email = models.EmailField(unique=True)
    description = models.fields.CharField(max_length=255, default="")
    social = models.URLField(blank=True)
    first_name = models.CharField(max_length=255, default="Anonymous")
    last_name = models.CharField(max_length=255, default="Anonymous")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=255, blank=False, default='+38033333333')
    show_phone = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255, blank=True)
    user_photo = models.CharField(max_length=500, blank=True, default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # email уже обязателен, не дублируем

    objects = UserManager()



    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(
            subject,
            message,
            from_email,
            [self.email],
            **kwargs,
        )

    def __str__(self):
        return self.email


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('github', 'GitHub'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('youtube', 'Youtube'),
        ('telegram', 'Telegram'),
        ('viber', 'Viber'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='social_links'
    )
    platform = models.CharField(
        max_length=50,
        choices=PLATFORM_CHOICES,
        default='other'
    )
    url = models.URLField()

    def __str__(self):
        return f"{self.user.email} - {self.platform}"


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Ad, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product')  # один товар один раз у кошику

# Create your models here.

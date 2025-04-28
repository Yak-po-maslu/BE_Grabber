from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
from django.db import models

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
    email = models.EmailField(unique=True)
    #full_name = models.CharField(max_length=255, blank=True)
    first_name = models.CharField(max_length=255, default="Anonymous")
    last_name = models.CharField(max_length=255, default="Anonymous")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=255, blank=False, default='+38033333333')
    date_joined = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255, blank=True)
    # если хочешь ещё что-то, например:
    # phone = models.CharField(max_length=20, blank=True)
    # avatar = models.ImageField(upload_to='avatars/', blank=True)

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

# Create your models here.


from users.views import CustomUser
from django.core.mail import send_mail
from django.conf import settings
from asgiref.sync import sync_to_async

User = CustomUser


async def send_email(user, subject: str, message: str):
    to_email = user.email
    print("Send to email:",to_email)
    await sync_to_async(send_mail)(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email],
        fail_silently=False
    )
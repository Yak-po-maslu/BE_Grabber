from adrf.views import APIView
from asgiref.sync import sync_to_async
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from subscriptions.models import NewsletterSubscriber
from subscriptions.serializers.create_sub import NewsletterSubscriberSerializer

class SubscribeView(APIView):
    @swagger_auto_schema(
        operation_description="Додає email користувача до списку підписників.",
        request_body=NewsletterSubscriberSerializer,
        responses={
            201: openapi.Response(description="Підписка успішна!"),
            409: openapi.Response(description="Ви вже підписані."),
            400: openapi.Response(description="Помилка валідації email."),
        }
    )
    async def post(self, request):
        serializer = NewsletterSubscriberSerializer(data=request.data)
        is_valid = await sync_to_async(serializer.is_valid)()
        if is_valid:
            email = serializer.validated_data["email"]

            subscriber, created = await sync_to_async(
            NewsletterSubscriber.objects.get_or_create
            )(email=email)

            if not created:
                return Response(
                    {"message": "Ви вже підписані."},
                    status=status.HTTP_409_CONFLICT
                )

            return Response(
                {"message": "Підписка успішна!"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
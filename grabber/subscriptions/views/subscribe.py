# subscriptions/views.py

from adrf.views import APIView
from asgiref.sync import sync_to_async
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status

from subscriptions.serializers.create_sub import NewsletterSubscriberSerializer


class SubscribeView(APIView):
    @swagger_auto_schema(
        operation_description="Додає email користувача до списку підписників.",
        request_body=NewsletterSubscriberSerializer,
        responses={
            201: openapi.Response(description="Підписка успішна!"),
            400: openapi.Response(description="Помилка валідації email або вже підписаний."),
        }
    )
    async def post(self, request):
        serializer = NewsletterSubscriberSerializer(data=request.data)
        is_valid = await sync_to_async(serializer.is_valid)()
        if is_valid:
            await sync_to_async(serializer.save)()
            return Response({'message': 'Підписка успішна!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





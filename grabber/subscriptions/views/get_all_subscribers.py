from adrf.views import APIView
from asgiref.sync import sync_to_async
from drf_yasg.utils import swagger_auto_schema

from subscriptions.models import NewsletterSubscriber
from subscriptions.serializers.create_sub import NewsletterSubscriberSerializer
from rest_framework import status
from rest_framework.response import Response

from users.permissions.permissions import IsAdminOrModerator


class GetAllSubscribersAPIView(APIView):

    permission_classes = [IsAdminOrModerator]

    @swagger_auto_schema(
        operation_description="Адмін або модератор може виконати цю дію.",

    )
    async def get(self, request):
        subs = await sync_to_async(list)(NewsletterSubscriber.objects.all())
        serializer_data = await sync_to_async(lambda: NewsletterSubscriberSerializer(instance=subs, many=True).data)()

        return Response(data=serializer_data, status=status.HTTP_200_OK)
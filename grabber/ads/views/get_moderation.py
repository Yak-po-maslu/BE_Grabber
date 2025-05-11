from adrf.views import APIView
from asgiref.sync import sync_to_async
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions.permissions import IsModerator
from ..models import Ad
from ..serializers.ad import AdSerializer


class GetModerationView(APIView):
    permission_classes = [IsAuthenticated, IsModerator]

    @swagger_auto_schema(
        operation_description="Get all ads with status 'pending' for moderation",
        responses={200: AdSerializer(many=True)})
    async def get(self, request):
        ads = await sync_to_async(lambda: list(Ad.objects.filter(status="pending")))()
        serializer = AdSerializer(ads, many=True)

        return Response({"ads": serializer.data}, status=status.HTTP_200_OK)

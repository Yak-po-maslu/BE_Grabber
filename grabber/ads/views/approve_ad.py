from django.utils import timezone
from adrf.views import APIView
from asgiref.sync import sync_to_async
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions.permissions import IsModerator
from ..models import Ad
from ..serializers.ad import AdSerializer


class ApproveAdAPIView(APIView):
    permission_classes = [IsAuthenticated, IsModerator]


    @swagger_auto_schema(
        operation_description="Approve ad with given ID",
        responses={
            200: openapi.Response(description="Ad approved"),
            400: openapi.Response(description="Ad already approved/rejected"),
            404: openapi.Response(description="Ad not found"),
        }
    )
    async def post(self, request, ad_id):
        ad = await sync_to_async(Ad.objects.filter(id=ad_id).first)()

        if not ad:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if ad.status != "pending":
            return Response({"detail": f"Ad's status is already {ad.status}"},
                            status=status.HTTP_400_BAD_REQUEST)

        ad.status = "approved"
        ad.moderated_by = request.user
        ad.moderated_at = timezone.now()
        await sync_to_async(ad.save)()

        serializer = AdSerializer(ad)

        return Response(serializer.data, status=status.HTTP_200_OK)


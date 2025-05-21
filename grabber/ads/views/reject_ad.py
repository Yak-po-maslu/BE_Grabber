from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from adrf.views import APIView
from asgiref.sync import sync_to_async
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from grabber import settings
from services.send_email import send_email
from users.permissions import permissions
from ..models import Ad
from ..serializers.ad import AdSerializer


class RejectAdAPIView(APIView):
    permission_classes = [IsAuthenticated,permissions.IsModerator]

    @swagger_auto_schema(
        operation_description="Reject ad with given ID and provide a rejection reason",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["rejection_reason"],
            properties={
                "rejection_reason": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Reason for rejecting the ad",
                    example="Spam or inappropriate content"
                )
            }
        ),
        responses={
            200: openapi.Response(description="Ad rejected"),
            400: openapi.Response(description="Missing reason or invalid status"),
            404: openapi.Response(description="Ad not found"),
        }
    )
    async def post(self, request, ad_id):
        ad = await sync_to_async(
            Ad.objects.select_related('user').filter(id=ad_id).first
        )()
        if not ad:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not ad.rejection_reason:
            return Response({"detail":"rejection_reason is required!"},status=status.HTTP_400_BAD_REQUEST)

        if ad.status != "pending":
            return Response({"detail":f"Ad status is {ad.status}"},status=status.HTTP_403_FORBIDDEN)

        ad.status = "rejected"
        ad.moderated_by = request.user
        ad.moderated_at = timezone.now()
        ad.rejection_reason = request.data["rejection_reason"]

        await sync_to_async(ad.save)()
        serializer = AdSerializer(ad)

        title = f"Reject Ad with title {ad.title}"
        message = f"""Ad with title {ad.title} has been rejected by moderator {request.user},
        rejection reason: {request.data["rejection_reason"]}"""


        await send_email(ad.user, title, message)


        return Response(serializer.data,status=status.HTTP_200_OK)
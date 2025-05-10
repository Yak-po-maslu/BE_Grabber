from adrf.views import APIView
from asgiref.sync import sync_to_async
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import user_has_permissions
from ..serializers.create_ad import CreateAdsSerializer
from ..models import Ad



class AsyncCreateAdsView(APIView):
    permission_classes = (IsAuthenticated, user_has_permissions.IsSellerOrAdminOrModerator)

    @swagger_auto_schema(request_body=CreateAdsSerializer, responses={201: "Created"})
    async def post(self, request):
        serializer = CreateAdsSerializer(data=request.data)
        await sync_to_async(serializer.is_valid)(raise_exception=True)
        await sync_to_async(serializer.save)(user=request.user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


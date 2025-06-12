from adrf.views import APIView as AsyncAPIView
from asgiref.sync import sync_to_async
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..serializers.serializers import UserProfileSerializer, UserEditProfileSerializer


class AsyncUserProfileView(AsyncAPIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        method='get',
        responses={status.HTTP_200_OK: UserProfileSerializer()},

    )
    @action(detail=True, methods=['get'], url_path='profile')
    async def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        method='patch',
        request_body=UserProfileSerializer,
        responses={status.HTTP_200_OK: UserProfileSerializer()},

    )
    @action(detail=True, methods=['patch'], url_path='profile')
    async def patch(self, request):
        serializer = UserEditProfileSerializer(
            request.user,
            data=request.data,
            partial=True  # частичное обновление
        )

        is_valid = await sync_to_async(serializer.is_valid)()

        if is_valid:
            await sync_to_async(serializer.save)()
            response_data = await sync_to_async(lambda: UserProfileSerializer(request.user).data)()
            return Response(response_data)



        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
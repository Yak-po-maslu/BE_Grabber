from adrf.views import APIView as AsyncAPIView
from asgiref.sync import sync_to_async
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..serializers.serializers import UserProfileSerializer


class AsyncUserProfileView(AsyncAPIView):

    permission_classes = [IsAuthenticated]
    async def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    async def patch(self, request):
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True  # частичное обновление
        )

        is_valid = await sync_to_async(serializer.is_valid)()

        if is_valid:
            await sync_to_async(serializer.save)()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
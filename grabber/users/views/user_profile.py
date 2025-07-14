from adrf.views import APIView as AsyncAPIView
from asgiref.sync import sync_to_async
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import CustomUser
from ..serializers.serializers import UserProfileSerializer, UserEditProfileSerializer
from ..utils.getUserData import get_user_data


class AsyncUserProfileView(AsyncAPIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        method='get',
        responses={status.HTTP_200_OK: UserProfileSerializer()},

    )
    @action(detail=True, methods=['get'], url_path='profile')
    async def get(self, request):
        user = await sync_to_async(CustomUser.objects.prefetch_related('social_links').get)(pk=request.user.pk)

        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        method='patch',
        request_body=UserEditProfileSerializer,
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
            #response_data = await sync_to_async(lambda: UserProfileSerializer(request.user).data)()
            response_data = await sync_to_async(get_user_data)(request.user)
            return Response(response_data)



        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
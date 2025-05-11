from http.client import responses

from asgiref.sync import sync_to_async
from adrf.views import APIView as AsyncAPIView
from django.utils.text import normalize_newlines
from drf_yasg.utils import swagger_auto_schema
from h11 import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .logout import AsyncCookieViewLogout

from . import CustomUser

User = CustomUser

class AsyncDeleteUserView(AsyncAPIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        method='delete',
        responses={204: "Successfully logged out and deleted"},

    )
    @action(detail=True, methods=['delete'], url_path='delete_user')
    async def delete(self, request, *args, **kwargs):
        user = self.request.user

        await sync_to_async(user.delete)()

        logout_view = AsyncCookieViewLogout()
        logout_view.request = request
        response  = await logout_view.post(request)
        response.data = {'message': 'Successfully logged out and deleted'}
        response.status_code = 204

        return response




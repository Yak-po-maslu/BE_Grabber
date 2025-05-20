from typing import cast

from adrf.views import APIView
from asgiref.sync import sync_to_async
from rest_framework import status
from rest_framework.response import Response

from users.permissions.permissions import IsSellerOrAdminOrModerator
from users.models import CustomUser
from ..models import Ad
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class DeleteAdView(APIView):
    permission_classes = (IsSellerOrAdminOrModerator,)

    @swagger_auto_schema(
        operation_description="Видаляє оголошення. Доступ дозволено продавцям (лише свої оголошення), модераторам і адміністраторам (будь-які оголошення).",
        manual_parameters=[
            openapi.Parameter(
                'ad_id', openapi.IN_PATH,
                description="ID оголошення",
                type=openapi.TYPE_INTEGER
            ),
        ],
        responses={
            204: 'Оголошення успішно видалено',
            400: 'Помилка при видаленні',
            403: 'Недостатньо прав для видалення',
        }
    )
    async def delete(self, request, ad_id):
        user = cast(CustomUser,request.user)
        user_status = user.role

        if user_status in ['moderator','admin']:
            try:
                ad = await sync_to_async(Ad.objects.get)(id=ad_id)
                await sync_to_async(ad.delete)()

                return Response(status=status.HTTP_204_NO_CONTENT)

            except Exception as e:
                return Response({"detail":str(e)},status=status.HTTP_400_BAD_REQUEST)

        if user_status == 'seller':
            try:
                ad = await sync_to_async(Ad.objects.get)(id=ad_id,user=user)
                await sync_to_async(ad.delete)()

                return Response( status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({"detail":str(e)},status=status.HTTP_400_BAD_REQUEST)




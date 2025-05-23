from typing import cast

from adrf.views import APIView
from asgiref.sync import sync_to_async
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from users.permissions.permissions import IsSellerOrAdminOrModerator
from users.models import CustomUser
from ..models import Ad
from grabber.ads.serializers.update_ad_serializer import UpdateAdSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UpdateAdView(APIView):
    permission_classes = (IsSellerOrAdminOrModerator,)
    parser_classes = (JSONParser,)

    @swagger_auto_schema(
        operation_description="Оновлює оголошення. Продавці можуть редагувати лише свої оголошення. Модератори та адміністратори — будь-яке.",
        manual_parameters=[
            openapi.Parameter(
                'ad_id', openapi.IN_PATH,
                description="ID оголошення",
                type=openapi.TYPE_INTEGER
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER),
                # додай поля, які ти хочеш дозволити оновлювати
            }
        ),
        responses={
            200: 'Оголошення успішно оновлено',
            400: 'Помилка при оновленні',
            403: 'Недостатньо прав',
        }
    )
    async def patch(self, request, ad_id):
        user = cast(CustomUser, request.user)
        user_status = user.role

        try:
            if user_status in ['moderator', 'admin']:
                ad = await sync_to_async(Ad.objects.get)(id=ad_id)
            elif user_status == 'seller':
                ad = await sync_to_async(Ad.objects.get)(id=ad_id, user=user)
            else:
                return Response({"detail": "Недостатньо прав"}, status=status.HTTP_403_FORBIDDEN)
        except Ad.DoesNotExist:
            return Response({"detail": "Оголошення не знайдено"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UpdateAdSerializer(ad, data=request.data, partial=True)
        if serializer.is_valid():
            await sync_to_async(serializer.save)()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

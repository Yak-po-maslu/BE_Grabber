from asgiref.sync import sync_to_async
from adrf.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from users.permissions.permissions import IsSellerOrAdminOrModerator
from ..models import Ad
from ..serializers.ad import AdSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GetAdsAPIView(APIView):
    permission_classes = [IsSellerOrAdminOrModerator]



    @swagger_auto_schema(
        operation_summary="Отримати всі оголошення користувача",
        operation_description="Повертає список оголошень, створених користувачем. Доступ мають продавці, модератори та адміністратори.",
        responses={
            200: openapi.Response(description="Список оголошень", schema=AdSerializer(many=True)),
            404: "Оголошення не знайдено або доступ заборонено"
        }
    )
    async def get(self, request):
        user = request.user

        ads_qs = await sync_to_async(list)(Ad.objects.filter(user=user))

        if not ads_qs:
            raise NotFound('Ads not found or access denied')

        serializer = AdSerializer(ads_qs, many=True)
        return Response(serializer.data)

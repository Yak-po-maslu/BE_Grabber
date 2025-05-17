from asgiref.sync import sync_to_async
from adrf.views import APIView as AsyncAPIView
from rest_framework.response import Response
from rest_framework import status
from ads.models import Ad
from ads.serializers.ad import AdSerializer
from django.db.models import Q

class MainPageAdListView(AsyncAPIView):
    async def get(self, request):
        # Асинхронно витягуємо базовий queryset
        base_qs = await sync_to_async(lambda: Ad.objects.filter(status="approved"))()

        # Обробка пошуку
        search = request.query_params.get("search")
        if search:
            base_qs = await sync_to_async(
                lambda: base_qs.filter(
                    Q(title__icontains=search) | Q(description__icontains=search)
                )
            )()

        # Сериалізація
        serializer = AdSerializer(base_qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
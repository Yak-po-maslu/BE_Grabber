from asgiref.sync import sync_to_async
from adrf.views import APIView as AsyncAPIView
from rest_framework.response import Response
from rest_framework import status
from ads.models import Ad
from ads.serializers.ad import AdSerializer
from django.db.models import Q

class MainPageAdListView(AsyncAPIView):
    async def get(self, request):
        search = request.query_params.get("search")

        ads = await sync_to_async(
            lambda: list(
                Ad.objects.filter(status="approved").filter(
                    Q(title__icontains=search) | Q(description__icontains=search)
                ) if search else Ad.objects.filter(status="approved")
            )
        )()

        serializer = await sync_to_async(AdSerializer)(ads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
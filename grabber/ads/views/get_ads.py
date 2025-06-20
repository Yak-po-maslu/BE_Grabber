from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ads.models import Ad
from ads.serializers.ad import AdSerializer
from ads.filters.filters import AdFilter
from ads.configs.ad_view_config import AdViewConfig  # імпортуємо нову конфігурацію
from rest_framework.views import APIView
from rest_framework.response import Response
class AdViewSet(viewsets.ModelViewSet):  # <-- замінили ReadOnlyModelViewSet
    serializer_class = AdSerializer

    def get_queryset(self):
        return Ad.objects.select_related('user', 'category')

   # Фільтри, пошук, сортування винесені в конфіг
    filter_backends = AdViewConfig.filter_backends
    filterset_class = AdViewConfig.filterset_class
    ordering_fields = AdViewConfig.ordering_fields
    search_fields = AdViewConfig.search_fields

class RecommendedAdsAPIView(APIView):
    def get(self, request):
        ads = Ad.objects.filter(
            is_recommended=True,
            status='approved'
        ).only('id', 'title', 'price', 'images', 'user_id', 'created_at', 'category')[:20]

        serializer = AdSerializer(ads, many=True)
        return Response(serializer.data)
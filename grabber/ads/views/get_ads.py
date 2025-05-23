from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ads.models import Ad
from ads.serializers.ad import AdSerializer
from ads.filters.filters import AdFilter
from ads.configs.ad_view_config import AdViewConfig  # імпортуємо нову конфігурацію

class AdViewSet(viewsets.ModelViewSet):  # <-- замінили ReadOnlyModelViewSet
    serializer_class = AdSerializer
    queryset = Ad.objects.all()

   # Фільтри, пошук, сортування винесені в конфіг
    filter_backends = AdViewConfig.filter_backends
    filterset_class = AdViewConfig.filterset_class
    ordering_fields = AdViewConfig.ordering_fields
    search_fields = AdViewConfig.search_fields
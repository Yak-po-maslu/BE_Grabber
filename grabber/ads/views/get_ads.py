from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ads.models import Ad
from ads.serializers.ad import AdSerializer
from ads.filters.filters import AdFilter  # <-- Імпортуємо твій кастомний фільтр

class AdViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AdSerializer
    queryset = Ad.objects.all()

    # Підключаємо фільтри та пошук
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = AdFilter
    ordering_fields = ['created_at', 'price']
    search_fields = ['title', 'description']
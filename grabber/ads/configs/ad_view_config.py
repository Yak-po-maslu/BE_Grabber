from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from ads.filters.filters import AdFilter  # вже використовується

class AdViewConfig:
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = AdFilter
    ordering_fields = ['created_at', 'price']
    search_fields = ['title', 'description']

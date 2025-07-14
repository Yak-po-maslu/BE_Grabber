from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from ads.models import Ad
from ads.serializers.ad import AdSerializer
import django_filters
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class RecommendedAdFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name='category_id')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Ad
        fields = ['category', 'min_price', 'max_price']

@method_decorator(cache_page(60 * 5), name='dispatch')  # кеш 5 хв

class RecommendedAdsAPIView(ListAPIView):
    queryset = Ad.objects.filter(is_recommended=True, status='approved').select_related('user', 'category')
    serializer_class = AdSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecommendedAdFilter

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return super().get_serializer(*args, **kwargs)
import django_filters
from django.db.models import Q
from ads.models import Ad
from ads.models import Attribute

class AdFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    category_id = django_filters.NumberFilter(field_name='category_id', lookup_expr='exact')
    subcategory_id = django_filters.NumberFilter(field_name='subcategory_id', lookup_expr='exact')  # якщо додаси поле

    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')

    class Meta:
        model = Ad
        fields = ['min_price', 'max_price', 'category', 'category_id', 'location']

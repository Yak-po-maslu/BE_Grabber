from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from ads.models import Ad
from ads.serializers.ad import AdSerializer
from ads.filters.filters import AdFilter  
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import RetrieveAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ads.models import Ad
from ads.serializers.ad import AdSerializer

@method_decorator(cache_page(60 * 5), name='dispatch')
class PopularAdsAPIView(ListAPIView):
    queryset = Ad.objects.filter(is_popular=True, status='approved').select_related('user', 'category')
    serializer_class = AdSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdFilter

    @swagger_auto_schema(
        operation_summary="Популярні товари",
        operation_description="Отримати список популярних товарів з можливістю фільтрації по категорії (назва), місту (назва) та ціні.",
        manual_parameters=[
            openapi.Parameter(
                'location', openapi.IN_QUERY,
                description="Назва міста (пошук по частині слова)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'category', openapi.IN_QUERY,
                description="Назва категорії (пошук по частині слова)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'min_price', openapi.IN_QUERY,
                description="Мінімальна ціна",
                type=openapi.TYPE_NUMBER
            ),
            openapi.Parameter(
                'max_price', openapi.IN_QUERY,
                description="Максимальна ціна",
                type=openapi.TYPE_NUMBER
            ),
        ],
        responses={200: AdSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """Swagger бачить цей метод як endpoint"""
        return super().list(request, *args, **kwargs)

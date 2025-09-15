from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ads.models import Category, Ad
from ads.serializers.attributes import AttributeSerializer

class CategoryFiltersAPIView(APIView):
    """
    GET /categories/<id>/filters/
    Повертає перелік атрибутів, базові фільтри та сортування.
    """

    @swagger_auto_schema(
        operation_description="Отримати фільтри для категорії",
        responses={
            200: openapi.Response(
                description="Фільтри категорії",
                examples={
                    "application/json": {
                        "category": {"id": 1, "name": "Електроніка"},
                        "base_filters": {
                            "price": {"min": 100, "max": 10000},
                            "location": {"type": "text"},
                            "subcategory": [
                                {"id": 11, "name": "Смартфони"},
                                {"id": 12, "name": "Ноутбуки"}
                            ]
                        },
                        "attributes": [
                            {"id": 1, "name": "Колір", "type": "select", "options": ["Чорний", "Білий"]},
                            {"id": 2, "name": "Стан", "type": "radio", "options": ["Новий", "Б/У"]}
                        ],
                        "sort": [
                            {"value": "newest", "label": "Найновіші"},
                            {"value": "price_asc", "label": "Дешевші → Дорожчі"},
                            {"value": "price_desc", "label": "Дорожчі → Дешевші"},
                            {"value": "popular", "label": "Популярні"}
                        ]
                    }
                }
            ),
            404: "Category not found"
        },
        manual_parameters=[
            openapi.Parameter(
                "id",  
                openapi.IN_PATH,
                description="ID категорії",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    def get(self, request, id: int): 
        try:
            category = Category.objects.get(pk=id)  
        except Category.DoesNotExist:
            return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        attrs = category.attributes.filter(is_filterable=True).order_by("sort_order", "id")
        attrs_data = AttributeSerializer(attrs, many=True).data

        prices = Ad.objects.filter(category=category).aggregate(
            min_price=models.Min("price"), max_price=models.Max("price")
        )

        subcats = list(category.subcategories.values("id", "name"))

        payload = {
            "category": {"id": category.id, "name": category.name},
            "base_filters": {
                "price": {"min": prices["min_price"] or 0, "max": prices["max_price"] or 0},
                "location": {"type": "text"},
                "subcategory": subcats
            },
            "attributes": attrs_data,
            "sort": [
                {"value": "newest", "label": "Найновіші"},
                {"value": "price_asc", "label": "Дешевші → Дорожчі"},
                {"value": "price_desc", "label": "Дорожчі → Дешевші"},
                {"value": "popular", "label": "Популярні"},
            ],
        }
        return Response(payload, status=status.HTTP_200_OK)

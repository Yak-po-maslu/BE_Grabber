# ads/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ads.models import Ad, Review
from ads.serializers.get_reviews_serialezer import ReviewSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Avg

class ProductReviewView(APIView):
    @swagger_auto_schema(
        operation_summary="Отримати відгуки про товар",
        responses={
            200: openapi.Response("Список відгуків та середній рейтинг"),
            404: "Product not found"
        }
    )
    def get(self, request, id):
        try:
            product = Ad.objects.get(pk=id)
        except Ad.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        reviews = Review.objects.filter(product=product)
        avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0

        serializer = ReviewSerializer(reviews, many=True)
        return Response({
            "average_rating": round(avg_rating, 2),
            "reviews": serializer.data
        })

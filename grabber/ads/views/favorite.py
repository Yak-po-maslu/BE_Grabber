from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ads.serializers.favorite_ad import FavoriteAdAddSerializer
from ads.models import Ad, FavoriteAd
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ads.serializers.favorite_ad import AdListSerializer

class FavoriteAdAddView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=FavoriteAdAddSerializer,  
        responses={
            201: openapi.Response("Added to favorites"),
            400: openapi.Response("Bad Request"),
            404: openapi.Response("Ad not found"),
        }
    )
    def post(self, request):
        serializer = FavoriteAdAddSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            try:
                ad = Ad.objects.get(pk=product_id)
                FavoriteAd.objects.get_or_create(user=request.user, ad=ad)
                return Response({"detail": "Added to favorites"}, status=status.HTTP_201_CREATED)
            except Ad.DoesNotExist:
                return Response({"detail": "Ad not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FavoriteAdListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: openapi.Response("List of favorite ads")}
    )
    def get(self, request):
        favorites = FavoriteAd.objects.filter(user=request.user).select_related('ad')
        ads = [favorite.ad for favorite in favorites]
        serializer = AdListSerializer(ads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class FavoriteAdRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'product_id',
                openapi.IN_PATH,
                description="ID оголошення для видалення з обраного",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            204: openapi.Response("Removed from favorites"),
            404: openapi.Response("Not found in favorites"),
        }
    )
    def delete(self, request, product_id):
        deleted, _ = FavoriteAd.objects.filter(user=request.user, ad_id=product_id).delete()
        if deleted:
            return Response({"detail": "Removed from favorites"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Not found in favorites"}, status=status.HTTP_404_NOT_FOUND)
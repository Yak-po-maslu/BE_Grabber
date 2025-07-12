from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ads.models import Ad, FavoriteAd

class FavoriteAdAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ad_id = request.data.get('product_id')
        try:
            ad = Ad.objects.get(pk=ad_id)
            FavoriteAd.objects.get_or_create(user=request.user, ad=ad)
            return Response({"detail": "Added to favorites"}, status=status.HTTP_201_CREATED)
        except Ad.DoesNotExist:
            return Response({"detail": "Ad not found"}, status=status.HTTP_404_NOT_FOUND)

class FavoriteAdRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, ad_id):
        deleted, _ = FavoriteAd.objects.filter(user=request.user, ad_id=ad_id).delete()
        if deleted:
            return Response({"detail": "Removed from favorites"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Not found in favorites"}, status=status.HTTP_404_NOT_FOUND)

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from ads.models import Ad
from ads.serializers.create_ad import CreateAdsSerializer
from ads.serializers.update_ad import UpdateAdSerializer


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateAdsSerializer
        elif self.action == 'partial_update':
            return UpdateAdSerializer
        return UpdateAdSerializer  # дефолт

    def partial_update(self, request, *args, **kwargs):
        if 'id' in request.data or 'status' in request.data:
            return Response(
                {"detail": "Редагування полів 'id' та 'status' заборонено."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().partial_update(request, *args, **kwargs)
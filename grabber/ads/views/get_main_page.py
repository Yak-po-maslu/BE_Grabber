from rest_framework.generics import ListAPIView
from ads.models import Ad
from ads.serializers.ad import AdSerializer
from django.db.models import Q

class MainPageAdListView(ListAPIView):
    serializer_class = AdSerializer

    def get_queryset(self):
        queryset = Ad.objects.filter(status="approved")
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        return queryset

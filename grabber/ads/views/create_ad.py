from adrf.views import APIView
from rest_framework.permissions import IsAuthenticated

class AsyncCreateAdsView(APIView):
    permission_classes = (IsAuthenticated,)
    async def post(self, request):
        pass

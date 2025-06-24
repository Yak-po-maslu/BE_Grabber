from rest_framework.views import APIView
from rest_framework.response import Response
from ads.models import FAQ
from ads.serializers.faq_serializer import FAQSerializer

class FAQListAPIView(APIView):
    def get(self, request):
        faqs = FAQ.objects.filter(is_active=True).order_by('-created_at')  # або інше сортування
        serializer = FAQSerializer(faqs, many=True)
        return Response(serializer.data)
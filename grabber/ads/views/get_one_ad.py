from asgiref.sync import sync_to_async
from adrf.views import APIView
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from drf_yasg import openapi

from ..models import Ad
from ..serializers.ad import AdSerializer
from ..serializers.create_ad import CreateAdsSerializer


class GetOneAdView(APIView):
    @swagger_auto_schema(manual_parameters= [
        openapi.Parameter(
                'ad_id', openapi.IN_PATH,
                description="ID оголошення",
                type=openapi.TYPE_INTEGER
            )
    ], responses={
        200: openapi.Response(
        schema=CreateAdsSerializer(),
        description="Get ad successfully")
    })
    async def get(self, request, ad_id):
        try:
             ad = await sync_to_async(Ad.objects.get)(id=ad_id)
        except Ad.DoesNotExist:
            raise Http404
        result_data  = await sync_to_async(lambda: AdSerializer(instance=ad).data)()

        return Response({"ad": result_data}, status=status.HTTP_200_OK)


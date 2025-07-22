from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.throttling import UserRateThrottle

from ads.models import ProductComment
from ads.serializers.product_comment_serializer import ProductCommentSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CommentThrottle(UserRateThrottle):
    rate = '1/min'


class ProductCommentView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [CommentThrottle]

    @swagger_auto_schema(
        operation_summary="Отримати коментарі до товару",
        responses={200: ProductCommentSerializer(many=True)}
    )
    def get(self, request, id):
        comments = ProductComment.objects.filter(product_id=id).order_by('-created_at')
        serializer = ProductCommentSerializer(comments, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Додати новий публічний коментар до товару",
        request_body=ProductCommentSerializer,
        responses={201: ProductCommentSerializer}
    )
    def post(self, request, id):
        data = request.data.copy()
        data['product_id'] = id
        serializer = ProductCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

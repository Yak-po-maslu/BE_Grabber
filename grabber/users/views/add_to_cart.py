from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from users.models import CartItem
from ads.models import Ad
from users.serializers.cart_add import AddToCartSerializer, RemoveFromCartSerializer

class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=AddToCartSerializer,
        responses={200: openapi.Response("Product added to cart")},
        operation_summary="Додати товар до кошика",
    )
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['productId']
            quantity = serializer.validated_data['quantity']
            product = Ad.objects.get(id=product_id)
            user = request.user

            cart_item, created = CartItem.objects.get_or_create(user=user, product=product)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()

            return Response({"message": "Product added to cart."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RemoveFromCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=RemoveFromCartSerializer,
        responses={204: openapi.Response("Product removed from cart")},
        operation_summary="Видалити товар з кошика",
    )
    def delete(self, request):
        serializer = RemoveFromCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['productId']
            user = request.user

            try:
                cart_item = CartItem.objects.get(user=user, product_id=product_id)
                cart_item.delete()
                return Response({"message": "Product removed from cart."})
            except CartItem.DoesNotExist:
                return Response({"error": "Product not in cart."}, status=404)
        return Response(serializer.errors, status=400)

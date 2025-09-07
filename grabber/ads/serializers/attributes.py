from drf_yasg import openapi
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from ads.models import Attribute, AttributeOption

class AttributeOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeOption
        fields = ("value", "label", "sort_order")

class AttributeSerializer(serializers.ModelSerializer):
    options = AttributeOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Attribute
        fields = (
            "id", "name", "slug", "type", "unit",
            "is_filterable", "sort_order", "options"
        )
        
    @swagger_serializer_method(serializer_or_field=openapi.Schema(
        type=openapi.TYPE_ARRAY,
        items=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                "name": openapi.Schema(type=openapi.TYPE_STRING, example="Колір"),
                "slug": openapi.Schema(type=openapi.TYPE_STRING, example="color"),
                "type": openapi.Schema(type=openapi.TYPE_STRING, example="select"),
                "unit": openapi.Schema(type=openapi.TYPE_STRING, example=None),
                "is_filterable": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                "sort_order": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                "options": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "value": openapi.Schema(type=openapi.TYPE_STRING, example="black"),
                            "label": openapi.Schema(type=openapi.TYPE_STRING, example="Чорний"),
                            "sort_order": openapi.Schema(type=openapi.TYPE_INTEGER, example=1)
                        }
                    )
                )
            }
        )
    ))
    def get_swagger_example(self):
        return AttributeSerializer(
            Attribute.objects.first()
        ).data

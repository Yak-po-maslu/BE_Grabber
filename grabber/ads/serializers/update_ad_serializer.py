from rest_framework import serializers
from ads.models import Ad
import decimal
from ctypes import cast
from decimal import Decimal
from unicodedata import category

from asgiref.sync import async_to_sync
from rest_framework import serializers

from services.upload_one_image import UploadOneImage
from .category import CategorySerializer
from ..models import Ad, Category


class UpdateAdSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=255,
        help_text="Название объявления. До 255 символов.",
        required=False,
    )
    description = serializers.CharField(
        help_text="Описание объявления. До 1000 символов.",
        required=False
    )
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Цена объявления. Десятичное число с двумя знаками после запятой.",
        required=False,
    )
    status = serializers.ChoiceField(
        choices=['draft', 'pending'],
        help_text="Статус объявления: 'draft' или 'pending'.",
        required=False,
    )

    class Meta:
        model = Ad
        fields = ['id', 'description', 'price',
                  'title', 'status']

        # extra_kwargs = {'images': {'read_only': True}}

    def validate_description(self, value):
        if value == '':
            raise serializers.ValidationError('Description cannot be empty')
        if len(value) > 1000:
            raise serializers.ValidationError('Description must be less than 1000 characters')
        return value

    def validate_price(self, value):
        if value in ['', None]:
            raise serializers.ValidationError('Price cannot be empty')
        try:
            price = Decimal(value)
            if price <= 0:
                raise serializers.ValidationError('Price must be greater than 0')
        except decimal.InvalidOperation:
            raise serializers.ValidationError('Price must be decimal number')
        return price

    def validate_title(self, value):
        if value == '':
            raise serializers.ValidationError('Title cannot be empty')
        if len(value) > 255:
            raise serializers.ValidationError('Title must be less than 255 characters')
        return value

    def validate_status(self, value):
        if not value:
            raise serializers.ValidationError('Status cannot be empty')

        if value not in ['draft', 'pending', ]:
            raise serializers.ValidationError('State must be draft/pending')
        return value

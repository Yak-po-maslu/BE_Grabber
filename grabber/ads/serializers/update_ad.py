from rest_framework import serializers
from ads.models import Ad

class UpdateAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'price', 'category', 'images']  # доступні до редагування поля
        read_only_fields = ['id', 'status', 'user', 'created_at', 'moderated_by', 'moderated_at']

    def update(self, instance, validated_data):
        # Страховка, навіть якщо хтось спробує змінити заборонені поля
        validated_data.pop('id', None)
        validated_data.pop('status', None)
        return super().update(instance, validated_data)
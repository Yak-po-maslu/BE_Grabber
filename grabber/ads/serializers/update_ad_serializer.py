from rest_framework import serializers
from ads.models import Ad

class UpdateAdSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Ad
        fields = ['title', 'description', 'price', 'category']
        read_only_fields = ['id', 'status', 'user', 'created_at', 'moderated_by', 'moderated_at']

    def update(self, instance, validated_data):
        for field in self.Meta.read_only_fields:
            validated_data.pop(field, None)
        return super().update(instance, validated_data)

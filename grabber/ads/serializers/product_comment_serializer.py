from rest_framework import serializers
from ads.models import ProductComment

class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = '__all__'

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Рейтинг має бути від 1 до 5.")
        return value

    def validate_comment_text(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Коментар має містити щонайменше 3 символи.")
        if len(value) > 100:
            raise serializers.ValidationError("Коментар не може перевищувати 100 символів.")
        return value

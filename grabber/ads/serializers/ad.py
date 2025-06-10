from rest_framework import serializers
from ..models import Ad


class AdSerializer(serializers.ModelSerializer):
    location = serializers.CharField(source='user.location')
    first_name = serializers.CharField(source='user.first_name')
    phone_number = serializers.SerializerMethodField()

    category_name = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.IntegerField(source='category.id', read_only=True)


    #
    #phone_number = models.CharField(max_length=255, blank=False, default='+38033333333')
    #show_phone = models.BooleanField(default=False)
    #
    class Meta:
        model = Ad
        fields = ['id', 'description', 'price', 'user_id',
                  'title', 'status', 'category_name', 'category_id', 'images', 'created_at','phone_number',
                  'first_name', 'location']



    def get_phone_number(self, obj):
        return obj.user.phone_number if obj.user.show_phone else 'user is not show phone'


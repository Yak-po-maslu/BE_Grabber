from rest_framework import serializers
from ..models import Ad


class AdSerializer(serializers.ModelSerializer):
    location = serializers.CharField(required=False, allow_blank=True)
    contact_name = serializers.CharField(source='user.first_name')
    phone = serializers.SerializerMethodField()

    category = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.IntegerField(source='category.id', read_only=True)
    view_count = serializers.IntegerField(source='views', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    is_favorite = serializers.SerializerMethodField()

    
    # 👇 Додано поле images як список URL
    images = serializers.ListField(
        child=serializers.URLField(),
        required=False,
        allow_empty=True
    ) 

    class Meta:
        model = Ad
        fields = ['id', 'description', 'price', 'user_id',
                  'title', 'status', 'category', 'category_id', 'images', 'created_at','phone',
                  'contact_name', 'location', 'view_count', 'email','is_favorite']



    def get_phone(self, obj):
        return obj.user.phone_number if obj.user.show_phone else 'user is not show phone'


    def get_is_favorite(self, obj):

        request = self.context.get('request')
        user = request.user if request else None
        if user and user.is_authenticated:
            return obj.favorited_by.filter(user=user).exists()
        return False
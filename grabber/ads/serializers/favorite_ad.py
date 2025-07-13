from rest_framework import serializers

class FavoriteAdAddSerializer(serializers.Serializer):
    """
    Serializer for adding an Ad to user's favorites.
    """
    product_id = serializers.IntegerField()

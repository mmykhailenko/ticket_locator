from rest_framework import serializers
from hello_world.models import SearchHistory, User


class SearchHistorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = SearchHistory
        fields = ('id', 'departure_city', 'arrival_city', 'departure_date', 'arrival_date', 'user')


class UserSerializer(serializers.ModelSerializer):
    search_history = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'search_history']
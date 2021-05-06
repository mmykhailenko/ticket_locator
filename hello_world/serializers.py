from rest_framework import serializers
from hello_world.models import User, SearchHistory


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'is_staff', 'is_active']


class SearchHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SearchHistory
        fields = ['id', 'departure_city', 'arrival_city', 'departure_date', 'arrival_date', 'user']

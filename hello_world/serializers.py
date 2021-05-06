from rest_framework import serializers
from hello_world.models import SearchHistory


class SearchHistorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = SearchHistory
        fields = ('id', 'departure_city', 'arrival_city', 'departure_date', 'arrival_date', 'user')
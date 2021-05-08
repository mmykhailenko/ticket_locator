from rest_framework import serializers
from .models import User, SearchHistory


class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'email']


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'email', 'is_active']


class SearchHistorySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = SearchHistory
		fields = ['id', 'user', 'user_id', 'departure_city', 'arrival_city', 'departure_date', 'arrival_date']


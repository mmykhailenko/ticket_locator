from rest_framework import serializers

from .models import User, SearchHistory


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
        )


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "is_active")


class SearchHistorySerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="email", read_only=True)

    class Meta:
        model = SearchHistory
        fields = (
            "id",
            "user",
            "user_id",
            "departure_city",
            "arrival_city",
            "departure_date",
            "arrival_date",
        )


class FlightSearchSerializer(serializers.Serializer):
    departure_airport = serializers.CharField(max_length=3, help_text="IATA format")
    arrival_airport = serializers.CharField(max_length=3, help_text="IATA format")
    departure_date = serializers.DateField()
    direct_flight = serializers.BooleanField(required=True)

    def create(self, validated_data):
        return validated_data

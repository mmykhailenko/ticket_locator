from rest_framework import serializers

from .models import User, SearchHistory
from ticket_locator.services.transavia_service import TransaviaService
from ticket_locator.services.singapor_air_service import SingaporeService


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email',)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'is_active')


class SearchHistorySerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', read_only=True)

    class Meta:
        model = SearchHistory
        fields = ('id', 'user', 'user_id', 'departure_city', 'arrival_city', 'departure_date', 'arrival_date',)


class CreatePostForMakingSearchDaySerializer(serializers.Serializer):
    CHOICES = [("Economy", "Economy"),
               ("Bisness", "Bisness")]
    departure_airport = serializers.CharField(max_length=150, required=True,
                                              help_text = "Departure airport name in IATA format")
    arrival_airport = serializers.CharField(max_length=150, required=True,
                                            help_text = "Arrival airport name in IATA format")
    departure_date = serializers.DateField(required=True)
    cabin_class = serializers.ChoiceField(choices=CHOICES)
    adult_count = serializers.IntegerField(min_value=1, required=True, help_text="Mandatory, min 1 passenger",initial= 1)
    child_count = serializers.IntegerField(min_value=0, default=0, initial= 0)
    infant_count = serializers.IntegerField(min_value=0, default=0,initial = 0)

    def create(self, validated_data):
        return validated_data
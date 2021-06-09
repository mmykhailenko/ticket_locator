from rest_framework import serializers, fields

from .models import User, SearchHistory


class UsersListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email',)


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'is_active')


class SearchHistorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = SearchHistory
        fields = ('id', 'user', 'departure_city', 'arrival_city', 'departure_date')


class FlightSearchSerializer(serializers.Serializer):
    departure_airport = serializers.CharField(max_length=3, help_text="IATA format")
    arrival_airport = serializers.CharField(max_length=3, help_text="IATA format")
    departure_date = serializers.DateField()
    direct_flight = serializers.BooleanField(required=True)

    def create(self, validated_data):
        return validated_data


class RegisterUsersSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        user = User(
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return user

    def create(self, validated_data):
        return validated_data
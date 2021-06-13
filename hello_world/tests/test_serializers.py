from django.test import TestCase

from hello_world.models import User, SearchHistory
from hello_world.serializers import (
    UsersListSerializer,
    UserDetailSerializer,
    SearchHistorySerializer,
    FlightSearchSerializer,
)


class TestUserSerializers(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="test1@gmail.com", password="123456"
        )
        self.user2 = User.objects.create_superuser(
            email="test2@gmail.com", password="55555"
        )

    def test_users_list_serializer(self):
        serializes_data = UsersListSerializer([self.user1, self.user2], many=True)
        compare_data = [
            {"id": self.user1.id, "email": "test1@gmail.com"},
            {"id": self.user2.id, "email": "test2@gmail.com"},
        ]
        self.assertEqual(serializes_data.data, compare_data)

    def test_user_detail_serializer(self):
        serializes_data = UserDetailSerializer(self.user1)
        compares_data = {
            "id": self.user1.id,
            "email": "test1@gmail.com",
            "is_active": True,
        }
        self.assertEqual(serializes_data.data, compares_data)


class TestSearchHistorySerializer(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="test1@gmail.com", password="123456"
        )
        self.user2 = User.objects.create_user(
            email="test2@gmail.com", password="456123"
        )
        self.history_test_unit1 = SearchHistory.objects.create(
            departure_city="AMS",
            arrival_city="IEV",
            departure_date="2021-03-12T00:00:00Z",
            arrival_date="2021-04-12T00:00:00Z",
            user=self.user1,
        )
        self.history_test_unit2 = SearchHistory.objects.create(
            departure_city="AMS",
            arrival_city="IEV",
            departure_date="2021-03-15T00:00:00Z",
            arrival_date="2021-04-15T00:00:00Z",
            user=self.user2,
        )

    def test_search_history_serializer(self):
        serializes_data = SearchHistorySerializer(self.history_test_unit1)
        compares_data = {
            "id": self.history_test_unit1.id,
            "user": "test1@gmail.com",
            "user_id": self.user1.id,
            "departure_city": "AMS",
            "arrival_city": "IEV",
            "departure_date": "2021-03-12T00:00:00Z",
            "arrival_date": "2021-04-12T00:00:00Z",
        }
        self.assertEqual(serializes_data.data, compares_data)


class TestFlightSearchSerializer(TestCase):
    def setUp(self):
        self.test_data2 = {
            "departure_airport": "IBZ",
            "arrival_airport": "AMS",
            "departure_date": "2021-06-06",
            "direct_flight": True,
        }

    def test_flight_search_serializer(self):
        serializes_data = FlightSearchSerializer(self.test_data2)
        print(serializes_data.data)
        compares_data = {
            "departure_airport": "IBZ",
            "arrival_airport": "AMS",
            "departure_date": "2021-06-06",
            "direct_flight": True,
        }
        self.assertEqual(serializes_data.data, compares_data)

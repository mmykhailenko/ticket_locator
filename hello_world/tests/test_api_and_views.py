import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from hello_world.models import User, SearchHistory
from hello_world.serializers import UsersListSerializer, UserDetailSerializer, SearchHistorySerializer
from unittest.mock import MagicMock
from hello_world.views import FlightSearchView
from django.test import Client


class UserViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email="test1@gmail.com", password="123456")
        self.user2 = User.objects.create_user(email="test2@gmail.com", password="456123")
        self.user3 = User.objects.create_superuser(email="test3@gmail.com", password="55555")

    def test_get_all(self):
        url = reverse("users")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(UsersListSerializer([self.user1, self.user2, self.user3], many=True).data, response.data)
        self.assertEqual(self.user3.is_superuser, True)
        self.assertEqual(self.user2.is_superuser and self.user1.is_superuser, False)

    def test_get_pk(self):
        url = reverse("user_detail", args="1")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(UserDetailSerializer(self.user1).data, response.data)


class SearchHistoryViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email="test1@gmail.com", password="123456")
        self.user2 = User.objects.create_user(email="test2@gmail.com", password="456123")
        self.history_test_unit1 = SearchHistory.objects.create(
            departure_city="AMS",
            arrival_city="IEV",
            departure_date="2021-03-12T00:00:00Z",
            arrival_date="2021-04-12T00:00:00Z",
            user=self.user1
        )
        self.history_test_unit2 = SearchHistory.objects.create(
            departure_city="AMS",
            arrival_city="IEV",
            departure_date="2021-03-15T00:00:00Z",
            arrival_date="2021-04-15T00:00:00Z",
            user=self.user2
        )

    def test_get_search_history_all(self):
        url = reverse("history_search")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(SearchHistorySerializer([self.history_test_unit1, self.history_test_unit2], many=True).data,
                         response.data)

    def test_get_search_history_pk(self):
        url = reverse("history_detail", args="1")
        response = self.client.get(url)
        response_dict = (json.loads(json.dumps(response.data)))[0]
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual((SearchHistorySerializer(self.history_test_unit1)).data, response_dict)


class FlightSearchViewTest(APITestCase):
    test_response_data = [[{'Airline': 'TK', 'FlightNumber': '1956', 'DepartureAirport': 'AMS',
                            'ArrivalAirport': 'IST', 'DepartureTime': '2021-06-06T23:15:00',
                            'ArrivalTime': '2021-06-07T03:35:00'},
                           {'Airline': 'TK', 'FlightNumber': '1857', 'DepartureAirport': 'IST',
                            'ArrivalAirport': 'MAD', 'DepartureTime': '2021-06-07T07:10:00',
                            'ArrivalTime': '2021-06-07T10:30:00'},
                           {'Airline': 'TK', 'FlightNumber': '9392', 'DepartureAirport': 'MAD',
                            'ArrivalAirport': 'IBZ', 'DepartureTime': '2021-06-08T15:05:00',
                            'ArrivalTime': '2021-06-08T16:20:00'}], [
                              {'Airline': 'HV', 'FlightNumber': '5675', 'DepartureAirport': 'AMS',
                               'ArrivalAirport': 'IBZ', 'DepartureTime': '2021-06-06T05:50:00',
                               'ArrivalTime': '2021-06-06T08:25:00'},
                              {'Airline': 'HV', 'FlightNumber': '5671', 'DepartureAirport': 'AMS',
                               'ArrivalAirport': 'IBZ', 'DepartureTime': '2021-06-06T12:00:00',
                               'ArrivalTime': '2021-06-06T14:35:00'}]]

    def setUp(self):
        FlightSearchView.get_air_info = MagicMock(return_value=self.test_response_data)
        self.factory = APIRequestFactory()
        self.view = FlightSearchView.as_view()
        self.test_data1 = {"departure_airport": 'IBZ', "arrival_airport": 'AMS', "departure_date": "2021-06-06"}
        self.test_data2 = {"departure_airport": 'IBZ', "arrival_airport": 'AMS', "departure_date": "2021-06-06",
                           "direct_flight": True}

    def test_post_input_data_ok(self):
        url = reverse("search")
        request = self.factory.post(url, self.test_data1)
        response = self.view(request)
        self.assertEqual(self.test_response_data, response.data)

    def test_post_input_data_broken(self):
        url = reverse("search")
        data = {"departure_airport": 'IBZ', "arrival_airport": 'AMS'}
        response = self.client.post(url, data)
        self.assertEqual({"Error": "Please fill all fields."}, response.data)

    def test_start_get_air_info_not_direct_flight(self):
        unit = FlightSearchView()
        unit.flight_info = self.test_response_data
        result = unit.start_get_air_info(air_company="Test1", request_data=self.test_data1)
        self.assertEqual(result, unit.flight_info)

    def test_start_get_air_info_with_direct_flight(self):
        unit = FlightSearchView()
        unit.flight_info = self.test_response_data
        result = unit.start_get_air_info(air_company="Test1", request_data=self.test_data2)
        self.assertEqual(result, [])


class TestSearchAirRoute(APITestCase):

    def setUp(self):
        self.client = Client()
        self.email = "test1@gmail.com"
        self.password = "123456"
        self.user = User.objects.create_user(self.email, self.password)
        self.request_data = {'departure_airport': 'Amsterdam Airport Schiphol (AMS), Amsterdam, NL',
                             'arrival_airport': 'Ibiza Airport (IBZ), Ibiza, ES', 'departure_date': '2021-06-06'}
        self.client.login(email=self.email, password=self.password)

    def test_post_user_anonymous(self):
        url = reverse("index")
        self.client.logout()
        self.client.post(url, data=self.request_data)
        self.assertFalse(SearchHistory.objects.all())

    def test_post_user_authenticated(self):
        url = reverse("index")
        self.client.post(url, data=self.request_data)
        self.assertTrue(SearchHistory.objects.get(user_id=self.user.id))
        self.assertEqual(SearchHistory.objects.get(user_id=self.user.id).departure_city, "AMS")

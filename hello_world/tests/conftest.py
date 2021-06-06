import pytest

import hello_world.views
from hello_world.models import User, SearchHistory


@pytest.fixture
def user_data():
    return {"email": "test1@test.test", "password1": "test12341234", "password2": "test12341234"}


@pytest.fixture
def wrong_user_data():
    return {"email": "test1@test.test", "password1": "test", "password2": "test"}


@pytest.fixture
def users():
    return "test1@test.test", "test2@test.test", "test3@test.test"


@pytest.fixture
def create_users(users):
    model = User
    response = []
    for user_id, user_email in enumerate(users, 1):
        model.objects.create(email=user_email)
        result = {"id": user_id, "email": user_email}
        response.append(result)
    return response


@pytest.fixture
def histories():
    return [
        {
            "departure_airport": "AKS",
            "arrival_airport": "BCS",
            "departure_date": "2021-06-20T00:00:00Z",
            "arrival_date": "2022-12-12T00:00:00Z"
        },
        {
            "departure_airport": "BCN",
            "arrival_airport": "ODS",
            "departure_date": "2021-06-12T00:00:00Z",
            "arrival_date": "2022-07-22T00:00:00Z"
        },
    ]


@pytest.fixture
def create_history(create_users, histories):
    search_model = SearchHistory
    users = User.objects.all()
    history_id = 1
    response = []
    for user in users:
        for history in histories:
            result = {
                "id": history_id,
                "user": user.email,
                "user_id": user.pk,
                "departure_city": history["departure_airport"],
                "arrival_city": history["arrival_airport"],
                "departure_date": history["departure_date"],
                "arrival_date": history["arrival_date"]
            }
            search_model.objects.create(user=user,
                                        departure_city=history["departure_airport"],
                                        arrival_city=history["arrival_airport"],
                                        departure_date=history["departure_date"],
                                        arrival_date=history["arrival_date"])
            response.append(result)
            history_id += 1

    return response


@pytest.fixture
def flight_search_expected_response():
    return [[{'Airline': 'TK', 'FlightNumber': '1956', 'DepartureAirport': 'AMS',
              'ArrivalAirport': 'IST', 'DepartureTime': '2021-06-06T23:15:00',
              'ArrivalTime': '2021-06-07T03:35:00'}]]


@pytest.fixture
def mock_flight_search(mocker, flight_search_expected_response):
    mocker.patch("hello_world.views.FlightSearchView.get_air_info", return_value=flight_search_expected_response)

from django import urls
import pytest
from hello_world.models import User


class TestUserView:
    @pytest.mark.django_db
    def test_get_all_users_empty_db(self, client):
        url = urls.reverse("api_users")
        response = client.get(url)
        assert response.status_code == 200
        assert not response.data

    @pytest.mark.django_db
    def test_get_user_by_id_empty_db(self, client):
        url = urls.reverse("api_user", kwargs={"pk": 1})
        response = client.get(url)
        assert response.status_code == 200
        assert response.data == {
            "id": 1,
            "email": "User with id (1) not found."
        }

    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def test_get_all_users_with_users(self, client, create_users):
        url = urls.reverse("api_users")
        response = client.get(url)
        expected_response = create_users
        assert response.status_code == 200
        assert response.data == expected_response

    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def test_get_user_by_id(self, client, create_users):
        users = create_users
        for user in users:
            user["is_active"] = True
            url = urls.reverse("api_user", kwargs={"pk": user["id"]})
            response = client.get(url)
            assert response.status_code == 200
            assert response.data == user


class TestSearchHistoryView:
    @pytest.mark.django_db
    def test_get_all_history_empty_db(self, client):
        url = urls.reverse("api_history")
        response = client.get(url)
        assert response.status_code == 200
        assert not response.data

    @pytest.mark.django_db
    def test_get_history_by_user_id_empty_db(self, client):
        url = urls.reverse("api_user_history", kwargs={"user": 1})
        response = client.get(url)
        assert response.status_code == 200
        assert response.data == []

    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def test_get_all_history_with_history(self, client, create_history):
        url = urls.reverse("api_history")
        response = client.get(url)
        expected_response = create_history
        assert response.status_code == 200
        assert response.data == expected_response

    @pytest.mark.django_db(transaction=True, reset_sequences=True)
    def test_get_history_by_user_id(self,
                                    client,
                                    create_users,
                                    create_history
                                    ):
        users = create_users
        history = create_history
        for history_id, user in enumerate(users, 0):
            expected_response = [
                history[history_id * 2],
                history[history_id * 2 + 1]
            ]
            url = urls.reverse("api_user_history", kwargs={"user": user["id"]})
            response = client.get(url)
            assert response.status_code == 200
            assert response.data == expected_response


class TestFlightSearchView:
    @pytest.mark.parametrize(
        "params",
        [
            {
                "departure_airport": "",
                "arrival_airport": "",
                "departure_date": ""
            },
            {
                "departure_airport": "BCN",
                "arrival_airport": "",
                "departure_date": ""
            },
            {
                "departure_airport": "BCN",
                "arrival_airport": "AMS",
                "departure_date": "",
            },
        ],
    )
    def test_post_incorrect_data(self, client, params):
        url = urls.reverse("api_search")
        response = client.post(url, data=params)
        assert response.data == {"Error": "Please fill all fields."}

    @pytest.mark.parametrize(
        "params",
        [
            {
                "departure_airport": "AMS",
                "arrival_airport": "IBZ",
                "departure_date": "2021-06-06",
            }
        ],
    )
    def test_post_without_direct_flight(
                                        self,
                                        client,
                                        params,
                                        mock_flight_search,
                                        flight_search_expected_response
                                        ):
        url = urls.reverse("api_search")
        response = client.post(url, data=params)
        assert response.data == flight_search_expected_response


class TestSearchAirRoute:
    def test_get(self, client):
        url = urls.reverse("index")
        response = client.get(url)
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "params",
        [
            {
                "departure_airport": "",
                "arrival_airport": "",
                "departure_date": ""
            },
            {
                "departure_airport": "BCN",
                "arrival_airport": "OHL",
                "departure_date": "12456789",
            },
        ],
    )
    def test_post_incorrect_data(self, client, params):
        url = urls.reverse("index")
        response = client.post(url, data=params)
        assert response.status_code == 302

    @pytest.mark.parametrize(
        "params",
        [
            {
                "departure_airport": "Afutara Aerodrome (AFT), Bila, SB",
                "arrival_airport": "Brawley Municipal Airport (BWC), "
                                   "Brawley, US",
                "departure_date": "2021-12-12",
            },
            {
                "departure_airport": "Amsterdam Airport Schiphol (AMS), "
                                     "Amsterdam, NL",
                "arrival_airport": "Odessa International Airport (ODS), "
                                   "Odessa, UA",
                "departure_date": "2021-03-06",
            },
        ],
    )
    def test_post_correct_data(self, client, params, mock_flight_search):
        url = urls.reverse("index")
        response = client.post(url, data=params)
        assert response.status_code == 200


class TestLogout:
    def test_get(self, client):
        url = urls.reverse("logout")
        response = client.get(url)
        assert response.status_code == 302


class TestRegistrationView:
    def test_get_request(self, client):
        url = urls.reverse("registration")
        response = client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_valid_registration(self, client, user_data):
        user_model = User
        assert user_model.objects.count() == 0
        url = urls.reverse("registration")
        response = client.post(url, user_data)
        assert user_model.objects.count() == 1
        assert response.status_code == 302

    @pytest.mark.django_db
    def test_not_valid_data_registration(self, client, wrong_user_data):
        user_model = User
        assert user_model.objects.count() == 0
        url = urls.reverse("registration")
        response = client.post(url, wrong_user_data)
        assert user_model.objects.count() == 0
        assert response.status_code == 200


class TestLogin:
    def test_get(self, client):
        url = urls.reverse("login")
        response = client.get(url)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_post_no_such_user(self, client, user_data):
        url = urls.reverse("login")
        user = {
            "email": user_data["email"],
            "password": user_data["password1"]
        }
        response = client.post(url, data=user)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_post_correct_user(self, client, user_data):
        user_model = User
        url = urls.reverse("registration")
        response = client.post(url, user_data)
        assert user_model.objects.count() == 1
        url = urls.reverse("login")
        user = {
            "email": user_data["email"],
            "password": user_data["password1"]
        }
        response = client.post(url, data=user)
        assert response.status_code == 302

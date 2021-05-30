import json
import requests
from ticket_locator.services.constants import SUCCESS
from ticket_locator import settings
from ticket_locator.services.base_service import AirCompanyService


class SingaporeAirService(AirCompanyService):
    _BASE_URL = (
        "https://apigw.singaporeair.com/api/v1/commercial/flightavailability/get"
    )
    _API_KEY = settings.SINGAPOREAIR_API_KEY

    _headers = {
        "Content-Type": "application/json",
        "apikey": _API_KEY,
    }

    _params = {
        "clientUUID": "SQ-API-Booking-Aggregator",
        "request": {
            "itineraryDetails": [
                {
                    "originAirportCode": "",
                    "destinationAirportCode": "",
                    "departureDate": "",
                }
            ],
            "cabinClass": "Y",
            "adultCount": 1,
        },
    }

    def _param_prepare(self, **kwargs):
        date = f'{kwargs["date"][:4]}-{kwargs["date"][4:6]}-{kwargs["date"][6:8]}'
        params = self._params["request"]["itineraryDetails"][0]
        params["originAirportCode"] = kwargs["departure_airport"]
        params["destinationAirportCode"] = kwargs["arrival_airport"]
        params["departureDate"] = date

    def get_flight_info_by_date(self, departure_airport, arrival_airport, date):

        response_service = []

        self._param_prepare(
            departure_airport=departure_airport,
            arrival_airport=arrival_airport,
            date=date,
        )

        response = requests.post(
            self._BASE_URL, data=json.dumps(self._params), headers=self._headers
        )

        if response.status_code == 200:
            response_json = response.json()

            if response_json["status"] == SUCCESS and response_json["response"].get(
                "flights"
            ):
                segments = response_json["response"]["flights"][0]["segments"]
                for segment in segments:
                    routes = segment["legs"]
                    routes_list = []
                    for flight in routes:
                        response_map = {
                            "Airline": flight["marketingAirline"]["code"],
                            "FlightNumber": flight["flightNumber"],
                            "DepartureAirport": flight["originAirportCode"],
                            "ArrivalAirport": flight["destinationAirportCode"],
                            "DepartureTime": "T".join(
                                flight["departureDateTime"].split(" ")
                            ),
                            "ArrivalTime": "T".join(
                                flight["arrivalDateTime"].split(" ")
                            ),
                        }
                        routes_list.append(response_map)

                    response_service.append(routes_list)

                return response_service

        return []

    def get_flight_info_by_period(
        self, departure_city, arrival_city, start_date, end_date
    ):
        pass

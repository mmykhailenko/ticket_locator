import json
import logging
from ticket_locator import settings
from ticket_locator.services.base_service import AirCompanyService
from ticket_locator.services.response_service import ServiceResponse
import requests

logger = logging.getLogger(__name__)

class SingaporeService(AirCompanyService):
    BASE_URL = "https://apigw.singaporeair.com/api"
    API_KEY = settings.SINGAPORE_API_KEY
    MAPPING_REQUEST_BODY = {
        "clientUUID": "SQ-API-Booking-Aggregator",
        "request": {
            "itineraryDetails": [
                {
                    "originAirportCode": "departure_airport",
                    "destinationAirportCode": "arrival_airport",
                    "departureDate": "departure_date",
                }
            ],
            "cabinClass": "cabin_class",
            "adultCount": "adult_count",
            "childCount": "child_count",
            "infantCount": "infant_count",
            "flexibleDates": False,
            "daterange": 0,
            "locale": "en_UK",
            "country": "SG"

        }
    }
    HEADERS = {"Content-Type": "application/json",
               "apikey": API_KEY}

    def _create_request_body(self,data):
        self.MAPPING_REQUEST_BODY["request"]["itineraryDetails"][0]["originAirportCode"] = data[0]
        self.MAPPING_REQUEST_BODY["request"]["itineraryDetails"][0]["destinationAirportCode"] = data[1]
        self.MAPPING_REQUEST_BODY["request"]["itineraryDetails"][0]["departureDate"] = data[2]
        self.MAPPING_REQUEST_BODY["request"]["cabinClass"] = data[3]
        self.MAPPING_REQUEST_BODY["request"]["adultCount"] = data[4]
        self.MAPPING_REQUEST_BODY["request"]["childCount"] = data[5]
        self.MAPPING_REQUEST_BODY["request"]["infantCount"] = data[6]
        return self.MAPPING_REQUEST_BODY

    def get_flight_info_by_date(self, departure_airport, arrival_airport, departure_date, cabin_class, adult_count,
                                child_count, infant_count):
        data = (departure_airport, arrival_airport, departure_date, cabin_class, adult_count,child_count, infant_count)
        request_body = self._create_request_body(data)
        url = self.BASE_URL + "/v1/commercial/flightavailability/get"
        response = requests.post(url=url, json=request_body, headers=self.HEADERS)
        if response.status_code == 200:
            try:
                response_dict = json.loads(response.text)
            except json.decoder.JSONDecodeError:
                logger.exception(msg = "Error serializing the response from the api of the singapore airline")
                return False
            if response_dict["status"] == "SUCCESS":
                create_response = ServiceResponse(response_dict["response"], departure_airport, arrival_airport,
                                                  cabin_class, adult_count, child_count, infant_count)
                return create_response.response_singapore_airline_by_date()
        return False


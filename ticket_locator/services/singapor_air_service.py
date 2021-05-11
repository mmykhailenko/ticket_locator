import json

from ticket_locator import settings
from ticket_locator.services.base_service import AirCompanyService
from ticket_locator.services.response_service import ServiseRespons
import requests


class SingaporeService(AirCompanyService):
    BASE_URL = "https://apigw.singaporeair.com/api"
    API_KEY = settings.SINGAPURE_API_KEY
    MAPPING_REQUEST_BODY = {
        "clientUUID": "SQ-API-Booking-Aggregator",
        "request": {
            "itineraryDetails": [
                {
                    "originAirportCode": "departure_airport",
                    "destinationAirportCode": "arrival_airport",
                    "departureDate": "departure_date",
                    "returnDate": "return_date",
                }
            ],
            "cabinClass": "cabin_class",
            "adultCount": "adult_count",
            "childCount": "child_count",
            "infantCount": "infant_count",
            "flexibleDates": "flexible_dates",
            "daterange": "date_range",
            "locale": "locale",
            "country": "country"

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
        self.MAPPING_REQUEST_BODY["request"]["flexibleDates"] = data[7]
        self.MAPPING_REQUEST_BODY["request"]["daterange"] = data[8]
        self.MAPPING_REQUEST_BODY["request"]["locale"] = data[9]
        self.MAPPING_REQUEST_BODY["request"]["country"] = data[10]
        if data[11]:
            self.MAPPING_REQUEST_BODY["request"]["itineraryDetails"][0]["returnDate"] = data[11]
        else:
            try:
                self.MAPPING_REQUEST_BODY["request"]["itineraryDetails"][0].pop("returnDate")
            except KeyError:
                pass
        return self.MAPPING_REQUEST_BODY

    def get_flight_info_by_date(self, departure_airport, arrival_airport, departure_date, cabin_class, adult_count,
                                child_count, infant_count, flexible_dates=False, date_range=0,
                                locale="en_UK",country="SG",return_date=False):
        data = (departure_airport, arrival_airport, departure_date, cabin_class, adult_count,child_count, infant_count,
                flexible_dates, date_range,locale,country,return_date)
        request_body = self._create_request_body(data)
        url = self.BASE_URL + "/v1/commercial/flightavailability/get"
        response = requests.post(url=url, json=request_body, headers=self.HEADERS)
        response_dict = json.loads(response.text)
        if response.status_code ==200 and response_dict["status"]=="SUCCESS":
            create_response = ServiseRespons(response_dict["response"],departure_airport,arrival_airport,adult_count,cabin_class,
                                            child_count,infant_count)
            return create_response.response_singapore_airline_by_date()
        return False


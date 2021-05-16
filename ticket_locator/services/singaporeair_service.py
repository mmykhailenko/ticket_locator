from ticket_locator.services.base_service import AirCompanyService
import requests
from ticket_locator.services.service_response import ServiceResponse
from ticket_locator import env


class SingaporeairService(AirCompanyService):
    BASE_URL = 'https://apigw.singaporeair.com/api/v1/commercial/flightavailability/get'
    API_KEY = {
        'apikey': env('API_KEY_SINGAPOREAIR'),
    }
    PARAMS = {
        "clientUUID":"SQ-API-Booking-Aggregator",
        "request":{
            "itineraryDetails":[
                {
                    "originAirportCode":None,
                    "destinationAirportCode":None,
                    "departureDate":None
                 }
            ],
            "cabinClass":"Y",
            "adultCount":1,
            "childCount":1,
            "infantCount":1
        }
    }
    RESPONSE_MAP = {
        'departure_city': None,
        'arrival_city': None,
        'date': None,
        'price': None
    }

    def _create_params(self, departure_airport, arrival_airport, date):
        self.PARAMS['request']['itineraryDetails'][0]['originAirportCode'] = departure_airport
        self.PARAMS['request']['itineraryDetails'][0]['destinationAirportCode'] = arrival_airport
        self.PARAMS['request']['itineraryDetails'][0]['departureDate'] = date

    def _create_response_map(self, resp_json, departure_airport, arrival_airport, date):
        self.RESPONSE_MAP['departure_city'] = departure_airport
        self.RESPONSE_MAP['arrival_city'] = arrival_airport
        self.RESPONSE_MAP['date'] = date
        self.RESPONSE_MAP['price'] = resp_json['response']['recommendations'][0]['fareSummary']['fareDetailsPerAdult']['totalAmount']

    def get_flight_info_by_date(self, departure_airport='SIN', arrival_airport='LHR', date='2021-05-16'):
        self._create_params(departure_airport, arrival_airport, date)
        try:
            resp = requests.post(url=self.BASE_URL, headers=self.API_KEY, json=self.PARAMS)
            resp_json = resp.json()
            if resp_json['code'] == '200':
                self._create_response_map(resp_json, departure_airport, arrival_airport, date)
                return ServiceResponse(response=self.RESPONSE_MAP)
            else:
                return ServiceResponse(response=resp_json['message'])
        except ConnectionError:
            print('Connection Error')

a = SingaporeairService()
a.get_flight_info_by_date()
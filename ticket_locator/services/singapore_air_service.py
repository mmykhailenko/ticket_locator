import requests
import json
from base_service import AirCompanyService
import settings_services
from service_response import ServiceResponse


class SingaporeAirService(AirCompanyService):
    BASE_URL = 'https://apigw.singaporeair.com/api/v1/commercial/flightavailability/get'
    API_KEY = settings_services.env('SINGAPORE_AIR_API_KEY')

    '======Request Mapping====='
    REQUEST_VALUES = {
        'clientUUID': 'SQ-API-Booking-Aggregator',
        'request': {
            'itineraryDetails': [
                {
                    'originAirportCode': 'departure_airport',
                    'destinationAirportCode': 'arrival_airport',
                    'departureDate': 'departure_date',
                }
            ],
            'cabinClass': 'Y',
            'adultCount': 1,
            'flexibleDates': 'false',
        }
    }
    REQUEST_HEADERS = {
        'Content-Type': 'application/json',
        'apikey': API_KEY
    }

    '======Response Mapping======'
    RESPONSE_MAP = {
        'airlinesName': 'Singapore Air',
        'departure_airport': ['response', 'flights', 0, 'originAirportCode'],
        'arrival_airport': ['response', 'flights', 0, 'destinationAirportCode'],
        'departure_date': ['response', 'flights', 0, 'departureDate']
    }

    def get_flight_info_by_date(self, departure_city, arrival_city, departure_date):
        departure_airports = self.find_airport_code(departure_city)
        arrival_airports = self.find_airport_code(arrival_city)
        if departure_airports and arrival_airports:
            for departure_airport in departure_airports:
                for arrival_airport in arrival_airports:
                    self.REQUEST_VALUES['request']['itineraryDetails'][0]['originAirportCode'] = departure_airport
                    self.REQUEST_VALUES['request']['itineraryDetails'][0]['destinationAirportCode'] = arrival_airport
                    self.REQUEST_VALUES['request']['itineraryDetails'][0]['departureDate'] = departure_date
                    try:
                        resp = requests.post(self.BASE_URL, json=self.REQUEST_VALUES, headers=self.REQUEST_HEADERS)
                        resp_json = resp.json()
                        print(resp_json)
                        if resp_json['status'] != 'SUCCESS':
                            continue
                        resp.raise_for_status()
                        return ServiceResponse(resp_json=resp_json,
                                               airlines_name=self.RESPONSE_MAP['airlinesName'],
                                               departure_airport=self.RESPONSE_MAP['departure_airport'],
                                               arrival_airport=self.RESPONSE_MAP['arrival_airport'],
                                               departure_date=self.RESPONSE_MAP['departure_date']
                                               )
                    except requests.exceptions.RequestException as e:
                        break


# t = SingaporeAirService()
#
# r = t.get_flight_info_by_date('Singapore', 'Istanbul', '2021-06-12')
# print(r.departure_airport)
# print(r.arrival_airport)
# print(r.departure_date)

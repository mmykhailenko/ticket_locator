import requests
import json
from . import settings_services
from .base_service import AirCompanyService
from .service_response import ServiceResponse


class TransaviaService(AirCompanyService):
    BASE_URL = 'https://api.transavia.com/v1/flightoffers/'
    API_KEY = settings_services.env('TRANSAVIA_API_KEY')
    EMPTY_JSON=None

    '======Request Mapping====='
    REQUEST_VALUES = {
        'origin': 'departure_airport',
        'destination': 'arrival_airport',
        'originDepartureDate': 'departure_date',
    }
    REQUEST_HEADERS = {
        'Content-Type': 'application/json',
        'apikey': API_KEY,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': '*/*',
        'Cache-Control': 'no-cache'
    }
    '======Response Mapping======'
    RESPONSE_MAP = {
        'airlinesName': 'Transavia',
        'departure_airport': ['flightOffer', 0, 'outboundFlight', 'departureAirport', 'locationCode'],
        'arrival_airport': ['flightOffer', 0, 'outboundFlight', 'arrivalAirport', 'locationCode'],
        'departure_date': ['flightOffer', 0, 'outboundFlight', 'departureDateTime']
    }

    def get_flight_info_by_date(self, departure_city, arrival_city, departure_date):
        departure_airports = self.find_airport_code(departure_city)
        arrival_airports = self.find_airport_code(arrival_city)
        if departure_airports and arrival_airports:
            for departure_airport in departure_airports:
                for arrival_airport in arrival_airports:
                    self.REQUEST_VALUES['origin'] = departure_airport
                    self.REQUEST_VALUES['destination'] = arrival_airport
                    self.REQUEST_VALUES['originDepartureDate'] = departure_date
                    try:
                        resp = requests.get(self.BASE_URL,
                                            params=self.REQUEST_VALUES,
                                            headers=self.REQUEST_HEADERS)
                        resp_json = resp.json()
                        resp.raise_for_status()
                        return ServiceResponse(resp_json=resp_json,
                                               airlines_name=self.RESPONSE_MAP['airlinesName'],
                                               departure_airport=self.RESPONSE_MAP['departure_airport'],
                                               arrival_airport=self.RESPONSE_MAP['arrival_airport'],
                                               departure_date=self.RESPONSE_MAP['departure_date']
                                               ).transform_json()
                    except requests.exceptions.RequestException as e:
                        continue
                    except json.decoder.JSONDecodeError:
                        continue
        return ServiceResponse(resp_json=self.EMPTY_JSON,
                               airlines_name=self.RESPONSE_MAP['airlinesName'],
                               departure_airport=departure_city,
                               arrival_airport=arrival_city,
                               departure_date=departure_date,
                               ).transform_json()

# t = TransaviaService()
#
# r = t.get_flight_info_by_date('Amsterdam', 'Odessa', '20210612')
#
# print(r.departure_airport)
# print(r.arrival_airport)
# print(r.departure_date)
# r = t.get_flight_info_by_date('Amsterdam', 'Tenerife', '20210612')
#
# print(r.departure_airport)
# print(r.arrival_airport)
# print(r.departure_date)
# print(r.status)

from ticket_locator.services.base_service import AirCompanyService
import requests
from ticket_locator.services.service_response import ServiceResponse
from ticket_locator import env


class TransaviaService(AirCompanyService):

    BASE_URL = 'https://api.transavia.com/v1/flightoffers/?'
    API_KEY = {
        'apikey': env('API_KEY_TRANSAVIA'),
    }
    PARAMS = {
        'origin': None,
        'destination': None,
        'originDepartureDate': None
    }
    RESPONSE_MAP = {
        'departure_city': None,
        'arrival_city': None,
        'date': None,
        'price': None
    }

    def _create_params(self, departure_airport, arrival_airport, date):
        self.PARAMS['origin'] = departure_airport
        self.PARAMS['destination'] = arrival_airport
        self.PARAMS['originDepartureDate'] = date

    def _create_response_map(self, resp_json, departure_airport, arrival_airport, date):
        self.RESPONSE_MAP['departure_city'] = departure_airport
        self.RESPONSE_MAP['arrival_city'] = arrival_airport
        self.RESPONSE_MAP['date'] = date
        self.RESPONSE_MAP['price'] = resp_json['flightOffer'][0]['pricingInfoSum']['totalPriceOnePassenger']

    def get_flight_info_by_date(self, departure_airport='LCA', arrival_airport='AMS', date='20210516'):
        date = ''.join(date.split('-'))
        self._create_params(departure_airport, arrival_airport, date)
        try:
            resp = requests.get(url=self.BASE_URL, headers=self.API_KEY, params=self.PARAMS)
            resp_json = resp.json()
            if resp.status_code == 200:
                self._create_response_map(resp_json, departure_airport, arrival_airport, date)
                return ServiceResponse(response=self.RESPONSE_MAP)
            else:
                return ServiceResponse(response=resp_json['errorMessage'])
        except ConnectionError:
            print('Connection Error')




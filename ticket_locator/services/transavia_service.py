import requests
from env_ticket_locator import env
from ticket_locator.services.base_service import AirCompanyService


class TransaviaService(AirCompanyService):
    _BASE_URL = 'https://api.transavia.com/v1/flightoffers/'
    _API_KEY = env('TRANSAVIA_API_KEY')

    _headers = {
        'Host': 'api.transavia.com',
        'apikey': _API_KEY,
    }

    _params = {
        'origin': '',
        'destination': '',
        'originDepartureDate': ''
    }

    def _param_prepare(self, **kwargs):
        params = self._params
        params['origin'] = kwargs['departure_airport']
        params['destination'] = kwargs['arrival_airport']
        params['originDepartureDate'] = kwargs['date']

    def get_flight_info_by_date(self, departure_airport, arrival_airport, date):

        response_service = []

        self._param_prepare(departure_airport=departure_airport,
                            arrival_airport=arrival_airport,
                            date=date)

        response = requests.get(self._BASE_URL, params=self._params, headers=self._headers)

        if response.status_code == 200:
            response_json = response.json()

            flights = response_json['flightOffer']
            for flight in flights:
                flight_info = flight['outboundFlight']
                response_map = {'Airline': flight_info['marketingAirline']['companyShortName'],
                                'FlightNumber': str(flight_info['flightNumber']),
                                'DepartureAirport': flight_info['departureAirport']['locationCode'],
                                'ArrivalAirport': flight_info['arrivalAirport']['locationCode'],
                                'DepartureTime': flight_info['departureDateTime'],
                                'ArrivalTime': flight_info['arrivalDateTime']}
                response_service.append(response_map)

            return [response_service]

        return []

    def get_flight_info_by_period(self, departure_city, arrival_city, start_date, end_date):
        pass

import json
import requests
from ticket_locator import settings
from ticket_locator.services.base_service import AirCompanyService

SUCCESS = 'SUCCESS'


class TurkishAirlinesService(AirCompanyService):
    _BASE_URL = 'https://api.turkishairlines.com/test/getAvailability'
    _API_KEY = settings.TURKISHAIRLINES_API_KEY
    _API_SECRET = settings.TURKISHAIRLINES_SECRET_KEY

    _headers = {
        'Content-Type': 'application/json',
        'apikey': _API_KEY,
        'apisecret': _API_SECRET
    }

    _params = {
        "requestHeader":
            {
                "clientUsername": "OPENAPI",
                "clientTransactionId": "CLIENT_TEST_1",
                "channel": "WEB"
            },
        "ReducedDataIndicator": True,
        "RoutingType": "M",
        "PassengerTypeQuantity": [
            {
                "Code": "adult",
                "Quantity": 1
            }],
        "OriginDestinationInformation": [
            {
                "DepartureDateTime":
                    {
                        "WindowAfter": "P0D",
                        "WindowBefore": "P0D",
                        "Date": ''
                    },
                "OriginLocation":
                    {
                        "LocationCode": '',
                        "AlternateLocation": True,
                        "MultiAirportCityInd": True
                    },
                "DestinationLocation":
                    {
                        "LocationCode": '',
                        "AlternateLocation": True,
                        "MultiAirportCityInd": True
                    },
                "CabinPreferences": [
                    {
                        "Cabin": "ECONOMY"
                    }]
            }]
    }

    def _param_prepare(self, **kwargs):
        date = kwargs['date'][6:8] + {'01': 'JAN',
                                      '02': 'FEB',
                                      '03': 'MAR',
                                      '04': 'APR',
                                      '05': 'MAY',
                                      '06': 'JUN',
                                      '07': 'JUL',
                                      '08': 'AUG',
                                      '09': 'SEP',
                                      '10': 'OCT',
                                      '11': 'NOV',
                                      '12': 'DEC',
                                      }[kwargs['date'][4:6]]
        params = self._params['OriginDestinationInformation'][0]
        params['OriginLocation']['LocationCode'] = kwargs['departure_airport']
        params['DestinationLocation']['LocationCode'] = kwargs['arrival_airport']
        params['DepartureDateTime']['Date'] = date

    @staticmethod
    def _get_flight_data(route_data):
        response_map = {'Airline': route_data['OperatingAirline']['CompanyShortName'],
                        'FlightNumber': route_data['FlightNumber'][2:],
                        'DepartureAirport': route_data['DepartureAirport']['LocationCode'],
                        'ArrivalAirport': route_data['ArrivalAirport']['LocationCode'],
                        'DepartureTime': route_data['DepartureDateTime'][:19],
                        'ArrivalTime': route_data['ArrivalDateTime'][:19]}
        return response_map

    def get_flight_info_by_date(self, departure_airport, arrival_airport, date):

        response_service = []

        self._param_prepare(departure_airport=departure_airport, arrival_airport=arrival_airport, date=date)

        response = requests.post(self._BASE_URL, data=json.dumps(self._params), headers=self._headers)

        if response.status_code == 200:
            response_json = response.json()

            if response_json['status'] == SUCCESS:
                segments = (response_json['data']
                                         ['availabilityOTAResponse']
                                         ['createOTAAirRoute']
                                         ['OTA_AirAvailRS']
                                         ['OriginDestinationInformation']
                                         ['OriginDestinationOptions']
                                         ['OriginDestinationOption'])

                if isinstance(segments, list):
                    for segment in segments:
                        routes = segment['FlightSegment']
                        if isinstance(routes, list):
                            routes_list = []
                            for route in routes:
                                routes_list.append(self._get_flight_data(route))
                            response_service.append(routes_list)
                        else:
                            response_service.append([self._get_flight_data(routes)])
                else:
                    routes = segments['FlightSegment']
                    if isinstance(routes, list):
                        routes_list = []
                        for route in routes:
                            routes_list.append(self._get_flight_data(route))
                        response_service.append(routes_list)
                    else:
                        response_service.append([self._get_flight_data(routes)])

            return response_service

        return []

    def get_flight_info_by_period(self, departure_city, arrival_city, start_date, end_date):
        pass

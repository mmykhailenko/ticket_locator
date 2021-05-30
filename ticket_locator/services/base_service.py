"""
Data format for get_flight_info_by_date method:
    departure_airport - Airport iata code [Example: 'BCN']
    arrival_airport - Airport iata code [Example: 'AMS']
    date - Departure date yyyyMMdd [Example: '20210510']

Data format for get_flight_info_by_period method:
    departure_airport - List of airports iata codes [Example: ['BCN', 'BLA']]
    arrival_airport - List of airports iata codes [Example: ['AMS', 'ORY']]
    start_date - Departure start date range yyyyMMdd [Example: '20210510']
    end_date - Departure end date range yyyyMMdd [Example: '20210527']

Data format for service_response:
    [
        [{
            'AirLine': 'Transavia',
            'FlightNumber': 'HV5132',
            'DepartureAirport': 'BCN',
            'ArrivalAirport': 'AMS',
            'DepartureDateTime': '2021-05-10T15:30:00',
            'ArrivalDateTime': '2021-05-10T17:55:00'
        },
        {
            ...
        }],
    ]
"""


class AirCompanyService:
    _BASE_URL = "API_URL"
    _API_KEY = "API_KEY"

    def get_flight_info_by_date(self, departure_airport, arrival_airport, date):
        raise NotImplementedError

    def get_flight_info_by_period(
        self, departure_city, arrival_city, start_date, end_date
    ):
        raise NotImplementedError

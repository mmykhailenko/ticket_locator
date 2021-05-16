class AirCompanyService:
    BASE_URL = 'https'
    API_KEY = 'env'


    def get_flight_info_by_date(self, departure_airport, arrival_airport, date):
        raise NotImplementedError

    def get_flight_info_by_period(self, departure_airport, arrival_airport, start_date, end_date):
        raise NotImplementedError

import json
import requests

from ticket_locator import settings
from ticket_locator.services.base_service import AirCompanyService
from ticket_locator.services.response_service import ServiseRespons


class TransaviaService(AirCompanyService):
    API_KEY = settings.TRANSAVIA_API_KEY
    BASE_URL = "https://api.transavia.com/v1/flightoffers/"
    HEADERS = {
        'apikey': API_KEY,
    }

    def get_flight_info_by_date(self, departure_airport, arrival_airport, origin_departure_date, product_class,
                                adults_count, child_count):
        params = {"origin": departure_airport, "destination": arrival_airport,
                  "originDepartureDate": origin_departure_date, "adults": adults_count,
                  "children": child_count, "productClass": product_class}
        response = requests.get(url=self.BASE_URL, headers=self.HEADERS, params=params)
        if response.status_code == 200:
            response_dict = json.loads(response.text)
            create_response = ServiseRespons(response_dict["flightOffer"], departure_airport, arrival_airport,
                                             adults_count, product_class, child_count)
            return create_response.response_transavia_airline_by_date_or_period()
        return False

    def get_flight_info_by_period(self, departure_airport, arrival_airport, origin_departure_period, product_class,
                                  adults_count,child_count):
        self.get_flight_info_by_date(departure_airport, arrival_airport, origin_departure_period, product_class,
                                     adults_count, child_count)

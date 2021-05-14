import json
import logging

import requests

from ticket_locator import settings
from ticket_locator.services.base_service import AirCompanyService
from ticket_locator.services.response_service import ServiceResponse

logger = logging.getLogger(__name__)

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
            try:
                response_dict = json.loads(response.text)
            except json.decoder.JSONDecodeError:
                logger.exception(msg="Error serializing the response from the api of the Transavia")
                return False
            create_response = ServiceResponse(response_dict["flightOffer"], departure_airport, arrival_airport,
                                              product_class, adults_count, child_count)
            return create_response.response_transavia_airline_by_date_or_period()
        return False

    def get_flight_info_by_period(self, departure_airport, arrival_airport, origin_departure_period, product_class,
                                  adults_count,child_count):
        # When requesting a period, a list of data is returned,
        # which is parsed in the same way as a request for a specific date,
        # therefore I use the same function as for a date
        self.get_flight_info_by_date(departure_airport, arrival_airport, origin_departure_period, product_class,
                                     adults_count, child_count)

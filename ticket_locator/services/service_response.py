import json


class ServiceResponse:

    def __init__(self, resp_json, airlines_name, departure_airport, arrival_airport, departure_date):
        self.airlines_name = airlines_name
        self.departure_airport = ServiceResponse.apply_mapping(resp_json, departure_airport) \
            if resp_json else departure_airport
        self.arrival_airport = ServiceResponse.apply_mapping(resp_json, arrival_airport) \
            if resp_json else arrival_airport
        self.departure_date = ServiceResponse.apply_mapping(resp_json, departure_date)[:10] \
            if resp_json else departure_date
        self.status = 'SUCCESS' if resp_json else 'FAILURE'

    def transform_json(self):
        return json.dumps({
            'airlinesName': self.airlines_name,
            'departureAirport': self.departure_airport,
            'arrivalAirport': self.arrival_airport,
            'departureDate': self.departure_date
        })

    @staticmethod
    def apply_mapping(data, list_of_keys):
        if data:
            for key in list_of_keys:
                data = data[key]
                list_of_keys = list_of_keys[1:]
            return data
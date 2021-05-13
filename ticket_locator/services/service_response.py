import json


class ServiceResponse:

    def __init__(self, resp_json, airlines_name, departure_airport, arrival_airport, departure_date):
        self.airlines_name = airlines_name
        self.resp_json = resp_json
        self.resp_dict = resp_json
        self.departure_airport = ServiceResponse.apply_mapping(self.resp_dict, departure_airport)
        self.arrival_airport = ServiceResponse.apply_mapping(self.resp_dict, arrival_airport)
        self.departure_date = ServiceResponse.apply_mapping(self.resp_dict, departure_date)[:10]

    def transform_json(self):
        return json.dumps({
            'airlinesName': self.airlines_name,
            'departureAirport': self.departure_airport,
            'arrivalAirport': self.arrival_airport,
            'departureDate': self.departure_date
        })

    @staticmethod
    def apply_mapping(data, list_of_keys):
        for key in list_of_keys:
            data = data[list_of_keys[0]]
            list_of_keys = list_of_keys[1:]
        return data

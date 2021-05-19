import json
import os


class AirCompanyService:
    BASE_URL = 'https'
    AIRPORT_LIST_FILE = r'\ticket_locator\services\data\airport_list.json'
    PATH_TO_DATAFILE = os.getcwd() + AIRPORT_LIST_FILE
    # API_KEY = settings.API_KEY

    def find_airport_code(self, city):
        city = city.lower().capitalize()
        with open(self.PATH_TO_DATAFILE, 'r') as json_file:
            data = json_file.read()
            airport_list = json.loads(data)
            return_list = []
        for entry in airport_list:
            if city == entry[1] and entry[3]:
                return_list.append(entry[3])
        return return_list

    def get_flight_info_by_date(self, departure_airport, arrival_airport, date):
        raise NotImplementedError

    # def get_flight_info_by_period(self, departure_airport, arrival_airport, start_date, end_date):
    #     raise NotImplementedError

# c = AirCompanyService()
# t = c.find_airport_code('Rome')
# print(t)
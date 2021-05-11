import json
import os.path


class AirCompanyService():
    BASE_URL = None
    API_KEY = None

    def get_flight_info_by_date(self, *args, **kwargs):
        raise NotImplementedError

    def get_flight_info_by_period(self, *args, **kwargs):
        raise NotImplementedError

    def _open_iata_data(self):
        with open(os.path.join(os.path.dirname(os.getcwd()),"iata_data/airports.json"),
                  mode="r",encoding="utf8") as file:
            data = json.load(file)
        return data

    def _iata_airport_code_by_city(self,departure_city,arrival_city):
        """The function returns a dictionary of possible airports of departure
        and arrival cities and their abbreviations in IATA format"""
        search_data_airport = {departure_city:{},arrival_city:{}}
        data = self._open_iata_data()
        for key_unit,values_unit in data.items():
            for key,values in values_unit.items():
                if key == "city" and values == departure_city:
                    if values_unit["iata"] != '':
                        search_data_airport[departure_city][values_unit["name"]] = values_unit["iata"]
                if key == "city" and values == arrival_city:
                    if values_unit["iata"] != '':
                        search_data_airport[arrival_city][values_unit["name"]] = values_unit["iata"]
        return search_data_airport





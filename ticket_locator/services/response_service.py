class ServiceResponse():
    RESPONSE_MAP = {
        "departure_airport": "departure_airport",
        "arrival_airport": "arrival_airport",
        "available flights": {
            "aircompany": [],
            "flightnumber": [],
            "departure_date": [],
            "arrival_date": [],
            "departure_time": [],
            "arrival_time": [],
            "transfer": [],
            "cabin_class": "cabin_class",
            "adult": "adult",
            "child": "child",
            "infant": "infant",
            "price": [],
            "currency": "currency_code"}
    }

    def __init__(self, response_data, departure_airport, arrival_airport,cabin_class, adult_count, child_count,
                 infant_count = None):
        self.response_obj_map = self.RESPONSE_MAP
        self.response_data = response_data
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.cabin_class = cabin_class
        self.adult_count = adult_count
        self.child_count = child_count
        self.infant_count = infant_count

    def _split_datetime(self, datetime):
        if not "T" in datetime:
            date, time = datetime.split(" ")
            return date, time
        date, time = datetime.split("T")
        return date, time

    def response_transavia_airline_by_date_or_period(self):
        self.response_obj_map["departure_airport"] = self.departure_airport
        self.response_obj_map["arrival_airport"] = self.arrival_airport
        self.response_obj_map["available flights"]["cabin_class"] = self.cabin_class
        self.response_obj_map["available flights"]["adult"] = self.adult_count
        self.response_obj_map["available flights"]["child"] = self.child_count
        self.response_obj_map["available flights"]["infant"] = self.infant_count
        for unit in self.response_data:
            self.response_obj_map["available flights"]["aircompany"].append(unit["outboundFlight"]["marketingAirline"]
                                                                        ["companyShortName"])
            self.response_obj_map["available flights"]["flightnumber"].append(unit["outboundFlight"]["flightNumber"])
            departure_date, departure_time = self._split_datetime(unit["outboundFlight"]["departureDateTime"])
            self.response_obj_map["available flights"]["departure_date"].append(departure_date)
            self.response_obj_map["available flights"]["departure_time"].append(departure_time)
            arrival_date, arrival_time = self._split_datetime(unit["outboundFlight"]["arrivalDateTime"])
            self.response_obj_map["available flights"]["arrival_date"].append(arrival_date)
            self.response_obj_map["available flights"]["arrival_time"].append(arrival_time)
            # I could not make it so that it would give a route with a transfer, but perhaps here it
            # will be necessary to add the processing of this field from the api's answer
            self.response_obj_map["available flights"]["price"].append(unit["pricingInfoSum"]["totalPriceAllPassengers"])
            self.response_obj_map["available flights"]["currency"] = unit["pricingInfoSum"]["currencyCode"]
        return self.response_obj_map

    def response_singapore_airline_by_date(self):
        temp_data = []  # temporary storage of the flight ID for receiving price information on it
        self.response_obj_map["departure_airport"] = self.departure_airport
        self.response_obj_map["arrival_airport"] = self.arrival_airport
        self.response_obj_map["available flights"]["cabin_class"] = self.cabin_class
        self.response_obj_map["available flights"]["adult"] = self.adult_count
        self.response_obj_map["available flights"]["child"] = self.child_count
        self.response_obj_map["available flights"]["infant"] = self.infant_count
        self.response_obj_map["available flights"]["currency"] = self.response_data["currency"]["code"]
        for flight_count in range(0, len(self.response_data["flights"])):
            for flight in self.response_data["flights"][flight_count]["segments"]:
                for legs_count in range(0, len(flight["legs"])):
                    self.response_obj_map["available flights"]["aircompany"].append(flight["legs"][legs_count]
                                                                                ["marketingAirline"]["name"])
                    self.response_obj_map["available flights"]["flightnumber"].append(flight["legs"]
                                                                                  [legs_count]["flightNumber"])
                    departure_date, departure_time = self._split_datetime(flight["departureDateTime"])
                    self.response_obj_map["available flights"]["departure_date"].append(departure_date)
                    self.response_obj_map["available flights"]["departure_time"].append(departure_time)
                    arrival_date, arrival_time = self._split_datetime(flight["arrivalDateTime"])
                    self.response_obj_map["available flights"]["arrival_date"].append(arrival_date)
                    self.response_obj_map["available flights"]["arrival_time"].append(arrival_time)
                    self.response_obj_map["available flights"]["transfer"].append(flight["legs"][legs_count]["stops"])
                    # This directory is added transfers, but I could not simulate the option with a transplant
                    temp_data.append(flight["segmentID"])
        for recommendations_count in range(0, len(self.response_data["recommendations"])):
            for segment_bounds_count in range(0, len(
                    self.response_data["recommendations"][recommendations_count]["segmentBounds"])):
                for segment in self.response_data["recommendations"][recommendations_count] \
                    ["segmentBounds"][segment_bounds_count]["segments"]:
                    if temp_data:  #Obtaining data on the minimum price for each flight
                        if segment["segmentID"] in temp_data:
                            temp_data.remove(segment["segmentID"])
                            self.response_obj_map["available flights"]["price"].append(self.response_data
                                                                                       ["recommendations"]
                                                                                   [recommendations_count]
                                                                                       ["segmentBounds"]
                                                                                   [segment_bounds_count]
                                                                                       ["fareSummary"]["fareTotal"]
                                                                                       ["totalAmount"])
        return self.response_obj_map




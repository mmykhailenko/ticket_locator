class ServiseRespons():
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

    def __init__(self, response_data, departure_airport, arrival_airport, adult_count, cabin_class, child_count,
                 infant_count = None):
        self.response_data = response_data
        self.departure_airport = departure_airport
        self.arrival_airport = arrival_airport
        self.adult_count = adult_count
        self.child_count = child_count
        self.infant_count = infant_count
        self.cabin_class = cabin_class

    def _split_datetime(self, datetime):
        if not "T" in datetime:
            date, time = datetime.split(" ")
            return date, time
        date, time = datetime.split("T")
        return date, time

    def response_transavia_airline_by_date_or_period(self):
        self.RESPONSE_MAP["departure_airport"] = self.departure_airport
        self.RESPONSE_MAP["arrival_airport"] = self.arrival_airport
        self.RESPONSE_MAP["available flights"]["cabin_class"] = self.cabin_class
        self.RESPONSE_MAP["available flights"]["adult"] = self.adult_count
        self.RESPONSE_MAP["available flights"]["child"] = self.child_count
        self.RESPONSE_MAP["available flights"]["infant"] = self.infant_count
        for unit in self.response_data:
            self.RESPONSE_MAP["available flights"]["aircompany"].append(unit["outboundFlight"]["marketingAirline"]
                                                                        ["companyShortName"])
            self.RESPONSE_MAP["available flights"]["flightnumber"].append(unit["outboundFlight"]["flightNumber"])
            departure_date, departure_time = self._split_datetime(unit["outboundFlight"]["departureDateTime"])
            self.RESPONSE_MAP["available flights"]["departure_date"].append(
                departure_date)
            self.RESPONSE_MAP["available flights"]["departure_time"].append(
                departure_time)
            arrival_date, arrival_time = self._split_datetime(unit["outboundFlight"]["arrivalDateTime"])
            self.RESPONSE_MAP["available flights"]["arrival_date"].append(
                arrival_date)
            self.RESPONSE_MAP["available flights"]["arrival_time"].append(
                arrival_time)
            # I could not make it so that it would give a route with a transfer, but perhaps here it
            # will be necessary to add the processing of this field from the api's answer
            self.RESPONSE_MAP["available flights"]["price"].append(unit["pricingInfoSum"]["totalPriceAllPassengers"])
            self.RESPONSE_MAP["available flights"]["currency"] = unit["pricingInfoSum"]["currencyCode"]
        return self.RESPONSE_MAP

    def response_singapore_airline_by_date(self):
        temp_data = []  # temporary storage of the flight ID for receiving price information on it
        self.RESPONSE_MAP["departure_airport"] = self.departure_airport
        self.RESPONSE_MAP["arrival_airport"] = self.arrival_airport
        self.RESPONSE_MAP["available flights"]["cabin_class"] = self.cabin_class
        self.RESPONSE_MAP["available flights"]["adult"] = self.adult_count
        self.RESPONSE_MAP["available flights"]["child"] = self.child_count
        self.RESPONSE_MAP["available flights"]["infant"] = self.infant_count
        self.RESPONSE_MAP["available flights"]["currency"] = self.response_data["currency"]["code"]
        for flight_count in range(0, len(self.response_data["flights"])):
            for flight in self.response_data["flights"][flight_count]["segments"]:
                for legs_count in range(0, len(flight["legs"])):
                    self.RESPONSE_MAP["available flights"]["aircompany"].append(
                        flight["legs"][legs_count]["marketingAirline"]["name"])
                    self.RESPONSE_MAP["available flights"]["flightnumber"].append(
                        flight["legs"][legs_count]["flightNumber"])
                    departure_date, departure_time = self._split_datetime(flight["departureDateTime"])
                    self.RESPONSE_MAP["available flights"]["departure_date"].append(
                        departure_date)
                    self.RESPONSE_MAP["available flights"]["departure_time"].append(
                        departure_time)
                    arrival_date, arrival_time = self._split_datetime(flight["arrivalDateTime"])
                    self.RESPONSE_MAP["available flights"]["arrival_date"].append(
                        arrival_date)
                    self.RESPONSE_MAP["available flights"]["arrival_time"].append(
                        arrival_time)
                    self.RESPONSE_MAP["available flights"]["transfer"].append(
                        flight["legs"][legs_count]["stops"])
                    temp_data.append(flight["segmentID"])
        for recommendations_count in range(0, len(self.response_data["recommendations"])):
            for segment_bounds_count in range(0, len(
                    self.response_data["recommendations"][recommendations_count]["segmentBounds"])):
                for segment in \
                self.response_data["recommendations"][recommendations_count]["segmentBounds"][segment_bounds_count][
                    "segments"]:
                    if temp_data:
                        if segment["segmentID"] in temp_data:
                            temp_data.remove(segment["segmentID"])
                            self.RESPONSE_MAP["available flights"]["price"].append(self.response_data["recommendations"]
                                                                                   [recommendations_count][
                                                                                       "segmentBounds"]
                                                                                   [segment_bounds_count][
                                                                                       "fareSummary"]["fareTotal"][
                                                                                       "totalAmount"])
        return self.RESPONSE_MAP




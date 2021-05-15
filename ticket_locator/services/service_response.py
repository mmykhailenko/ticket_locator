class ServerResponse:
	def __init__(self, response_json, departure_city, arrival_city):
		self.departure_city = response_json.get(departure_city)
		self.arrival_city = response_json.get(arrival_city)

	def transform_json(self):
		pass
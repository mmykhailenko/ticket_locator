from ticket_locator.services.singaporeair_service import SingaporeairService
from ticket_locator.services.transavia_service import TransaviaService


def get_request(departure_city, arrival_city, date):
	air_companies = [TransaviaService, SingaporeairService]

	for company in air_companies:
		print(f'{company.__name__}:')
		company().get_flight_info_by_date(departure_city, arrival_city, date)


if __name__ == "__main__":
	get_request()
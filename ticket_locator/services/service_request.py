from ticket_locator.services.singaporeair_service import SingaporeairService
from ticket_locator.services.transavia_service import TransaviaService


def get_request(departure_city, arrival_city, date):
	air_companies = [TransaviaService, SingaporeairService]
	result = {}
	for company in air_companies:
		company_res = company().get_flight_info_by_date(departure_city, arrival_city, date)
		result[company.__name__] = company_res
	return result

if __name__ == "__main__":
	get_request(departure_city='LCA', arrival_city='AMS', date='20210523')
from celery import shared_task

from ticket_locator.services.singaporeair_service import SingaporeAirService
from ticket_locator.services.transavia_service import TransaviaService
from ticket_locator.services.turkishairlines_service import TurkishAirlinesService


@shared_task(time_limit=300)
def get_air_data(air_company, request_data):
    result = []
    departure_airport = request_data["departure_airport"]
    arrival_airport = request_data["arrival_airport"]
    departure_date = "".join(request_data["departure_date"].split("-"))
    direct_flight = request_data.get("direct_flight")
    airlines = {
        "TurkishAirlinesService": TurkishAirlinesService,
        "TransaviaService": TransaviaService,
        "SingaporeAirService": SingaporeAirService,
    }
    flight_info = airlines[air_company]().get_flight_info_by_date(
        departure_airport, arrival_airport, departure_date
    )

    if direct_flight:
        for flight in flight_info:
            if len(flight) < 2:
                result += [flight]
    else:
        result += flight_info

    return result

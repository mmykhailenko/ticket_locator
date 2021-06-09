import json
import requests
import telebot
from ticket_locator import settings


BOT_TOKEN = settings.BOT_TOKEN
bot = telebot.TeleBot(BOT_TOKEN)


def search(departure_airport, arrival_airport, departure_date, direct_flight=False):
    URL = 'http://localhost:8000/api/search/'
    _headers = {
        'Content-Type': 'application/json',
        }
    _params = {
      "departure_airport": departure_airport,
      "arrival_airport": arrival_airport,
      "departure_date": departure_date,
      "direct_flight": direct_flight
    }
    response = requests.post(URL, data=json.dumps(_params), headers=_headers)
    return response


def check_iata(iata):
    if iata.isalpha():
        if len(iata) == 3:
            return iata
    return None


def check_date(date):
    import time
    try:
        time.strptime(date, '%Y-%m-%d')
        return date
    except ValueError:
        return None


def check_msg(message):
    try:
        msg = message.text.upper()
        search_text = msg.split(':')[1]
        search_text = search_text.split('/')
        departure_airport = check_iata(search_text[0])
        arrival_airport = check_iata(search_text[1])
        departure_date = check_date(search_text[2])
        if not (departure_airport and arrival_airport):
            bot.send_message(message.from_user.id, f'Упсс, что-то не так. Попробуй еще раз. '
                                                   f'Укажи откуда и куда в формате IATA - '
                                                   f'3 латинские буквы')
        elif not departure_date:
            bot.send_message(message.from_user.id, f'Упсс, что-то не так. Попробуй еще раз. '
                                                   f'Укажи дату в формате "yyyy-mm-dd"')
        else:
            return departure_airport, arrival_airport, departure_date
    except IndexError as e:
        print(e)
        bot.send_message(message.from_user.id, 'Упсс, что-то не так. Попробуй еще раз. '
                                               'Например, вот так "search:AMS/LHR/2021-06-30"')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user = str(message.from_user.first_name).title()
    bot.reply_to(message, f'Привет, {user}! Я - бот.  '
                          f'Я помогу тебе найти рейс, Начни с "search:", '
                          f'далее укажи откуда и куда в формате IATA, укажи дату. '
                          f'Например так: "search:SIN/LHR/2021-06-10"' )


@bot.message_handler(func=lambda message: message.text.startswith('search:'))
def get_text_messages(message):
    try:
        departure_airport, arrival_airport, departure_date = check_msg(message)
    except TypeError as e:
        print(e)
    else:
        response = search(departure_airport, arrival_airport, departure_date)
        if response.status_code == 200:
            response = json.loads(response.text)
            if not response:
                bot.send_message(message.from_user.id, f'На эту дату нет полетов. попробуй другую дату')
            else:
                for flight_info in response:
                    for flight in flight_info:
                        bot.send_message(message.from_user.id,  f"Airline: {flight['Airline']} "
                                                        f"Flight number: {flight['FlightNumber']} "
                                                        f"Departure Airport: {flight['DepartureAirport']} "
                                                        f"Arrival airport: {flight['ArrivalAirport']} "
                                                        f"Departure time: {flight['DepartureTime']} "
                                                        f"Arrival time: {flight['ArrivalTime']}")


if __name__ == "__main__":
    bot.polling(none_stop=False, interval=False, timeout=20)




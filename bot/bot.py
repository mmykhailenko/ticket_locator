import os
import time

import requests
import telebot
from flask import Flask, request
from dotenv import load_dotenv


load_dotenv(dotenv_path=os.path.abspath("bot.env"))
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
time.sleep(1)
bot.set_webhook(url="https://ba7e6304afb3.ngrok.io")
app = Flask(__name__)
app.config.from_pyfile('flask_config.py')


@app.route('/', methods=["POST"])
def webhook():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "ok"


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text=f"Hi, {message.from_user.first_name} "
                                           f"To search for flights, enter a command using the following pattern "
                                           f"/search departure_airport(iata format) arrival_airport(iata format) departure_date(format YYYY-MM-DD)"
                                           f"direct_flight (format y/n)")

@bot.message_handler(func=lambda message:message.text.startswith('/search'))
def search(message):
    request_data = _create_request_data(message)
    response = requests.post(url="http://127.0.0.1:8000/api/search",data = request_data)
    if response.status_code == 200:
        if not response.json():
            return bot.send_message(message.chat.id, text="Alas, there are no options")
        counter = 1
        for flight_route in response.json():
            result_str = f"Option {counter} \n \n"
            for flight_unit in flight_route:
                text_result = f'Airline {flight_unit["Airline"]} \n' \
                              f'FlightNumber {flight_unit["FlightNumber"]} \n' \
                              f'DepartureAirport {flight_unit["DepartureAirport"]} \n' \
                              f'ArrivalAirport {flight_unit["ArrivalAirport"]} \n' \
                              f'DepartureTime {flight_unit["DepartureTime"]} \n' \
                              f'ArrivalTime {flight_unit["ArrivalTime"]} \n \n'
                result_str+=text_result
            counter+=1
            bot.send_message(message.chat.id, text=result_str)
        return
    return bot.send_message(message.chat.id, text="Oh something went wrong, try again")

def _create_request_data(message):
    data_from_message = (message.text).split(" ")[1:]
    if len(data_from_message) != 4:
        return bot.send_message(message.chat.id, text="You entered the wrong number of parameters")
    else:
        if data_from_message[3] == "y":
            data_from_message[3] = True
        else:
            data_from_message[3] = False
    print(data_from_message)
    request_data = {
        "departure_airport": (data_from_message[0]).upper(),
        "arrival_airport": (data_from_message[1]).upper(),
        "departure_date": data_from_message[2],
        "direct_flight": data_from_message[3]
    }
    return request_data


if __name__ == "__main__":
    app.run()

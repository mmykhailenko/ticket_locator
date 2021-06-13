import re
from django.core.management.base import BaseCommand
from ticket_locator import settings
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
from telegram.ext import Updater
from telegram.utils.request import Request

from hello_world.views import FlightSearchView
from . import constants


def start(update: Update, _: CallbackContext) -> None:
    user_name = update.message.chat.first_name
    reply_text = (
        f"\U00002708 Привет {user_name}!\n"
        f"\U00002708 Рады видеть тебя:)\U0000270A\n\n"
        f"\U00002708 Нужна помощь? Введите /help"
    )
    update.message.reply_text(text=reply_text)


def search(update: Update, _: CallbackContext) -> None:
    text = update.message.text.split(" ")
    if len(text) > 2:
        if (
            re.search("[A-Za-z]{3}", text[0])
            and re.search("[A-Za-z]{3}", text[1])
            and re.search("[0-9]{8}", text[2])
        ):
            request_data = {
                "departure_airport": text[0].upper(),
                "arrival_airport": text[1].upper(),
                "departure_date": text[2].upper(),
                "direct_flight": text[3]
                if len(text) > 3 and text[3].upper() == "DIRECT"
                else None,
            }
            response = FlightSearchView().get_air_info(request_data)
            if response:
                for flights in response:
                    reply_text = "--------------------\n"
                    reply_text += "С пересадкой\n" if len(flights) > 1 else "Прямой\n"
                    reply_text += "--------------------\n\n"
                    for flight_item in flights:
                        reply_text += (
                            f'Из: {flight_item["DepartureAirport"]} В: {flight_item["ArrivalAirport"]}\n'
                            f'Рейс: {flight_item["Airline"]}{flight_item["FlightNumber"]}\n'
                            f'Время вылета: {" ".join(flight_item["DepartureTime"].split("T"))}\n'
                            f'Время прибытия: {" ".join(flight_item["ArrivalTime"].split("T"))}\n\n'
                        )
                    update.message.reply_text(text=reply_text)
            else:
                update.message.reply_text(text=constants.BOT_NO_RESULT_TEXT)
        else:
            update.message.reply_text(text=constants.BOT_ERROR_TEXT)
    else:
        update.message.reply_text(text=constants.BOT_ERROR_TEXT)


def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(text=constants.BOT_HELP_TEXT)


class Command(BaseCommand):
    help = "Телеграм-бот"

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=1.0,
            read_timeout=2.0,
        )
        bot = Bot(
            request=request,
            token=settings.TELEGRAM_BOT_TOKEN,
            base_url=settings.TELEGRAM_BOT_URL,
        )

        updater = Updater(
            bot=bot,
            use_context=True,
        )

        updater.dispatcher.add_handler(CommandHandler("start", start))
        updater.dispatcher.add_handler(CommandHandler("help", help_command))
        updater.dispatcher.add_handler(CommandHandler("search", search))
        updater.dispatcher.add_handler(
            MessageHandler(Filters.text & ~Filters.command, search)
        )

        updater.start_polling()
        updater.idle()

import datetime
import json
import time
import SendGotify
from DailyNotifierConfig import (
    FOLDER_PATH,
    NAME_DAYS_PATH,
    GOTIFY_DAILY_TOKEN,
    TELEGRAM_IDS_LIST,
)
import FetchWeather
import TelegramSender
import SpecialsReminder

CURRENT_DATE = datetime.datetime.today()
# FINNISH_DATE = CURRENT_DATE.strftime("%d.%m.%Y")
TITLE = f'{CURRENT_DATE.strftime("%d.%m.%Y (%a)")}'
MONTH = CURRENT_DATE.month
DAY = CURRENT_DATE.day
YEAR = CURRENT_DATE.year
MONTH_DATE = f"{MONTH:02d}-{DAY:02d}"


def get_flag_day():
    """
    Gets today's flag day's information from file
    :return: str, Today's flag day, empty if none
    """
    try:
        with open(f"{FOLDER_PATH}flags{YEAR}.json", "r", encoding="utf-8") as file:
            flags = json.load(file)
    except IOError:
        flags = {MONTH_DATE: {"name": "Couldn't fetch flag day"}}
    flag = flags.get(MONTH_DATE)
    if flag is not None:
        flag_name = f"🇫🇮{flag.get('name')}"
    else:
        flag_name = ""
    return flag_name


def get_holiday():
    """
    Gets today's holiday's information from a file
    :return: str, Today's holiday, empty if none
    """
    try:
        with open(f"{FOLDER_PATH}holidays{YEAR}.json", "r", encoding="utf-8") as file:
            holidays = json.load(file)
    except IOError:
        holidays = {MONTH_DATE: {"name": "Couldn't fetch holiday", "status": "Error"}}
    holiday = holidays.get(MONTH_DATE)
    if holiday is not None:
        holiday_name = f"🎉{holiday.get('name')} ({holiday.get('status')})"
    else:
        holiday_name = ""
    return holiday_name


def get_custom_holiday():
    """
    Gets today's custom holiday's information from a file
    :return: str, Today's custom holiday, empty if none
    """
    try:
        with open(f"{FOLDER_PATH}custom_holidays.json", "r", encoding="utf-8") as file:
            holidays = json.load(file)
    except IOError:
        holidays = {
            MONTH_DATE: {"name": "Couldn't fetch custom holiday", "status": "Error"}
        }
    holiday = holidays.get(MONTH_DATE)
    if holiday is not None:
        holiday_name = f"🎉{holiday.get('name')} ({holiday.get('status')})"
    else:
        holiday_name = ""
    return holiday_name


def get_name_days():
    """
    Gets today's name day's information from file
    :return: list, Today's name days
    """
    try:
        with open(NAME_DAYS_PATH, "r", encoding="utf-8") as file:
            name_days = json.load(file)
    except IOError:
        name_days = {MONTH_DATE: ["Couldn't fetch name day"]}
    name_day = name_days.get(MONTH_DATE)
    # If name_day is empty
    if not name_day:
        name_day = ["(Ei nimipäivää tänään)"]
    return name_day


def get_weather_and_times():
    """
    Get's weather and sun times as string from file
    :return: str, Empty if there was a problem
    """
    # Try to fetch the data 6 times in total
    wait_times = [0, 5, 10, 30, 60, 1800]
    for wait_time in wait_times:
        print(f"Trying to fetch weather. Sleeping for {wait_time} seconds")
        # Wait 0 s, 5 s, 10 s, 30 s, 1 min and the last time 30 min
        time.sleep(wait_time)
        fetched_weather_data = FetchWeather.fetch_data()
        # If data was successfully fetched, stop trying again
        if fetched_weather_data is not None:
            break
    if fetched_weather_data is not None:
        weather = FetchWeather.get_weather_icons(fetched_weather_data)
        all_sun_times = FetchWeather.get_sun_times(fetched_weather_data)
        # Format eg. 11:15 to 11h 15min
        total_sun_time = f'{all_sun_times[-1].replace(":", "h ")}min'
        # Only leave sunrise and sunset to sun times
        sun_times = all_sun_times[:-1]
        temperatures = FetchWeather.get_temperatures(fetched_weather_data)
        weather_and_times = (
            f'{"".join(weather)} ({" ... ".join(temperatures)})\n↑{" - ".join(sun_times)}↓ '
            f"({total_sun_time})"
        )
    else:
        weather_and_times = ""
    return weather_and_times


def craft_messages(
    flag, holiday, custom_holiday, name_day, weather_and_times, debug_info=""
):
    """
    Crafts messages from given information
    :param flag: str, Today's flag day
    :param holiday: str, Today's holiday
    :param custom_holiday: str, Today's custom holiday
    :param name_day: list, Today's name days
    :param weather_and_times: str, Today's weather
    :param debug_info:
    :return: str, str
    """
    flag_and_holiday = f"{flag}\n{holiday}\n{custom_holiday}".strip()
    message = (
        f"{weather_and_times}\n**{', '.join(name_day)}**\n\n{flag_and_holiday}".strip()
    )
    telegram_message = f"{TITLE}\n{weather_and_times}\n***{', '.join(name_day)}***\n\n{flag_and_holiday}".strip()
    if debug_info != "":
        message += f"\n({debug_info})"
    return message.replace("\n", "  \n"), telegram_message


def main():
    start_time = time.time()
    flag = get_flag_day()
    name_day = get_name_days()
    weather_and_times = get_weather_and_times()
    holiday = get_holiday()
    custom_holiday = get_custom_holiday()
    debug_info = f"{round((time.time() - start_time) * 1000, 2)} ms"
    message, telegram_message = craft_messages(
        flag, holiday, custom_holiday, name_day, weather_and_times, debug_info
    )
    print(message)

    SendGotify.send(GOTIFY_DAILY_TOKEN, TITLE, message)
    for telegram_id in TELEGRAM_IDS_LIST:
        TelegramSender.send(telegram_message, telegram_id)
    SpecialsReminder.remind()


if __name__ == "__main__":
    main()

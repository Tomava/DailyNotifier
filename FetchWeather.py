import urllib.request
import json
from datetime import datetime
from DailyNotifierConfig import LATITUDE, LONGITUDE, WEATHER_API

FILE_NAME = "DailyWeather.json"
ICONS = {
    "01d": "☀",
    "02d": "🌤",
    "03d": "☁",
    "04d": "☁",
    "09d": "🌧",
    "10d": "🌧",
    "11d": "🌩",
    "13d": "❄",
    "50d": "🌫",
    "01n": "☀",
    "02n": "🌤",
    "03n": "☁",
    "04n": "☁",
    "09n": "🌧",
    "10n": "🌧",
    "11n": "🌩",
    "13n": "❄",
    "50n": "🌫"
}

def fetch_data():
    """
    Fetches the weather data and returns it as a dict
    :return: dict
    """
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={LATITUDE}&lon={LONGITUDE}&exclude=current,minutely,alerts&appid={WEATHER_API}&units=metric&cnt=8"
    try:
        with urllib.request.urlopen(url) as site:
            data = json.loads(site.read())
    except:
        return None
    # try:
    #     with open(f"{FOLDER_PATH}FILE_NAME", "w") as file:
    #         json.dump(data, file, indent=2, ensure_ascii=False)
    # except IOError:
    #     return None
    return data


def get_weather_icons(data):
    """
    Returns correct weather icons
    :return: list
    """
    today = datetime.today()
    list_of_icons = []
    for hour_data in data.get("list"):
        hour_time = datetime.fromtimestamp(hour_data.get("dt"))
        # Break on tomorrow
        if hour_time.date() != today.date():
            break
        # Only get hours 9, 12, 15, 18, 21
        if 8 < hour_time.hour < 22 and hour_time.hour % 3 == 0:
            icon_id = hour_data.get("weather")[0].get("icon")
            icon = ICONS.get(icon_id)
            list_of_icons.append(icon)
    # Check that there is at least one icon
    if len(list_of_icons) < 1:
        daily = data.get("list")
        icon_id = daily[0].get("weather")[0].get("icon")
        icon = ICONS.get(icon_id)
        list_of_icons.append(icon)
    return list_of_icons


def get_sun_times(data):
    """
    Returns today's sunrise and sunset as strings
    :return: str, str
    """
    sunrise_iso = datetime.fromtimestamp(data.get("city").get("sunrise"))
    sunset_iso = datetime.fromtimestamp(data.get("city").get("sunset"))

    sunrise = datetime.time(sunrise_iso).strftime("%H:%M")
    sunset = datetime.time(sunset_iso).strftime("%H:%M")

    # [:-3} removes seconds from time, replace seconds so it doesn't seem like there is an extra minute
    total_time = str((sunset_iso.replace(second=0) - sunrise_iso.replace(second=0)))[:-3]

    return str(sunrise), str(sunset), str(total_time)


def get_temperatures(data):
    """
    Returns today's min and max temperatures as strings rounded to whole number
    :return: str, str: min, max
    """
    today = datetime.today()
    temperatures_min = []
    temperatures_max = []
    for hour_data in data.get("list"):
        hour_time = datetime.fromtimestamp(hour_data.get("dt"))
        # Break on tomorrow
        if hour_time.date() != today.date():
            break
        temperatures_min.append(hour_data.get("main").get("temp_min"))
        temperatures_max.append(hour_data.get("main").get("temp_max"))
    min_temp = min(temperatures_min)
    max_temp = max(temperatures_max)
    return str(min_temp) + "°C", str(max_temp) + "°C"

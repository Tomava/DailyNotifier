import os
from dotenv import load_dotenv

load_dotenv()
PUSHOVER_DAILY_API_KEY = os.getenv('PUSHOVER_DAILY_API_KEY')
PUSHOVER_SPECIALS_API_KEY = os.getenv('PUSHOVER_SPECIALS_API_KEY')
PUSHOVER_USER_KEY = os.getenv('PUSHOVER_USER_KEY')
WEATHER_API = os.getenv('WEATHER_API')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_IDS = os.getenv('TELEGRAM_IDS')

TELEGRAM_IDS_LIST = [x for x in os.getenv("TELEGRAM_IDS").split(" ")]

FOLDER_PATH = f"Fetched_data{os.sep}"
NAME_DAYS_PATH = f"{FOLDER_PATH}namedays.json"
SPECIALS_MONTHLY_PATH = f"{FOLDER_PATH}specials_monthly.json"
SPECIALS_YEARLY_PATH = f"{FOLDER_PATH}specials_yearly.json"

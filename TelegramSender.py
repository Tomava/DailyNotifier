import urllib.request
import requests
from DailyNotifierConfig import TELEGRAM_BOT_TOKEN


def send(bot_message, chat_id):
    bot_chatID = str(chat_id)
    bot_message = urllib.parse.quote_plus(bot_message)
    send_text = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={bot_message}"
    response = requests.get(send_text)
    return response.json()

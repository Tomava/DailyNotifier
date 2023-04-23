import requests
from DailyNotifierConfig import PUSHOVER_USER_KEY

URL = "https://api.pushover.net/1/messages.json"

def send(api_key, title, message):
    json_data = {"token": api_key, "user": PUSHOVER_USER_KEY, "message": message, "title": title, "html": 1}
    try:
        request = requests.post(URL, json=json_data)
        return True
    except:
        return False

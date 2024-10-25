import requests
from DailyNotifierConfig import GOTIFY_URL

def send(token, title, message):
    json_data = {
        "message": message,
        "title": title,
        "priority": 5
    }
    try:
        requests.post(f"{GOTIFY_URL}/message", json=json_data, params={"token": token}, timeout=60)
        return True
    except:
        return False

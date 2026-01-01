import requests
from latest_user_agents import get_random_user_agent


def fetch_url(url):
    try:
        r = requests.get(
            url, headers={"User-Agent": get_random_user_agent()}, timeout=30
        )
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return ""
    return r.text

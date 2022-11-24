from pathlib import Path
import os
import urllib.request

HOME = str(Path.home())
USER_AGENT_FILE = HOME + os.sep + 'UserAgent' + os.sep + 'user_agent.txt'


def fetch_url(url):
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    try:
        with open(USER_AGENT_FILE, "r") as file:
            user_agent = file.readline()
    except IOError:
        pass
    try:
        req = urllib.request.Request(
            url,
            data=None,
            headers={
                'User-Agent': user_agent
            }
        )
    except:
        print("Error")
    resp = urllib.request.urlopen(req)
    respData = resp.read().decode('utf-8')
    return respData
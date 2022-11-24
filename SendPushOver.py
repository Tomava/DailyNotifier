from pushover import init, Client


def send(init_key, title, message):
    try:
        init(init_key)
        Client().send_message(message, title=title, html=1)
        return True
    except:
        return False

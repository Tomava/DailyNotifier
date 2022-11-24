# DailyNotifier

Sends daily notification with various information

## Installation
1. Install **Python 3** (minimum Python **3.8**) and **Pip**.
2. Install dependencies:
```sh
pip install -r requirements.txt
```
3. Get telegram bot token and chat id or Pushover API key(s) as well as Openweathermap API key
4. Create a file called *.env* in the root of the project and add the lines from the *.env.template* with previously gotten keys
5. Run FetchFlagDays.py and FetchHolidays.py to fetch information
6. Run **DailyNotifier.py**
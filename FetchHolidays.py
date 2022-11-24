import re
import json
import datetime
from DailyNotifierConfig import FOLDER_PATH
from Fetcher import fetch_url

CURRENT_YEAR = datetime.datetime.today().year


def main():
    base_url = "https://www.xn--juhlapyht-22a.fi/viralliset-pyhapaivat-ja-vapaapaivat/kaikki-pyhapaivat-"
    url = f"{base_url}{CURRENT_YEAR}"
    respData = fetch_url(url)

    all_holidays = {}
    holidays_html = re.findall('<ul>(.*?)</ul>', str(respData).replace("\n", ""))
    # holidays_html = re.findall(f'<p>(.*?)</p>', holidays_html[-1])
    list_of_holidays = re.findall('<li>(.*?)</li>', holidays_html[0])
    print(list_of_holidays)
    for holiday in list_of_holidays:
        holiday = holiday.replace('<span style="color: #439cee;"><em>', '')
        date = re.findall('^(.*?) ', holiday)[0]
        date = str(date).strip().split(".")
        day = int(date[0])
        month = int(date[1])
        date = f"{month:02d}-{day:02d}"
        if holiday.count("title") > 0:
            day_name = re.findall('>(.*?)</a>', holiday)[0].strip()
            status = "Virallinen"
        else:
            day_name = re.findall('; (.*?) \(', holiday)[0].strip()
            status = "Epävirallinen"
        print(date, day_name, status)
        all_holidays[date] = {'name': day_name, 'status': status}
    with open(f"{FOLDER_PATH}holidays{CURRENT_YEAR}.json", "w", encoding="utf-8") as file:
        json.dump(all_holidays, file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()

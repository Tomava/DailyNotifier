import re
import json
import datetime
from DailyNotifierConfig import FOLDER_PATH
from Fetcher import fetch_url

CURRENT_YEAR = datetime.datetime.today().year


def main():
    base_url = "https://intermin.fi/suomen-lippu/liputuspaivat/"
    # https://intermin.fi/suomen-lippu/liputuspaivat/2021
    url = f"{base_url}{CURRENT_YEAR}"
    respData = fetch_url(url)

    all_flag_days = {}
    table_html = re.findall(f'data-analytics-asset-title="Liputuspäivät vuonna {CURRENT_YEAR}(?s:.*?)</div>',
                            str(respData))
    flag_days_html = re.findall('<li>(.*?)</li>', str(table_html))
    for flag_day in flag_days_html:
        finnish_date = re.match('\d{1,2}\.\d{1,2}\.', flag_day)
        # There can be an extra space before year
        date = finnish_date.group().strip().split(".")
        day = int(date[0])
        month = int(date[1])
        date = f"{month:02d}-{day:02d}"
        day_name = str(flag_day).replace(finnish_date.group(), "").strip()
        status = "Virallinen liputuspäivä"
        print(date, day_name, status)
        all_flag_days[date] = {'name': day_name, 'status': status}
    with open(f"{FOLDER_PATH}flags{CURRENT_YEAR}.json", "w", encoding="utf-8") as file:
        json.dump(all_flag_days, file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()

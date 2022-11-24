import datetime
import json
import SendPushOver
from dateutil import relativedelta
from DailyNotifierConfig import SPECIALS_MONTHLY_PATH, SPECIALS_YEARLY_PATH


def get_year_month_day(date):
    """
    Gets year, month and day from date
    :param date: datetime object, Given date
    :return: int, int, int
    """
    year = date.year
    month = date.month
    day = date.day
    return year, month, day


def get_age(current_date, special_date):
    """
    Calculates age in total months, whole years and whole months
    :param current_date: datetime object, Current date
    :param special_date: datetime object, Date of the special
    :return: int, int, int, int
    """
    current_year, current_month, current_day = get_year_month_day(current_date)
    special_year, special_month, special_day = get_year_month_day(special_date)
    # Count how many months from 0 has passed until the first special year
    start_months = special_year * 12 + special_month
    # Subtract that from current amount of months since 0
    age_total_months = (current_year * 12 + current_month) - start_months
    age_total_days = (current_date - special_date).days
    age_year = int(age_total_months / 12)
    age_month = age_total_months - (age_year * 12)
    return age_total_months, age_total_days, age_year, age_month


def get_yearly(date, yearly_message):
    """
    Gets yearly notifiers
    :param date: datetime object
    :param yearly_message: str, Message to append to
    :return: str, yearly_message
    """
    year, month, day = get_year_month_day(date)
    # ISO-format month and day
    month_day = f"{month:02d}-{day:02d}"
    try:
        with open(SPECIALS_YEARLY_PATH, "r", encoding="utf-8") as file:
            specials_yearly = json.load(file)
    except IOError:
        specials_yearly = {month_day: [{'name': "Couldn't fetch yearly specials", 'date': date}]}
    special_yearly = specials_yearly.get(month_day)
    if special_yearly is not None:
        for special in special_yearly:
            special_date = datetime.datetime.fromisoformat(special.get("date"))
            age_total_months, age_total_days, age_year, _ = get_age(date, special_date)
            yearly_message += f"{special.get('name')} ({age_year} years) [{age_total_months} months] " \
                              f"[{age_total_days} days]\n"
        # Add extra space after last
        yearly_message += "\n"
    else:
        yearly_message = ""
    return yearly_message


def get_monthly(date, monthly_message):
    """
    Gets monthly notifiers
    :param date: datetime object
    :param monthly_message: str, Message to append to
    :return: str, monthly_message
    """
    year, month, day = get_year_month_day(date)
    iso_day = f"{day:02d}"
    try:
        with open(SPECIALS_MONTHLY_PATH, "r", encoding="utf-8") as file:
            specials_monthly = json.load(file)
    except IOError:
        specials_monthly = {iso_day: [{"name": "Couldn't fetch monthly specials", "date": date}]}
    special_monthly = specials_monthly.get(iso_day)
    if special_monthly is not None:
        for special in special_monthly:
            special_date = datetime.datetime.fromisoformat(special.get("date"))
            age_total_months, age_total_days, age_year, age_month = get_age(date, special_date)
            monthly_message += f"{special.get('name')}"
            if age_year == 0:
                monthly_message += f" ({age_month} months)"
            elif age_month == 0:
                monthly_message += f" ({age_year} years)"
            else:
                monthly_message += f" ({age_year} years, {age_month} months)"
            monthly_message += f" [{age_total_months} months] [{age_total_days} days]\n"
    else:
        monthly_message = ""
    return monthly_message


def remind(PUSHOVER_SPECIALS_API_KEY):
    """
    Sends a daily reminder of special days
    :param PUSHOVER_SPECIALS_API_KEY: str, Pushover api key
    :return: nothing
    """
    # Make empty messages
    yearly_template = "Yearly:\n"
    yearly_two_week_template = "In two weeks:\n"
    monthly_template = "Monthly:\n"
    message = ""

    current_date = datetime.datetime.today()
    # Used for testing
    # current_date = datetime.datetime.fromisoformat("2021-12-06T12:00:00")
    finnish_date = current_date.strftime("%d.%m.%Y")
    two_week_date = current_date + relativedelta.relativedelta(days=14)

    yearly_message = get_yearly(current_date, yearly_template)
    yearly_two_week_message = get_yearly(two_week_date, yearly_two_week_template)
    monthly_message = get_monthly(current_date, monthly_template)

    message += f"{yearly_message}{yearly_two_week_message}{monthly_message}".strip()
    print(message)
    # Format (25.02.2021), Title = Date:
    '''
    Yearly:
    X (21 years) [252 total months]
    
    In two weeks:
    Y (14 years) [168 total months]
    
    Monthly:
    Z (1 years, 3 months) [15 total months]
    '''
    # Format (14.04.2021), Title = Date:
    '''
    Yearly:
    X (21 years) [252 months] [7560 days]

    In two weeks:
    Y (14 years) [168 months] [5040 days]

    Monthly:
    Z (1 years, 3 months) [15 months] [455 days]
    '''
    if message != "":
        SendPushOver.send(PUSHOVER_SPECIALS_API_KEY, str(finnish_date), message)

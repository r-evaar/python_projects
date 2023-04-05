import requests
from datetime import datetime, timedelta

def get_api_data(endpoint, params):
    response = requests.get(url=endpoint, params=params)
    response.raise_for_status()
    return response.json()

def day_before(day):
    """
    Return the string date of the day before a given day.
    The returned day has to be a business day; otherwise,
    the day before it is given.
    Args:
        day: datetime obj

    Returns: datetime obj
    """
    test_day = day
    while True:
        test_day = test_day - timedelta(days=1)
        if test_day.weekday() in [5, 6]:
            continue
        else:
            break
    return test_day

def get_prev_two_days():
    today = datetime.today()
    yesterday = day_before(today)
    before_yesterday = day_before(yesterday)
    return \
        yesterday.__str__().split(' ')[0], \
        before_yesterday.__str__().split(' ')[0]



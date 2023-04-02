import requests
import smtplib
from datetime import datetime, timedelta
from time import time

SUNSET_EP = 'https://api.sunrise-sunset.org/json'
ISS_EP = 'http://api.open-notify.org/iss-now.json'
MY_LAT = 24.407538
MY_LNG = 54.564830
MARGIN = 5
SMTP_SERVER, PORT = 'smtp.gmail.com', 587
SENDER_ID, KEY = 'evaar.test@gmail.com', 'jjfbtmjgdzscpmgs'
TARGET = 'evaar.test@outlook.com'

class Timer:
    def __init__(self, p): self.p = p; self.t = time()

    def triggered(self):
        if time()-self.t > self.p: self.t = time(); return True
        else: return False

def get_api_data(ep, p=None): r = requests.get(url=ep, params=p); r.raise_for_status(); return r.json()

def to_date(string):
    dt, _ = string.split('+')
    dt_utc = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    return dt_utc + timedelta(hours=4)

def get_local_info():
    params = {'lat': MY_LAT, 'lng': MY_LNG, 'formatted': 0}
    data = get_api_data(SUNSET_EP, params)
    sunrise = to_date(data['results']['sunrise'])+timedelta(days=1)
    sunset = to_date(data['results']['sunset'])
    return {'sunset': sunset, 'sunrise': sunrise}

def is_sunset(info):
    return info['sunset'] < datetime.now() < info['sunrise']

def near_me(loc):
    within_lat = abs(float(loc['latitude']) - MY_LAT) < MARGIN
    within_lng = abs(float(loc['longitude']) - MY_LNG) < MARGIN
    return within_lat and within_lng

def send_notification(loc):
    subject = 'Subject:ISS is Near Your Location\n'
    body = f'''
    You can observe the International Space Station tonight.
    
    Location: {loc['latitude']}N, {loc['longitude']}E
    '''
    with smtplib.SMTP(SMTP_SERVER, PORT) as connection:
        connection.starttls()
        connection.login(user=SENDER_ID, password=KEY)
        connection.sendmail(from_addr=SENDER_ID, to_addrs=TARGET, msg=subject+body)


if __name__ == '__main__':

    timer = Timer(60)
    while True:

        if not timer.triggered():
            continue

        local_info = get_local_info()

        if not is_sunset(local_info):
            continue

        iss_loc = get_api_data(ISS_EP)['iss_position']

        if near_me(iss_loc):
            send_notification(iss_loc)



import requests
import json
import os
import numpy as np
from twilio.rest import Client

API_KEY = '6663f3e5fc154333353ffc31b27cac02'
WEATHER_ENDPOINT = 'https://api.openweathermap.org/data/2.5/weather'
FORECAST_ENDPOINT = 'https://api.openweathermap.org/data/2.5/forecast'
ONE_CALL_ENDPOINT = 'https://api.openweathermap.org/data/2.8/onecall'
MY_LAT = 39#24.407538
MY_LNG = 19#54.564830
NUM_HRS = 12

TWILIO_SID = 'AC2c602693cda98c15c6419c013bde3353'
# Key is saved as an environment variable to prevent security leak when code is shared
TWILIO_KEY = os.environ.get('TWILIO_KEY')  # Edit Configurations -> Environment variables
                                           # NOTE: no "
                                           # In Bash:
                                           # $ export TWILIO_KEY=<key>

params = {
    'lat': MY_LAT,
    'lon': MY_LNG,
    'appid': API_KEY,
    'exclude': 'current,minutely,daily'
}

response = requests.get(url=ONE_CALL_ENDPOINT, params=params)
response.raise_for_status()

data = response.json()['hourly']

weather_ids = [hour['weather'][0]['id'] for hour in data][:NUM_HRS]

msg = "It's going to rain today. Bring an umbrella!" \
    if (np.asarray(weather_ids) < 700).any() else "The weather is good today"

sms_client = Client(TWILIO_SID, TWILIO_KEY)
sms = sms_client.messages.create(
    from_='+15855522877',
    body=msg,
    to='+971521240215'
)

print(sms.status)

with open('response.json', 'w') as f:
    json.dump(data, f, indent=4)

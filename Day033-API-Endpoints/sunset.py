import requests

SUNSET_EP = 'https://api.sunrise-sunset.org/json'
ISS_EP = 'http://api.open-notify.org/iss-now.json'
MY_LAT = 24.407538
MY_LNG = 54.564830

def get_api_data(ep, p=None): r = requests.get(ep, params=p); r.raise_for_status(); return r.json()

params = {
    'lat': MY_LAT,
    'lng': MY_LNG,
    'formatted': 0
}

print(get_api_data(SUNSET_EP, params))
print(f"To get the data in browser: {SUNSET_EP}?lat={MY_LAT}&lng={MY_LNG}")

import os
import requests
from datetime import datetime

NUTR_ID = os.environ.get("NUTR_ID")
NUTR_KEY = os.environ.get("NUTR_KEY")
NUTR_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_ENDPOINT = f"https://api.sheety.co/{os.environ.get('SHEETY_SHEET')}/myWorkouts/workouts"

GENDER = "male"
WEIGHT = 69
HEIGHT = 175
AGE = 24

txt = 'I ran for 3 miles, walked for 5km, then jogged for half an hour'

headers = {
    "x-app-id": NUTR_ID,
    "x-app-key": NUTR_KEY
}

inpt = {
    "query": txt,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE
}

response = requests.post(url=NUTR_ENDPOINT, json=inpt, headers=headers)
exercises = response.json()['exercises']

header = {"Authorization": "Bearer "+os.environ.get('SHEETY_KEY')}
for exercise in exercises:

    now = datetime.today()
    row = {
        'workout': {
            'date': now.strftime('%d/%m/%Y'),
            'time': now.strftime('%H:%M:%S'),
            'exercise': exercise['name'].title(),
            'duration': exercise['duration_min'],
            'calories': exercise['nf_calories']
        }
    }
    response = requests.post(url=SHEETY_ENDPOINT, json=row, headers=header)
    print(response.text)

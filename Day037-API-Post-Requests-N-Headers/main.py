import requests
import os
from datetime import datetime, timedelta

username = 'evaar'
key = os.environ.get('PIXELA_KEY')

PIXELA_ENDPOINT_ROOT = 'https://pixe.la'
USERS = '/v1/users'

# --- Creating a new user --------------------------------------------------------- #

user_endpoint = PIXELA_ENDPOINT_ROOT+USERS

params = {
    "username": username,
    "token": key,
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}

# response = requests.post(url=user_endpoint, json=params)
# print(response.json())

# --- Set up a new graph ---------------------------------------------------------- #

graph = f'{user_endpoint}/{username}/graphs'
graph_id = "t001"

graph_config = {
    "id":       graph_id,
    "name":     "Walking Graph",
    "unit":     "km",
    "type":     "float",
    "color":    "ajisai"
}

headers = {
    "X-USER-TOKEN": key
}

# response = requests.post(url=graph, json=graph_config, headers=headers)
# print(response.json())

# --- Add a pixel to the graph --------------------------------------------------- #

pixel = f'{graph}/{graph_id}'
today = datetime.today()
yesterday = today - timedelta(days=1)

pixel_today_data = {
    "date": today.strftime('%Y%m%d'),
    "quantity": "1.1"
}

# response = requests.post(url=pixel, headers=headers, json=pixel_today_data)
# print(response.text)

pixel_yesterday_data = {
    "date": yesterday.strftime('%Y%m%d'),
    "quantity": "9.3"
}

# response = requests.post(url=pixel, headers=headers, json=pixel_yesterday_data)
# print(response.text)

# --- Modify an existing pixel in the graph ------------------------------------- #

pixel_to_modify = f"{pixel}/{yesterday.strftime('%Y%m%d')}"

pixel_data_update = {
    "quantity": "0.5"
}

# response = requests.put(url=pixel_to_modify, headers=headers, json=pixel_data_update)
# print(response.text)

# --- Delete a pixel in the graph ----------------------------------------------- #

pixel_to_delete = f"{pixel}/{today.strftime('%Y%m%d')}"

response = requests.delete(url=pixel_to_delete, headers=headers)
print(response.text)

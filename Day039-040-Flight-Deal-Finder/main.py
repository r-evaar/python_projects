import os
from api_management import APIManager
from twilio.rest import Client
from utils import planning_query, to_msg
import pandas as pd

KIWI_KEY = os.environ.get('KIWI_KEY')
SHEETY_KEY = os.environ.get('SHEETY_KEY')
TWILIO_KEY = os.environ.get('TWILIO_KEY')
SHEETY_ENDPOINT = 'https://api.sheety.co/6dc91b93879974c3bd107a05a54a6a9d/flightDeals/prices'
KIWI_ENDPOINT = 'https://api.tequila.kiwi.com/v2/search'
TWILIO_SID ='AC2c602693cda98c15c6419c013bde3353'
HOME = "AUH"
SENDER = "+15855522877"
RECIPIENT = "+971521240215"

if __name__ == "__main__":
    data_manager = APIManager(ep=SHEETY_ENDPOINT, key=SHEETY_KEY, key_name='Authorization')
    planner = APIManager(ep=KIWI_ENDPOINT, key=KIWI_KEY, simulate=False)
    notifier = Client(TWILIO_SID, TWILIO_KEY)

    travel_data = data_manager.get()
    for query in planning_query(travel_data, HOME):
        best_tickets = planner.get(query=query)
        try:
            df = pd.DataFrame(data=best_tickets['data'])
            best_ticket = df.loc[df['price'] == df['price'].min()].iloc[0].squeeze()
        except KeyError:
            continue

        msg = to_msg(best_ticket)
        # print(msg)
        print(notifier.messages.create(from_=SENDER, body=msg, to=RECIPIENT).sid)



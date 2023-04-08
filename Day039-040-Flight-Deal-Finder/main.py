from api_management import APIManager
from twilio.rest import Client
from utils import planning_query, to_msg, send_emails
from ui import FlightClubApp
from config import *
import pandas as pd

if __name__ == "__main__":
    app = FlightClubApp()
    data_manager = APIManager(ep=SHEETY_ENDPOINT+'prices', key=SHEETY_KEY, key_name='Authorization')
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
        # print(notifier.messages.create(from_=SENDER, body=msg, to=RECIPIENT).sid)
        send_emails(app.user_manager, msg)




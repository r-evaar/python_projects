from datetime import datetime, timedelta

def planning_query(data, home):
    today = datetime.today()

    return [{
        "fly_from": home,
        "fly_to": item['iataCode'],
        "date_from": today.strftime("%d/%m/%Y"),
        "date_to": (today+timedelta(days=6*30)).strftime("%d/%m/%Y"),
        "curr": "USD",
        "price_to": item["lowestPrice"]
    } for item in data["prices"]]

def to_msg(s):
    return f"Low price alert!"\
           f"\n\nOnly ${s['price']} to fly"\
           f" from {s['cityFrom']}-{s['cityCodeFrom']}"\
           f" to {s['cityTo']}-{s['cityCodeTo']}"\
           f" from{s['utc_departure'].split('T')[0]}"\
           f" to {s['utc_arrival'].split('T')[0]} UTC."

import os
from config import *
from utils import get_api_data, get_prev_two_days
from html import unescape
from twilio.rest import Client

def monitor_stocks():
    params = {
        'apikey': os.environ.get('AVS_API_KEY'),
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': STOCK
    }

    data = get_api_data(AVS_API, params)['Time Series (Daily)']
    yesterday, before_yesterday = get_prev_two_days()

    close_i = float(data[before_yesterday]['4. close'])
    close_f = float(data[yesterday]['4. close'])

    return close_f/close_i - 1

def get_news():
    params = {
        'apiKey': os.environ.get('NEWS_API_KEY'),
        'q': COMPANY_NAME,
        'pageSize': 3
    }

    data = get_api_data(NEWS_API, params)

    if data['status'] == 'error':
        return False, (data['code'], data['message'])

    if data['totalResults'] == 0:
        return False, ('Warning:', 'No Stories were found')

    articles = data['articles']

    return True, [
        {
            'Headline': unescape(article['title']),
            'Brief': unescape(article['description']),
            'URL': article['url']
        }
        for article in articles
    ]

def send_sms(value, articles):
    symbol = '🔺' if value > 0 else '🔻'
    for article in articles:
        msg = f"{STOCK}: {symbol}{abs(value)*100:.2f}%" \
              f"\nHeadline: {article['Headline']}" \
              f"\nBrief: {article['Brief']}" \
              f"\n\nRead more at: {article['URL']}"

        sid = os.environ.get('TWILIO_SID')
        key = os.environ.get('TWILIO_KEY')
        client = Client(sid, key)

        sms = client.messages.create(from_=SENDER, body=msg, to=RECIPIENT)
        print(sms.status)


if __name__ == '__main__':
    stock_update = monitor_stocks()
    if abs(stock_update) > STOCK_THRESH:
        success, response = get_news()
        if success:
            send_sms(stock_update, response)
        else:
            print(response[0], response[1])

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday
# then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description
# to your phone number.


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge 
funds and prominent investors are required to file by the SEC The 13F 
filings show the funds' and investors' portfolio positions as of March 
31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge 
funds and prominent investors are required to file by the SEC The 13F 
filings show the funds' and investors' portfolio positions as of March 
31st, near the height of the coronavirus market crash.
"""


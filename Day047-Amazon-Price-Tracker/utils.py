import requests
import json
import os
import smtplib
from bs4 import BeautifulSoup
def get_price(item):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0',
        'Accept-Language': 'en-US'
    }

    response = requests.get(url=item, headers=headers)
    response.raise_for_status()

    # Manually confirm the item is returned, and not a captcha
    with open('test.html', 'w') as f:
        json.dump(response.text, f, indent=4)

    soup = BeautifulSoup(response.text, 'lxml')

    try:
        whole, frac, currency = [soup.select_one(f"#corePriceDisplay_desktop_feature_div .a-price-{i}").text
                                 for i in ['whole', 'fraction', 'symbol']]
    except AttributeError:
        raise Exception("Could not connect properly to the product's website")

    price = {
        'value': float(whole.replace(',', '') + frac),
        'currency': currency
    }

    return price

def send_email(email, price, item=None, link=None):

    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        usr, pas = os.environ.get('SENDER'), os.environ.get('SENDER_KEY')
        # print(f"Username={usr}\nPassword={pas}")

        connection.starttls()
        connection.login(
            user=usr,
            password=pas
        )

        msg = "Subject:Item Price Notification" \
              "\n\n" \
              f"{item if item else 'Product'} is available at " \
              f"{price['value']} {price['currency']}." \
              "\n" \
              f"{'Link: '+link if link else ''}"

        connection.sendmail(
            from_addr=usr,
            to_addrs=email,
            msg=msg
        )

        print(f'Email Sent to {email}.')

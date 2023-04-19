import os
from utils import get_price, send_email

PRODUCT = 'https://www.amazon.ae/ASUS-Gaming-GeForce-Graphics-DisplayPort/dp/B0BLGHRCLX/ref=sr_1_1'
TARGET_NAME = 'Asus TUF RTX 4080'
TARGET_PRICE = 4800
EMAIL = os.environ.get('PERSONAL_EMAIL')

if __name__ == '__main__':

    price = get_price(PRODUCT)

    if price['value'] < TARGET_PRICE:
        send_email(EMAIL, price, item=TARGET_NAME, link=PRODUCT)
    else:
        print(f"Price ({price['currency']}) criteria ({TARGET_PRICE}) not met ({price['value']}).")


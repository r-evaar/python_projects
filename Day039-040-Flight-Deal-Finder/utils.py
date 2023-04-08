import tkinter as tk
import smtplib
from PIL import Image, ImageTk
from datetime import datetime, timedelta
from config import *

def button(ratio=1, **kw):

    if 'img_file' in kw.keys():
        filename_1 = kw['img_file']['release']
        filename_2 = kw['img_file']['press']
        del kw['img_file']
        add_img = True
    else:
        add_img = False

    btn = tk.Button(**kw)

    if add_img:
        img_1 = Image.open(filename_1)
        img_2 = Image.open(filename_2)
        cw, ch, r = img_1.width, img_1.height, ratio
        w = int(cw * r)
        h = int(ch * w / cw)
        img_1 = ImageTk.PhotoImage(img_1.resize((w, h), Image.BICUBIC))
        img_2 = ImageTk.PhotoImage(img_2.resize((w, h), Image.BICUBIC))
        btn.configure(image=img_1, relief='flat', borderwidth=0, takefocus=0, width=w, height=h)
        btn.bind('<ButtonRelease-1>', lambda _: btn.configure(image=img_1))
        btn.bind('<Button-1>', lambda _: btn.configure(image=img_2))

        return btn, img_1, img_2

    return btn

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

def send_emails(manager, msg):
    responses = manager.get()['users']
    for response in responses:
        email = f"Subject: Flight Offer\n\n"\
                f"Hi, {response['firstName']}! "\
                + msg
        email = email.encode('utf8')
        try:
            with smtplib.SMTP(SENDER_SERVER, PORT) as connection:
                connection.starttls()
                connection.login(user=GMAIL_SENDER['email'], password=GMAIL_SENDER['pass'])
                connection.sendmail(from_addr=GMAIL_SENDER['email'], to_addrs=response['email'], msg=email)
        except Exception as e:
            print(f"Failed to send email to {response['email']}.")
            print(e)
        else:
            print(f"Email sent to {response['email']}.")


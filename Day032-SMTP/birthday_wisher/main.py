import os
import smtplib
import datetime as dt
import pandas as pd
from random import choice

SMTP_SERVER, PORT = 'smtp.gmail.com', 587
SENDER_U, SENDER_P = 'evaar.test@gmail.com', 'woxkwkdotbuswrkr'
DATA_FILE = './birthdays.csv'

def letter():
    files = os.walk('./letter_templates/').__next__()
    with open(files[0]+choice(files[2])) as f:
        return f.read()

def check_recipients():
    df = pd.read_csv(DATA_FILE)
    dates = [dt.datetime(year=i[0], month=i[1], day=i[2]) for _, i in df[['year', 'month', 'day']].iterrows()]
    date_only = lambda date: date.__str__().split(' ')[0]
    now = date_only(dt.datetime.now())
    return [df.iloc[i] for i, date in enumerate(dates) if now == date_only(date)]

def birthday_msg(person):
    template = letter()
    return template.replace('[NAME]', person['name'])

def send_mail(user, mail):
    with smtplib.SMTP(SMTP_SERVER, PORT) as connection:
        connection.starttls()
        connection.login(user=SENDER_U, password=SENDER_P)
        connection.sendmail(from_addr=SENDER_U, to_addrs=user['email'], msg=mail)

if __name__ == '__main__':
    recipients = check_recipients()
    if recipients:
        for recipient in recipients:
            body = birthday_msg(recipient)
            subject = 'Subject:Happy Birthday!\n\n'
            send_mail(recipient, subject+body)

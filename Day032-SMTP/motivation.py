import smtplib
import datetime as dt
from random import choice

now = dt.datetime.now()
days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

def motivate():
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user='evaar.test@gmail.com', password='woxkwkdotbuswrkr')

        with open('quotes.txt', 'r') as f:
            lines = f.readlines()

        header = "Subject:It's a Great Day!\n\n"
        msg = choice(lines)
        connection.sendmail(from_addr='evaar.test@gmail.com', to_addrs='evaar.test@outlook.com', msg=header+msg)

if days[now.weekday()] == 'FRI':
    motivate()

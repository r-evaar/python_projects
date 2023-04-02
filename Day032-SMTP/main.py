import smtplib

SENDER_SERVER = "smtp.gmail.com"
RECIPIENT_SERVER = "smtp.office365.com"
GMAIL_USER = {'email': 'evaar.test@gmail.com', 'pass': 'woxkwkdotbuswrkr'}
OUTLOOK_USER = {'email': 'evaar.test@outlook.com', 'pass': 'KJEG4O"hIEHH'}

SENDER_PORT = 587

with smtplib.SMTP(SENDER_SERVER, SENDER_PORT) as connection:  # to avoid: connection.close()

    connection.starttls()  # Encrypts the rest of the SMTP session, securing the email data traffic
    connection.login(user=GMAIL_USER['email'], password=GMAIL_USER['pass'])

    msg = '''Subject:Test-2
    
    [Title]
    
    Test-2
    
    [end]
    '''

    connection.sendmail(from_addr=GMAIL_USER['email'], to_addrs=OUTLOOK_USER['email'], msg=msg)


import os
import sys
#sys.path.append("/users/gustavomarquez/Desktop/rays_updates")

from dotenv import load_dotenv

from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure

def send_sms(message,phone_var):
    load_dotenv(dotenv_path=sys.path[-1]+'/twilio.env')

    try:
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
    except:
        load_dotenv(dotenv_path=sys.path[-2]+'/twilio.env')
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
                
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body= message,
                         from_=os.environ['TWILIO_PHONE_NUMBER'],
                         to=os.environ[phone_var]
                     )

    return message.sid

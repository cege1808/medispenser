from twilio.rest import Client
from decouple import config

TWILIO_ACCOUNT = config('TWILIO_ACCOUNT')
TWILIO_TOKEN = config('TWILIO_TOKEN')
TWILIO_TO = config('TWILIO_TO')
TWILIO_FROM = config('TWILIO_FROM')

if TWILIO_ACCOUNT and TWILIO_TOKEN and TWILIO_TO and TWILIO_FROM:
  client = Client(TWILIO_ACCOUNT, TWILIO_TOKEN)
  text_body = "\nHello {caretaker_name}, \n{client_name} has taken their medication".format(caretaker_name='Jeeves', client_name="Clarissa")
  message = client.messages.create(to=TWILIO_TO, from_=TWILIO_FROM, body=text_body)
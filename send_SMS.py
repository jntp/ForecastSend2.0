# send_SMS.py allows the user to make API calls, as in send the forecast to subscribers
import os
from twilio.rest import Client

# Load credentials from environmental variables
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

# Make API Call
class MakeCalls:
  # Sends forecasts to selected subscribers
  def makeCall(self, forecast, selectedNumbers, selectedNames):
    for index, number in enumerate(selectedNumbers):
      message = client.messages \
        .create(
          body = forecast,
          from_ = '+17148315677',
          to = number
        )
      
      print(message.sid) 
      print("Forecast sent to " + selectedNames[index] + " @ " + number + "\n")

# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'XXXX'
auth_token = 'XXXX'
client = Client(account_sid, auth_token)

message = client.messages \
  .create(
    body="DO IT BABY STICK IT BABY MOVE IT BABY LICK IT BABY SUCK UP ON THAT CLIT UNTIL THAT PUSSY GOT A HICKEY, BABY",
    from_='+17148315677',
    to='+17143996939'
  )

print(message.sid)

# Should print character count, preview, and who the message got sent to

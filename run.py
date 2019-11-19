from flask import Flask
app = Flask(__name__)

@app.route("/sms")
def hello():
  return "DO IT BABY STICK IT BABY MOVE IT BABY SUCK UP ON THAT CLIT UNTIL THAT PUSSY GOT A HICKEY, BABY"

if __name__ == "__main__":
  app.run(debug = True)

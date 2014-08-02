from flask import Flask, request, redirect, render_template
import twilio.twiml
import datetime, os, requests, json

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    """ Show off the texts that have been sent today."""

    messages = []
    auth = (os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
    r = requests.get("http://api.twilio.com/2010-04-01/Accounts/"+os.environ.get('TWILIO_ACCOUNT_SID')+"/Messages.json?DateSent>="+str(datetime.date.today()), auth=auth)
    r = r.json()
    for message in r['messages']:
        messages.append(message['body'])
    return render_template("index.html", messages=messages)

@app.route("/incoming", methods=['GET', 'POST'])
def incoming():
    """Respond to incoming calls with a simple text message."""

    resp = twilio.twiml.Response()
    resp.message("Isn't that cute.")
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

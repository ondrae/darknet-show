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
        if message['direction'] == 'inbound':
            messages.append(message['body'])
    return render_template("index.html", messages=messages)

@app.route("/incoming", methods=['POST'])
def incoming():
    """Respond to incoming calls with a simple text message."""

    resp = twilio.twiml.Response()
    resp.message("You can trust me.")
    return str(resp)

@app.route("/message", methods=["GET", "POST"])
def message():
    if request.method == "POST":
        auth = (os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
        r = requests.get("http://api.twilio.com/2010-04-01/Accounts/"+os.environ.get('TWILIO_ACCOUNT_SID')+"/Messages.json?DateSent>="+str(datetime.date.today()), auth=auth)
        r = r.json()
        for message in r['messages']:
            if message['direction'] == 'inbound':
                msg_dict = {}
            	msg_dict['To'] = message['from']
            	msg_dict['From'] = '4157412078'
            	msg_dict['Body'] = request.form['message']
            	twilio_endpoint = "https://api.twilio.com/2010-04-01/Accounts/%s/SMS/Messages.json" % (os.environ.get('TWILIO_ACCOUNT_SID'))
            	r = requests.post("%s" %(twilio_endpoint), data = msg_dict, auth=(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN')))
        return "Messages blasted."

    return render_template("message.html")

if __name__ == "__main__":
    app.run(debug=True)

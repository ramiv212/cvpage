from flask import Flask,render_template,request
import json
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
recaptcha = os.environ['RECAPTCHA']

HOST = 'smtp.live.com'

import smtplib

def send_email(subject, to_addr, from_addr, body_text):
    """
    Send an email
    """
    BODY = "\r\n".join((
            "From: %s" % from_addr,
            "To: %s" % to_addr,
            "Subject: %s" % subject ,
            "",
            body_text
            ))
    server = smtplib.SMTP(HOST)
    server.sendmail(from_addr, [to_addr], BODY)
    server.quit()


@app.route("/")
def hello_world():
    return render_template('index.html',recaptcha=recaptcha)


@app.route("/api/contact", methods=['POST'])
def send_email():
    print(request.json['name'])

    json_response = {}

    if not request.json['name']:
        json_response['name_validation'] = False
    else:
        json_response['name_validation'] = True

    if not request.json['email']:
        json_response['email_validation'] = False
    else:
        json_response['email_validation'] = True

    if not request.json['message']:
        json_response['message_validation'] = False
    else:
        json_response['message_validation'] = True

    return json.dumps(json_response)

PORT = os.environ["PORT"]
app.run(debug=True,host="0.0.0.0", port=PORT)
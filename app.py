from flask import Flask,render_template,request,jsonify
import json
from dotenv import load_dotenv
import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket
import requests

load_dotenv()

app = Flask(__name__)
recaptcha = os.environ['RECAPTCHA']

HOST = 'smtp.gmail.com'

def send_email_func(name, from_addr, body_text):
    msg = MIMEMultipart()
    msg["from"] = from_addr
    msg["to"] = 'ramiv212@hotmail.com'
    msg["subject"] = f"{name} has sent you an email via ramirovaldes.com! with {from_addr}"
    msg.attach(MIMEText(body_text, 'plain'))

    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    connection = smtplib.SMTP(HOST, 587)
    connection.ehlo()
    connection.starttls(context=context)
    connection.ehlo()
    connection.login(os.environ['HOST_USERNAME'], os.environ['HOST_PASSWORD'])
    text = msg.as_string()
    sender_email = from_addr
    receiver_email = 'ramiv212@hotmail.com'
    connection.sendmail(sender_email, receiver_email, text)



@app.route("/")
def hello_world():

    print(request)

    ip_geo = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey={os.environ["GEO_API_KEY"]}&ip={request.access_route[0]}', headers={'Accept': 'application/json'})
    print(ip_geo.json())
    
    if request.remote_addr != "127.0.0.1":
        body_text = f'Somebody with the IP address {request.access_route} and {request.remote_addr} has visited your page!'

        msg = MIMEMultipart()
        msg["from"] = 'ramirovaldes.com'
        msg["to"] = 'ramiv212@hotmail.com'
        msg["subject"] = f"Somebody has checked out your CV page!"
        msg.attach(MIMEText(body_text, 'plain'))

        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        connection = smtplib.SMTP(HOST, 587)
        connection.ehlo()
        connection.starttls(context=context)
        connection.ehlo()
        connection.login(os.environ['HOST_USERNAME'], os.environ['HOST_PASSWORD'])
        text = msg.as_string()
        sender_email = 'ramiv212@gmail.com'
        receiver_email = 'ramiv212@hotmail.com'
        connection.sendmail(sender_email, receiver_email, text)

    return render_template('index.html',recaptcha=recaptcha)


@app.route("/api/contact", methods=['POST'])
def send_email():

    json_response = {}

    if not request.json['name']:
        json_response['name_validation'] = False
    else:
        json_response['name_validation'] = True

    if not request.json['email'] and request.json['email'].find("@") == -1 or request.json['email'].find(".") == -1:
        json_response['email_validation'] = False
    else:
        json_response['email_validation'] = True

    if not request.json['message']:
        json_response['message_validation'] = False
    else:
        json_response['message_validation'] = True

    if json_response['name_validation'] == True and json_response['email_validation'] == True and json_response['message_validation'] == True:
        send_email_func(request.json['name'],request.json['email'],request.json['message'])

    return json.dumps(json_response)

PORT = os.environ["PORT"]
app.run(host="0.0.0.0", port=PORT)
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

def return_remote_addr(remote_addr):
    if remote_addr:
        return remote_addr
    else:
        return "None"

def return_city(city):
    if city:
        return city
    else:
        return "None"

def return_state_prov(state_prov):
    if state_prov:
        return state_prov
    else:
        return "None"

def return_country_name(country_name):
    if country_name:
        return country_name
    else:
        return "None"

def return_organization(organization):
    if organization:
        return organization
    else:
        return "None"

def create_app(testing: bool = True):

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

        # ip_geo = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey={os.environ["GEO_API_KEY"]}&ip={request.access_route[0]}', headers={'Accept': 'application/json'}).json()
        
        # if request.remote_addr != "127.0.0.1":
        #     try:
        #         body_text = f'Somebody with the IP address {return_remote_addr(request.remote_addr)} from {return_city(ip_geo["city"])}, {return_state_prov(ip_geo["state_prov"])}, {return_country_name(ip_geo["country_name"])}, has visited your page! Organization: {return_organization(ip_geo["organization"])}'

        #         msg = MIMEMultipart()
        #         msg["from"] = 'ramirovaldes.com'
        #         msg["to"] = 'ramiv212@hotmail.com'
        #         msg["subject"] = f"Somebody has checked out your CV page!"
        #         msg.attach(MIMEText(body_text, 'plain'))

        #         context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        #         connection = smtplib.SMTP(HOST, 587)
        #         connection.ehlo()
        #         connection.starttls(context=context)
        #         connection.ehlo()
        #         connection.login(os.environ['HOST_USERNAME'], os.environ['HOST_PASSWORD'])
        #         text = msg.as_string()
        #         sender_email = 'ramiv212@gmail.com'
        #         receiver_email = 'ramiv212@hotmail.com'
        #         connection.sendmail(sender_email, receiver_email, text)
        #     except:
        #         print("Unable to send email alert!")

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

    # app.run(host="0.0.0.0", port=PORT, debug=testing)
    return app


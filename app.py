import flask
from flask import Flask, render_template, request
import requests
import json
from datetime import datetime


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    req = requests.get("https://api.exchangeratesapi.io/latest")

    data_for_euro = json.loads(req.content)

    # This project will be about TRY's currency rates
    # So we need to replace our data's base currency-EUR- with TRY
    new_key = 'EUR'
    old_key = 'TRY'
    for i in data_for_euro['rates']:
        if i == "TRY":
            data_for_euro['rates'][new_key]=data_for_euro['rates'].pop(old_key)
    data = data_for_euro

    # We need to have EUR/TRY rate for calculating other currencies rate for TRY
    eur_try_rate = data['rates']['EUR']
    usd_try_rate = data['rates']['USD']

    # The loop for calculating correct rates for TRY
    for j in data['rates']:
        if j != "EUR":
            data['rates'][j] = round(eur_try_rate/data['rates'][j], 4)

    # Splitting date data for better visuals
    year = data['date'].split("-")[0]
    month = data['date'].split("-")[1]
    day = data['date'].split("-")[2]

    data['date'] = day + "/" + month + "/" + year

    ip_address = flask.request.remote_addr


    # Splitting user agent data and writing it to a file(logging)
    user_agent = request.headers.get('User-Agent')

    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    time_date = "Date and Time: " + now.strftime("%d/%m/%Y %H:%M:%S")

    # Logging
    f = open("logs.txt", "a")
    f.write("User's IP: " + ip_address + "\n")
    f.write(time_date + "\n")
    f.write("Browser and Operating System Data as User Agent: " + user_agent + "\n" + "\n")



    return render_template("index.html", data=data)

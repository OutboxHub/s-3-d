from flask import Flask, render_template, request
from mongoengine import connect
from models import HealthCenter, IncomingPatient
from twilio.rest import *

__author__ = 'dolel'

app = Flask(__name__)
connect('med')


@app.route('/')
def index():
    return render_template("index.html")


def send_sms_message(sms_message):
    #prepare to connect to the Twilio API
    account_sid = "ACec327c1199de511a8af2082223ce3167"
    auth_token = "44aaddf4d801a619f50a5751203ff94e"
    client = TwilioRestClient(account_sid, auth_token)
    #Send message
    send_message = client.sms.messages.create(from_="+12248033229",
                                              body=sms_message,
                                              to="+256788303658")


def generate_message(health_centers, sms_message):
    for health_center in health_centers:
        sms_message += health_center.name + " in " + health_center.parish + ","
    return sms_message


def save_condition():
    incoming_health = IncomingPatient(condition_and_location=request.form['message'])
    incoming_health.save()


@app.route('/sms_message', methods=['GET', 'POST'])
def sms_message(sms_message=""):
    if request.method == "POST":
        if 'antenatal' in str(request.form['message']).lower():
            health_centers = HealthCenter.objects(level__gte=1)
            if health_centers.count() >= 0:
                sms_message = generate_message(health_centers, sms_message)
                send_sms_message(sms_message)
                save_condition()
                return sms_message

        if 'labour' or 'delivery' or 'deliver' in str(request.form['message']).lower():
            health_centers = HealthCenter.objects(level__gte=3)
            if health_centers.count() >= 0:
                sms_message = generate_message(health_centers, sms_message)
                send_sms_message(sms_message)
            save_condition()
            return render_template('index.html', message="SMS sent", health_centers_found=sms_message)

    return render_template("index.html")


@app.route('/incoming_patient')
def incoming():
    return render_template("incoming_patient.html", patients=IncomingPatient.objects())


@app.route('/add_health_center', methods=['GET', 'POST'])
def add_health_center():
    if request.method == "POST":
        health_center = HealthCenter(parish=request.form['parish'], zone=request.form['zone'],
                                     name=request.form['name'], category=request.form['category'],
                                     level=request.form['level'], status=request.form['status'],
                                     lab=request.form['lab'])
        health_center.save()
        return render_template('index.html')
    return render_template("add_health_center.html")


if __name__ == "__main__":
    app.run(debug=True)
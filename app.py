#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
from functools import wraps
from flask import Flask, render_template, request, Response, Markup
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {17: {'name': 'GPIO 23', 'state': GPIO.LOW}}

# Set each pin as an output and make it low:
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)



def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'USER' and password == 'PASSWORD'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/')
@requires_auth
def main():

    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
    
    message = Markup('<div class="alert alert-info" role="alert"><strong>Heads up!</strong> The gate is currently closed.</div>')
    # Put the pin dictionary into the template data dictionary:
    templateData = {'pins': pins, 'message': message}

    # Pass the template data into the template main.html and return it to the user
    return render_template('main.html', **templateData)


# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route('/<changePin>/<action>')
@requires_auth
def action(changePin, action):

    # Convert the pin from the URL into an integer:
    changePin = int(changePin)

    # Get the device name for the pin being changed:
    deviceName = pins[changePin]['name']

    # If the action part of the URL is "open," execute the code indented below:
    if action == 'open':
        # Set the pin high, wait 1.5s, then set low:
        print('Setting HIGH')
        GPIO.output(changePin, GPIO.HIGH)
        time.sleep(1)
        print('Setting LOW')
        GPIO.output(changePin, GPIO.LOW)
        # Save the status message to be passed into the template:
        message =  Markup('<div class="alert alert-success" role="alert"><strong>Alrighty!</strong> The gate is now opening. This page will refresh in 30 seconds.</div>')
        
    if action == 'example':
        GPIO.output(changePin, GPIO.LOW)
        message =  Markup('<div class="alert alert-danger" role="alert"><strong>Oh snap!</strong> How\'d you trigger this example?</div>')

    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

    # Along with the pin dictionary, put the message into the template data dictionary:
    templateData = {'pins': pins, 'message': message}

    return render_template('main.html', **templateData)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

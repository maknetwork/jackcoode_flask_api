import flask
import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825

app = flask.Flask(__name__)
app.config["DEBUG"] = True
Motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
motor_Status = "closed"


@app.route("/", methods=["GET"])
def home():
    global motor_Status
    return motor_Status


@app.route("/stepperRotateOpen", methods=["GET"])
def stepper_open():

    global motor_Status
    motor_Status = "opened"
    Motor1.SetMicroStep("softward", "fullstep")
    Motor1.TurnStep(Dir="forward", steps=200, stepdelay=0.005)

    Motor1.Stop()
    return motor_Status


@app.route("/stepperRotateClose", methods=["GET"])
def stepper_close():

    global motor_Status
    motor_Status = "closed"
    Motor1.SetMicroStep("softward", "fullstep")
    Motor1.TurnStep(Dir="backward", steps=200, stepdelay=0.005)

    Motor1.Stop()
    return motor_Status


app.run()

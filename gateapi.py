import flask
from pyfcm import FCMNotification
import RPi.GPIO as GPIO
import time
from DRV8825 import DRV8825

push_service = FCMNotification(
    api_key="AAAAcOFO_Jc:APA91bGDyhNcgWPEXfa4feqLoMFDpSdOvPMe4zLk2KZE5j1NSgPBSiMzwYmHAYlX7o4-6hC4sJmMIST8tSsed0hjYH31gOUVoPtDYjI8gwGNlE7H6BG2sgK0znOAvc58elkr9lZZsP7E"
)


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


@app.route("/sendNotification", methods=["GET"])
def send_notification():
    body = ""
    title = flask.request.args.get("title")
    devicetoken = flask.request.args.get("deviceToken")

    print("body is" + body)
    message_title = title
    message_body = body
    result = push_service.notify_single_device(
        registration_id=devicetoken,
        message_title=message_title,
        message_body=message_body,
    )
    print(result)
    return result


app.run(host="0.0.0.0")

import time

from adafruit_servokit import ServoKit
from enum import Enum

kit = ServoKit(channels=16)

# o servo (pan)    is 0.07 stop
# + servo (pitch)  is -0.07 stop


class Servo(Enum):
    PAN = "pan"
    PITCH = "pitch"


PAN_ERROR = 0.07
PITCH_ERROR = -0.08


def move_servo(servo_type: Servo, amount: int):
    if servo_type == Servo.PAN:
        amount = max(-1, min(1, amount + PAN_ERROR))  # Clamp between -1 and 1
        kit.continuous_servo[0].throttle = amount
    elif servo_type == Servo.PITCH:
        amount = max(-1, min(1, amount + PITCH_ERROR))  # Clamp between -1 and 1
        kit.continuous_servo[1].throttle = amount
    else:
        raise NotImplementedError("only pan and pitch rn")


move_servo(Servo.PAN, 1)
move_servo(Servo.PITCH, 1)

time.sleep(1)
move_servo(Servo.PAN, -1)
move_servo(Servo.PITCH, -1)

time.sleep(1)

move_servo(Servo.PAN, 0)
move_servo(Servo.PITCH, 0)

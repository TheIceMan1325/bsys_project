from gpiozero import Servo
import math
from time import sleep
import os

from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()
servo = Servo(17, min_pulse_width=0.8/1000, max_pulse_width=2.5/1000, pin_factory=factory)



def rotateSensor():
    servo.value = math.sin(math.radians(0))
    sleep(2)
    while True:
        for angle in range(0, 360):
            servo.value = math.sin(math.radians(angle))
            if (angle % 15 == 0):
                servoAngle = abs(90 * servo.value - 90)

            sleep(0.01)

rotateSensor()
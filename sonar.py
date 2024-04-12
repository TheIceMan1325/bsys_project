from gpiozero import Servo
import math
from time import sleep
import os

from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()
servo = Servo(17, min_pulse_width=0.8/1000, max_pulse_width=2.5/1000, pin_factory=factory)

def output(angle):
    os.system("clear")
    print("135                      90°                           45°\n")
    print("  .                        .                        .     \n")
    print("      .                    .                    .         \n")
    print("          .                .                .             \n")
    print("              .            .            .                 \n")
    print("                  .        .        .                     \n")
    print("                      .    .    .                         \n")
    print("180 . . . . . . . . . . . . . . . . . . . . . . . . . . 0°\n")
    print("\nCurrent angle: ", angle, "°\n")

def rotateSensor():
    servo.value = math.sin(math.radians(90))
    sleep(2)
    while True:
        for i in range(0, 360):
            servo.value = math.sin(math.radians(i))
            if (i % 30 == 0):
                # output(i / 2)
                print(servo.value)
            sleep(0.01)

rotateSensor()
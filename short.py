import math
from time import sleep

class Radar:
    def drawLine(angle):
        print()

    def drawObject(angle, distance):
        print()


radar = Radar


from gpiozero import DistanceSensor, Servo
from gpiozero.pins.pigpio import PiGPIOFactory

factoryServo = PiGPIOFactory()
servo = Servo(17, min_pulse_width=0.8/1000, max_pulse_width=2.5/1000, pin_factory=factoryServo)
factorySensor = PiGPIOFactory()
ultrasonic = DistanceSensor(echo=21, trigger=20, pin_factory=factorySensor)

... 

while True:
    for angle in range(0, 360):
        servo.value = math.sin(math.radians(angle))

        ...

        radar.drawLine(angle=angle)
        if (angle % 5 == 0):
            distance = ultrasonic.distance
            if (distance < 0.5):
                radar.drawObject(angle=angle, distance=distance)
        sleep(0.01)

...
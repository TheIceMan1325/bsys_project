import math
from time import sleep
import tkinter as tk
import array

from gpiozero import DistanceSensor, Servo
from gpiozero.pins.pigpio import PiGPIOFactory

root = tk.Tk()

class Radar(tk.Canvas):
    line = 0
    # 180° divided by 5° -> 36 values + 1 value for 180° 
    objects = array.array("i", (0 for i in range(0,37)))
    SPACING = 50
    width = 0
    height = 0
    centerX = 0
    centerY = 0
    radian = 0

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(bg="black", highlightthickness=0)
        Radar.width = self.winfo_reqwidth()
        Radar.height = self.winfo_reqheight()
        Radar.centerX = Radar.width / 2
        Radar.centerY = Radar.height / 2
        Radar.radian = (Radar.width - Radar.SPACING * 2) / 2

    def drawRadar(self):
        # Draw background
        self.create_arc(Radar.SPACING, Radar.SPACING, Radar.width - Radar.SPACING, Radar.height - Radar.SPACING, start=0, extent=180, outline="green", width=2)

        # Degree lines
        numLines = 8
        for i in range(1, numLines):
            angleRad = math.radians(180 / numLines * i)
            x = Radar.centerX + Radar.radian * math.cos(angleRad)
            y = Radar.centerY - Radar.radian * math.sin(angleRad)
            self.create_line(Radar.centerX, Radar.centerY, x, y, fill="green")

        # Descriptions
        self.create_text(Radar.width - 30, Radar.centerY, text="0°", fill="green")
        self.create_text(Radar.width - 90, Radar.centerY / 2 - 30, text="45°", fill="green")
        self.create_text(Radar.centerX, 30, text="90°", fill="green")
        self.create_text(90, Radar.centerY / 2 - 30, text="135°", fill="green")
        self.create_text(30, Radar.centerY, text="180°", fill="green")

        # Semicircles
        for i in range(1, 10):
            x = Radar.SPACING + i * 20
            self.create_arc(x, x, Radar.width - x, Radar.height - x, start=0, extent=180, outline="green", width=1)

    # Moving line
    def drawLine(self, angle):
        if (specificRound(angle) % 5 == 0 and Radar.objects[determineIndex(angle)] != 0):
            self.delete(Radar.objects[determineIndex(angle)])
        if (Radar.line != 0):
            self.delete(Radar.line)
        angleRad = math.radians(angle)
        x = Radar.centerX + Radar.radian * math.cos(angleRad)
        y = Radar.centerY - Radar.radian * math.sin(angleRad)
        Radar.line = self.create_line(Radar.centerX, Radar.centerY, x, y, fill="green")

    # Detected object
    def drawObject(self, angle, distance):
        distance *= Radar.radian
        x1 = Radar.centerX + distance * math.cos(math.radians(angle)) - 5
        y1 = Radar.centerY - distance * math.sin(math.radians(angle)) - 5
        x2 = x1 + 10
        y2 = y1 + 10
        Radar.objects[determineIndex(angle)] = self.create_oval(x1, y1, x2, y2, fill="green")

def determineIndex(angle) -> int:
    index = int(specificRound(angle) / 5)
    return index

def specificRound(angle) -> int:
    roundedAngle = int(math.floor(angle))
    if (roundedAngle % 5 == 0):
        return roundedAngle
    roundedAngle = int(math.ceil(angle))
    if (roundedAngle % 5 == 0):
        return roundedAngle
    return int(round(angle))

def rotateSensor():
    factoryServo = PiGPIOFactory()
    servo = Servo(17, min_pulse_width=0.8/1000, max_pulse_width=2.5/1000, pin_factory=factoryServo)  

    # Initialize sensor
    factorySensor = PiGPIOFactory()
    ultrasonic = DistanceSensor(echo=21, trigger=20, pin_factory=factorySensor)
    servo.value = math.sin(math.radians(0))
    sleep(2)

    # Rotate sensor
    while True:
        for angle in range(0, 360):
            try:
                servo.value = math.sin(math.radians(angle))
                # Delay GUI for more accuracy
                delayedValue = math.sin(math.radians(angle - 25))
                delayedAngle = abs(90 * delayedValue - 90)
                radar.drawLine(angle=delayedAngle)
                # Only draw object if in range and only every 5th degree
                if (ultrasonic.distance < 0.5 and specificRound(delayedAngle) % 5 == 0):
                    print("Winkel: ", delayedAngle, "\n")
                    print("Abstand: ", ultrasonic.distance, "\n")
                    radar.drawObject(angle=delayedAngle, distance=(ultrasonic.distance * 2))

                root.update()
                sleep(0.01)
            except tk.TclError:
                return

if __name__ == "__main__":
    root.title("Radar")
    root.geometry("500x500")

    # Initialize GUI
    radar = Radar(root, width=500, height=500)
    radar.pack(fill=tk.BOTH, expand=True)
    radar.drawRadar()
    root.update()

    rotateSensor()
    
from gpiozero import Servo
import math
from time import sleep
import tkinter as tk

from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory

class Radar(tk.Canvas):
    line = 0

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(bg="black", highlightthickness=0)

    def drawRadar(self):
        spacing = 50
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        center_x = width / 2
        center_y = height / 2

        # Draw background
        self.create_arc(spacing, spacing, width - spacing, height -spacing, start=0, extent=180, outline="green", width=2)

        # Degree lines
        num_lines = 8
        radian = (width - spacing * 2) / 2
        for i in range(1, num_lines):
            angle_rad = math.radians(180 / num_lines * i)
            x = center_x + radian * math.cos(angle_rad)
            y = center_y - radian * math.sin(angle_rad)
            self.create_line(center_x, center_y, x, y, fill="green")

        # Descriptions
        self.create_text(width - 30, center_y, text="0°", fill="green")
        self.create_text(width - 90, center_y / 2 - 30, text="45°", fill="green")
        self.create_text(center_x, 30, text="90°", fill="green")
        self.create_text(90, center_y / 2 - 30, text="135°", fill="green")
        self.create_text(30, center_y, text="180°", fill="green")

        # Semicircles
        for i in range(1, 10):
            x = spacing + i * 20
            self.create_arc(x, x, width - x, height - x, start=0, extent=180, outline="green", width=1)

    # Moving line
    def drawLine(self, angle):
        spacing = 50
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        center_x = width / 2
        center_y = height / 2
        radian = (width - spacing * 2) / 2
        if (Radar.line != 0):
            self.delete(Radar.line)
        angle_rad = math.radians(angle)
        x = center_x + radian * math.cos(angle_rad)
        y = center_y - radian * math.sin(angle_rad)
        Radar.line = self.create_line(center_x, center_y, x, y, fill="green")


root = tk.Tk()

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
                radar.drawLine(angle=(abs(90 * servo.value - 90)))
                if (ultrasonic.distance < 0.3):
                    print(ultrasonic.distance)
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
    
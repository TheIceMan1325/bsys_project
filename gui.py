import tkinter as tk
import math
from time import sleep

class Radar(tk.Canvas):
    line = 0

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(bg="black", highlightthickness=0)

    def draw_radar(self):
        spacing = 50
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        center_x = width / 2
        center_y = height / 2

        # Zeichne den Radar-Hintergrund
        self.create_arc(spacing, spacing, width - spacing, height -spacing, start=0, extent=180, outline="green", width=2)

        # Gradlinien
        num_lines = 8
        radian = (width - spacing * 2) / 2
        for i in range(1, num_lines):
            angle_rad = math.radians(180 / num_lines * i)
            x = center_x + radian * math.cos(angle_rad)
            y = center_y - radian * math.sin(angle_rad)
            self.create_line(center_x, center_y, x, y, fill="green")

        # Beschriftung
        self.create_text(width - 30, center_y, text="0°", fill="green")
        self.create_text(width - 90, center_y / 2 - 30, text="45°", fill="green")
        self.create_text(center_x, 30, text="90°", fill="green")
        self.create_text(90, center_y / 2 - 30, text="135°", fill="green")
        self.create_text(30, center_y, text="180°", fill="green")

        # Halbkreise
        for i in range(1, 10):
            x = spacing + i * 20
            self.create_arc(x, x, width - x, height - x, start=0, extent=180, outline="green", width=1)

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


def main():
    root = tk.Tk()
    root.title("Radar")
    root.geometry("500x500")

    radar = Radar(root, width=500, height=500)
    radar.pack(fill=tk.BOTH, expand=True)
    radar.draw_radar()


    while True:
        for angle in range(0, 180):
            radar.drawLine(angle=angle)
            sleep(0.01)
            root.update()
            root.update_idletasks()

if __name__ == "__main__":
    main()
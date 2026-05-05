import customtkinter as ctk
import math
import time

class AnalogClock(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = ctk.CTkCanvas(
            self,
            width=300,
            height=300,
            bg="black",
            highlightthickness=0
        )
        self.canvas.pack(expand=True)

        self.center = 150
        self.radius = 100

        self.update_clock()

    def update_clock(self):
        self.canvas.delete("all")

        # Clock circle
        self.canvas.create_oval(
            50, 50, 250, 250,
            outline="white"
        )

        now = time.localtime()
        sec = now.tm_sec
        min = now.tm_min
        hour = now.tm_hour % 12

        self.draw_hand(sec * 6, 90, "red")     # seconds
        self.draw_hand(min * 6, 70, "white")   # minutes
        self.draw_hand(hour * 30, 50, "white") # hours

        self.after(1000, self.update_clock)

    def draw_hand(self, angle, length, color):
        angle = math.radians(angle - 90)

        x = self.center + length * math.cos(angle)
        y = self.center + length * math.sin(angle)

        self.canvas.create_line(
            self.center, self.center, x, y,
            fill=color, width=2
        )

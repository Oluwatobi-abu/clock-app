import customtkinter as ctk
import time

class DigitalClock(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = ctk.CTkLabel(self, font=("Arial", 40))
        self.label.pack(expand=True)

        self.update_time()

    def update_time(self):
        self.label.configure(text=time.strftime("%H:%M:%S"))
        self.after(1000, self.update_time)

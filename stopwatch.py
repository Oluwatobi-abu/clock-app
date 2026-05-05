import customtkinter as ctk
import time


class Stopwatch(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.running = False
        self.start_time = 0
        self.elapsed = 0

        self.label = ctk.CTkLabel(
            self,
            text="00:00:00",
            font=("Consolas", 32)
        )
        self.label.pack(pady=20)

        btns = ctk.CTkFrame(self)
        btns.pack()

        ctk.CTkButton(btns, text="Start", command=self.start).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="Pause", command=self.pause).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="Reset", command=self.reset).pack(side="left", padx=5)

        self.update_display()

    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed
            self.running = True

    def pause(self):
        if self.running:
            self.elapsed = time.time() - self.start_time
            self.running = False

    def reset(self):
        self.running = False
        self.elapsed = 0
        self.label.configure(text="00:00:00")

    def update_display(self):
        if self.running:
            self.elapsed = time.time() - self.start_time

        hrs = int(self.elapsed // 3600)
        mins = int((self.elapsed % 3600) // 60)
        secs = int(self.elapsed % 60)
        milliseconds = int((self.elapsed % 1) * 100)

        self.label.configure(text=f"{hrs:02}:{mins:02}:{secs:02}.{milliseconds:02}")
        self.after(200, self.update_display)

import customtkinter as ctk
import time
import pygame
from pathlib import Path

pygame.mixer.init()

# 🔊 Absolute path to alarm.wav
SOUND_FILE = Path(__file__).parent / "alarm.wav"


class Timer(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.running = False
        self.paused = False
        self.end_time = None
        self.remaining = 0
        self.alarm_playing = False

        # -------- INPUT --------
        self.entry = ctk.CTkEntry(
            self,
            placeholder_text="Minutes (e.g. 1 or 0.5)",
            width=180
        )
        self.entry.pack(pady=10)

        # -------- DISPLAY --------
        self.label = ctk.CTkLabel(
            self,
            text="00:00",
            font=("Consolas", 32)
        )
        self.label.pack(pady=10)

        # -------- BUTTONS --------
        btns = ctk.CTkFrame(self)
        btns.pack(pady=5)

        self.start_btn = ctk.CTkButton(btns, text="Start", command=self.start)
        self.start_btn.pack(side="left", padx=5)

        self.pause_btn = ctk.CTkButton(btns, text="Pause", command=self.pause)
        self.pause_btn.pack(side="left", padx=5)

        self.reset_btn = ctk.CTkButton(btns, text="Reset", command=self.reset)
        self.reset_btn.pack(side="left", padx=5)

        # -------- LOOP --------
        self.after(200, self.update_timer)

    # ==================================================
    # TIMER CONTROLS
    # ==================================================

    def start(self):
        # Resume if paused
        if self.paused and self.remaining > 0:
            self.end_time = time.time() + self.remaining
            self.running = True
            self.paused = False
            self.pause_btn.configure(text="Pause")
            return

        # Fresh start
        try:
            minutes = float(self.entry.get())
            if minutes <= 0:
                return

            self.remaining = int(minutes * 60)
            self.end_time = time.time() + self.remaining
            self.running = True
            self.paused = False
            self.alarm_playing = False
            pygame.mixer.music.stop()
            self.pause_btn.configure(text="Pause")

        except ValueError:
            pass

    def pause(self):
        if not self.running:
            return

        # Pause
        self.remaining = max(0, int(self.end_time - time.time()))
        self.running = False
        self.paused = True
        self.pause_btn.configure(text="Resume")

    def reset(self):
        self.running = False
        self.paused = False
        self.end_time = None
        self.remaining = 0
        self.alarm_playing = False
        pygame.mixer.music.stop()
        self.label.configure(text="00:00")
        self.pause_btn.configure(text="Pause")

    # ==================================================
    # TIMER LOOP
    # ==================================================

    def update_timer(self):
        try:
            if self.running and self.end_time:
                self.remaining = int(self.end_time - time.time())

                if self.remaining <= 0:
                    self.running = False
                    self.remaining = 0
                    self.label.configure(text="00:00")
                    self.play_sound()
                else:
                    mins = self.remaining // 60
                    secs = self.remaining % 60
                    self.label.configure(text=f"{mins:02}:{secs:02}")

        except Exception as e:
            print("Timer error:", e)

        self.after(200, self.update_timer)

    # ==================================================
    # SOUND
    # ==================================================

    def play_sound(self):
        if self.alarm_playing:
            return

        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(str(SOUND_FILE))
            pygame.mixer.music.play(-1)
            self.alarm_playing = True
        except Exception as e:
            print("Sound error:", e)


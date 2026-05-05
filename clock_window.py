import customtkinter as ctk
from clock_app.digital_clock import DigitalClock
from clock_app.analog_clock import AnalogClock
from clock_app.alarm import AlarmManager
from clock_app.stopwatch import Stopwatch
from clock_app.timer import Timer

ctk.set_appearance_mode("Dark")

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class ClockApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Clock App")
        self.geometry("420x500")

        # ---------- STATE ----------
        self.mode = "clock"          # clock | stopwatch | timer
        self.is_digital = True
        self.alarm_popup_open = False
        self.after_id = None

        self.alarm_manager = AlarmManager()

        # ---------- MAIN VIEW ----------
        self.view_container = ctk.CTkFrame(self)
        self.view_container.pack(expand=True, fill="both", pady=10)

        self.clock_frame = None

        # ---------- TOGGLE BUTTON (CREATE ONCE) ----------
        self.toggle_btn = ctk.CTkButton(
            self,
            text="Switch Digital / Analog",
            command=self.switch_clock
        )

        # ---------- SHOW INITIAL VIEW ----------
        self.show_clock()

        # ---------- ALARM INPUT ----------
        self.alarm_frame = ctk.CTkFrame(self)
        self.alarm_frame.pack(pady=5)

        self.alarm_entry = ctk.CTkEntry(
            self.alarm_frame,
            placeholder_text="HH:MM",
            width=80
        )
        self.alarm_entry.pack(side="left", padx=5)

        ctk.CTkButton(
            self.alarm_frame,
            text="Add Alarm",
            command=self.add_alarm
        ).pack(side="left", padx=5)

        # ---------- REPEAT DAYS ----------
        days_frame = ctk.CTkFrame(self)
        days_frame.pack(pady=5)

        self.day_vars = {}
        for day in DAYS:
            var = ctk.BooleanVar()
            self.day_vars[day] = var
            ctk.CTkCheckBox(days_frame, text=day, variable=var).pack(side="left", padx=2)

        # ---------- ALARM LIST ----------
        self.alarm_list = ctk.CTkScrollableFrame(self, height=120)
        self.alarm_list.pack(fill="x", padx=10, pady=5)

        self.refresh_alarm_list()

        # ---------- MODE BUTTONS ----------
        controls = ctk.CTkFrame(self)
        controls.pack(pady=10)

        ctk.CTkButton(
            controls, text="Clock",
            command=lambda: self.set_mode("clock")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            controls, text="Stopwatch",
            command=lambda: self.set_mode("stopwatch")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            controls, text="Timer",
            command=lambda: self.set_mode("timer")
        ).pack(side="left", padx=5)

        # ---------- ALARM LOOP ----------
        self.start_alarm_check()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # ==================================================
    # MODES
    # ==================================================

    def set_mode(self, mode):
        self.mode = mode

        # Safety net ✔
        if hasattr(self, "toggle_btn"):
            if mode == "clock":
                self.toggle_btn.pack(pady=5)
            else:
                self.toggle_btn.pack_forget()

        self.show_clock()

    def show_clock(self):
        if self.clock_frame:
            self.clock_frame.destroy()

        if self.mode == "clock":
            self.clock_frame = (
                DigitalClock(self.view_container)
                if self.is_digital
                else AnalogClock(self.view_container)
            )

        elif self.mode == "stopwatch":
            self.clock_frame = Stopwatch(self.view_container)

        elif self.mode == "timer":
            self.clock_frame = Timer(self.view_container)

        self.clock_frame.pack(expand=True, fill="both")

    def switch_clock(self):
        self.is_digital = not self.is_digital
        self.show_clock()

    # ==================================================
    # ALARMS
    # ==================================================

    def add_alarm(self):
        time_str = self.alarm_entry.get().strip()
        repeat_days = [d for d, v in self.day_vars.items() if v.get()]

        if len(time_str) == 5 and time_str[2] == ":":
            self.alarm_manager.add_alarm(time_str, repeat_days)
            self.refresh_alarm_list()

    def refresh_alarm_list(self):
        for w in self.alarm_list.winfo_children():
            w.destroy()

        for alarm in self.alarm_manager.alarms:
            row = ctk.CTkFrame(self.alarm_list)
            row.pack(fill="x", pady=2, padx=5)

            ctk.CTkLabel(
                row,
                text=f"{alarm.alarm_time}  {' '.join(alarm.repeat_days) or 'Once'}"
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                row,
                text="❌",
                width=30,
                command=lambda a=alarm: self.remove_alarm(a)
            ).pack(side="right", padx=5)

    def remove_alarm(self, alarm):
        self.alarm_manager.remove_alarm(alarm)
        self.refresh_alarm_list()

    def start_alarm_check(self):
        alarm = self.alarm_manager.check_alarms()

        if alarm and not self.alarm_popup_open:
            self.alarm_popup_open = True
            self.show_alarm_popup(alarm)

        for a in self.alarm_manager.alarms:
            if getattr(a, "ringing", False):
                a.increase_volume()

        self.after_id = self.after(1000, self.start_alarm_check)

    def show_alarm_popup(self, alarm):
        popup = ctk.CTkToplevel(self)
        popup.title("⏰ Alarm")
        popup.geometry("260x180")
        popup.grab_set()

        ctk.CTkLabel(
            popup,
            text=f"Alarm {alarm.alarm_time}",
            font=("Consolas", 20)
        ).pack(pady=15)

        def stop_alarm():
            alarm.stop()
            self.alarm_popup_open = False
            popup.destroy()

        def snooze():
            alarm.snooze()
            self.alarm_popup_open = False
            popup.destroy()

        ctk.CTkButton(popup, text="🛑 Stop", command=stop_alarm).pack(pady=5)
        ctk.CTkButton(popup, text="😴 Snooze", command=snooze).pack(pady=5)

        popup.protocol("WM_DELETE_WINDOW", stop_alarm)

    # ==================================================
    # EXIT
    # ==================================================

    def on_closing(self):
        if self.after_id:
            self.after_cancel(self.after_id)
        self.destroy()

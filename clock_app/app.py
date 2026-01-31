from clock_app.clock_window import ClockApp

def main():
    app = ClockApp()
    app.mainloop()

if __name__ == "__main__":
    main()

def set_alarm(self):
    alarm_time = self.alarm_entry.get()
    if alarm_time:
        self.alarm.set_alarm(alarm_time)

def check_alarm(self):
    self.alarm.check()
    self.after(1000, self.check_alarm)
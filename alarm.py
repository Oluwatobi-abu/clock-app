import json
import pygame
from datetime import datetime, timedelta
from pathlib import Path

pygame.mixer.init()

SOUND_FILE = Path(__file__).parent / "alarm.wav"
ALARM_FILE = Path(__file__).parent / "alarms.json"

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


# ==================================================
# ALARM
# ==================================================
class Alarm:
    def __init__(self, alarm_time, repeat_days=None):
        self.alarm_time = alarm_time              # "HH:MM"
        self.repeat_days = repeat_days or []
        self.ringing = False

        self.snooze_until = None
        self.snooze_minutes = 0

        self.volume = 0.3
        self.last_trigger_date = None   # 🔑 prevents infinite looping

    # --------------------------
    # RING
    # --------------------------
    def ring(self):
        if self.ringing:
            return

        if SOUND_FILE.exists():
            pygame.mixer.music.load(str(SOUND_FILE))
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)

        self.ringing = True
        self.last_trigger_date = datetime.now().date()

    # --------------------------
    # STOP
    # --------------------------
    def stop(self):
        pygame.mixer.music.stop()
        self.ringing = False
        self.snooze_until = None
        self.snooze_minutes = 0

    # --------------------------
    # SNOOZE (5 → 10 → 15)
    # --------------------------
    def snooze(self):
        self.stop()

        self.snooze_minutes = min(15, self.snooze_minutes + 5 or 5)
        self.snooze_until = datetime.now() + timedelta(minutes=self.snooze_minutes)

    # --------------------------
    # SHOULD RING?
    # --------------------------
    def should_ring(self):
        now = datetime.now()

        # Snooze check
        if self.snooze_until:
            return now >= self.snooze_until

        # Prevent re-trigger same day
        if self.last_trigger_date == now.date():
            return False

        # Time match
        return now.strftime("%H:%M") == self.alarm_time

    # --------------------------
    # GRADUAL VOLUME
    # --------------------------
    def increase_volume(self):
        if self.ringing and self.volume < 1.0:
            self.volume = min(1.0, self.volume + 0.05)
            pygame.mixer.music.set_volume(self.volume)

    # --------------------------
    # SERIALIZATION
    # --------------------------
    def to_dict(self):
        return {
            "alarm_time": self.alarm_time,
            "repeat_days": self.repeat_days,
        }

    @staticmethod
    def from_dict(data):
        return Alarm(
            alarm_time=data["alarm_time"],
            repeat_days=data.get("repeat_days", [])
        )


# ==================================================
# ALARM MANAGER
# ==================================================
class AlarmManager:
    def __init__(self):
        self.alarms = []
        self.load()

    def add_alarm(self, time_str, repeat_days=None):
        self.alarms.append(Alarm(time_str, repeat_days))
        self.save()

    def remove_alarm(self, alarm):
        if alarm in self.alarms:
            alarm.stop()
            self.alarms.remove(alarm)
            self.save()

    def check_alarms(self):
        for alarm in self.alarms:
            if alarm.should_ring():
                alarm.ring()
                return alarm
        return None

    # --------------------------
    # PERSISTENCE
    # --------------------------
    def save(self):
        with open(ALARM_FILE, "w") as f:
            json.dump([a.to_dict() for a in self.alarms], f, indent=4)

    def load(self):
        if not ALARM_FILE.exists():
            self.alarms = []
            return

        try:
            with open(ALARM_FILE, "r") as f:
                data = json.load(f)

            if isinstance(data, list):
                self.alarms = [Alarm.from_dict(a) for a in data]
            else:
                self.alarms = []

        except (json.JSONDecodeError, IOError) as e:
            print("⚠ alarms.json corrupted, resetting:", e)
            self.alarms = []
            self.save()


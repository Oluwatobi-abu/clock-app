⏰ Clock App (Python)

A simple and beautiful desktop clock application built with Python and CustomTkinter.

It includes:

🕒 Digital & Analog Clock

⏱️ Stopwatch (with milliseconds)

⏲️ Countdown Timer

🔔 Alarm with snooze (5 → 10 → 15 minutes)

🔊 Sound alerts using Pygame


🚀 Features

Switch between Digital and Analog clock

Multiple alarms with repeat days

Smart snooze system

Pause / Resume timer

Desktop-friendly UI

Packaged as a Windows .exe


🛠️ Built With

Python 3.11+

CustomTkinter

Pygame

PyInstaller


▶️ How to Run (Developer Mode)

python -m clock_app


📦 Build EXE

pyinstaller --onefile --windowed --name ClockApp \
--add-data "clock_app/alarm.wav;clock_app" \
--add-data "clock_app/alarms.json;clock_app" \
clock_app/__main__.py


📁 Project Structure

clock_app/
 ├── alarm.py
 ├── timer.py
 ├── stopwatch.py
 ├── digital_clock.py
 ├── analog_clock.py
 └── __main__.py


❤️ Author

Built with love by Abubakar Oluwatobi


📜 License

MIT License — feel free to use, learn, and improve it.
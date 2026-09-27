import tkinter as tk
from tkinter import messagebox
import random
import time

quotes = [
    "Stay focused and never give up.",
    "Discipline beats motivation.",
    "You're one session closer to your goal.",
    "Success starts with consistency.",
    "Put the controller down — pick up your future."
]

# Reminder interval in milliseconds. 1 hour by default; use 600000 for 10 minutes.
REMINDER_INTERVAL_MS = 3600000


def remind():
    quote = random.choice(quotes)
    messagebox.showinfo("⏰ RememberMe", f"Time to study!\n\n{quote}")

def start_reminder():
    button.config(state=tk.DISABLED, text="Reminders active")
    remind()
    # Repeat until the window is closed.
    root.after(REMINDER_INTERVAL_MS, start_reminder)

# Create window
root = tk.Tk()
root.title("RememberMe")
root.geometry("300x150")
root.resizable(False, False)

label = tk.Label(root, text="RememberMe Study App", font=("Arial", 14))
label.pack(pady=10)

button = tk.Button(root, text="Start Reminders", command=start_reminder, bg="#4CAF50", fg="white", font=("Arial", 12))
button.pack(pady=20)

root.mainloop()

import os
import sys

def add_to_startup():
    appdata = os.getenv('APPDATA')
    if not appdata:
        # Startup registration only applies on Windows; skip elsewhere
        # instead of crashing on a None path.
        return
    startup_path = os.path.join(appdata, 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    target_path = os.path.join(startup_path, 'rememberme.bat')
    if os.path.exists(target_path):
        # Already registered; don't rewrite the launcher on every start.
        return

    python_path = sys.executable
    script_path = os.path.abspath(__file__)

    try:
        with open(target_path, 'w') as bat_file:
            bat_file.write(f'start "" "{python_path}" "{script_path}"')
    except OSError:
        # A locked-down Startup folder must not crash the app itself.
        pass

# Call it once so it adds itself
add_to_startup()

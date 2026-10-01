import tkinter as tk
from tkinter import messagebox
import os
import random
import sys

quotes = [
    "Stay focused and never give up.",
    "Discipline beats motivation.",
    "You're one session closer to your goal.",
    "Success starts with consistency.",
    "Put the controller down — pick up your future."
]

# Reminder interval in milliseconds. 1 hour by default; use 600000 for 10 minutes.
REMINDER_INTERVAL_MS = 3600000


# Id of the pending `after` callback, or None when reminders are stopped.
reminder_job = None


def remind():
    """Show one study reminder popup with a random motivational quote."""
    quote = random.choice(quotes)
    messagebox.showinfo("⏰ RememberMe", f"Time to study!\n\n{quote}")


def schedule_reminder():
    """Show a reminder now, then queue the next one after the interval."""
    global reminder_job
    remind()
    reminder_job = root.after(REMINDER_INTERVAL_MS, schedule_reminder)


def toggle_reminders():
    """Start reminders on first click; stop them on the next click."""
    global reminder_job
    if reminder_job is not None:
        # Reminders are running: cancel the pending one and re-arm the button.
        root.after_cancel(reminder_job)
        reminder_job = None
        button.config(text="Start Reminders")
        return
    button.config(text="Stop Reminders")
    schedule_reminder()

# Create window
def add_to_startup():
    """Register the app to launch at Windows login (frozen exe or script)."""
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

    if getattr(sys, 'frozen', False):
        # Running as a PyInstaller bundle: launch the exe itself. There is no
        # Python interpreter or __file__ to point at in this mode.
        launch_command = f'start "" "{sys.executable}"'
    else:
        launch_command = f'start "" "{sys.executable}" "{os.path.abspath(__file__)}"'

    try:
        with open(target_path, 'w') as bat_file:
            bat_file.write(launch_command)
    except OSError:
        # A locked-down Startup folder must not crash the app itself.
        pass

root = tk.Tk()
root.title("RememberMe")
root.geometry("300x150")
root.resizable(False, False)

# Register at startup now, while the app is launching: calling this after
# root.mainloop() would only run it once the window closes.
add_to_startup()

label = tk.Label(root, text="RememberMe Study App", font=("Arial", 14))
label.pack(pady=10)

button = tk.Button(root, text="Start Reminders", command=toggle_reminders, bg="#4CAF50", fg="white", font=("Arial", 12))
button.pack(pady=20)

root.mainloop()

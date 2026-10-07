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

# Reminder interval in milliseconds. 1 hour by default; override it at launch
# with `python rememberme.py --interval-minutes 10`.
REMINDER_INTERVAL_MS = 3600000

# Effective interval in milliseconds, set from --interval-minutes in main().
reminder_interval_ms = REMINDER_INTERVAL_MS


# Id of the pending `after` callback, or None when reminders are stopped.
reminder_job = None


_FLAG_MISSING = object()


def _interval_flag_value(args):
    """Return the raw value given to --interval-minutes, or _FLAG_MISSING.

    Accepts both ``--interval-minutes 10`` and ``--interval-minutes=10``.
    A present-but-empty value is reported as a present flag with an invalid
    value (the caller turns it into an exit-2 error, same as a bad integer).
    """
    for index, arg in enumerate(args):
        if arg == "--interval-minutes":
            return args[index + 1] if index + 1 < len(args) else ""
        if arg.startswith("--interval-minutes="):
            return arg.partition("=")[2]
    return _FLAG_MISSING


def _parse_interval_minutes(argv):
    """Return the reminder interval in minutes from ``--interval-minutes``.

    Accepts both ``--interval-minutes 10`` and ``--interval-minutes=10``.
    Defaults to 60. Exits with status 2 on a missing or invalid value.
    """
    args = list(argv[1:])
    raw = _interval_flag_value(args)
    if raw is _FLAG_MISSING:
        return 60
    try:
        minutes = int(raw)
    except (TypeError, ValueError):
        print("error: --interval-minutes needs a positive integer number of minutes",
              file=sys.stderr)
        raise SystemExit(2)
    if minutes <= 0:
        print("error: --interval-minutes must be positive", file=sys.stderr)
        raise SystemExit(2)
    return minutes


# Index of the quote shown last, or None before the first reminder.
last_quote_index = None


def remind():
    """Show one study reminder popup with a random motivational quote.

    Never shows the same quote twice in a row.
    """
    global last_quote_index
    index = random.randrange(len(quotes))
    while len(quotes) > 1 and index == last_quote_index:
        index = random.randrange(len(quotes))
    last_quote_index = index
    messagebox.showinfo("⏰ RememberMe", f"Time to study!\n\n{quotes[index]}")


def schedule_reminder():
    """Show a reminder now, then queue the next one after the interval."""
    global reminder_job
    remind()
    reminder_job = root.after(reminder_interval_ms, schedule_reminder)


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

def add_to_startup():
    """Register the app to launch at Windows login (frozen exe or script)."""
    appdata = os.getenv('APPDATA')
    if not appdata:
        # Startup registration only applies on Windows; skip elsewhere
        # instead of crashing on a None path.
        return
    startup_path = os.path.join(appdata, 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    target_path = os.path.join(startup_path, 'rememberme.bat')
    if getattr(sys, 'frozen', False):
        # Running as a PyInstaller bundle: launch the exe itself. There is no
        # Python interpreter or __file__ to point at in this mode.
        launch_command = f'start "" "{sys.executable}"'
    else:
        launch_command = f'start "" "{sys.executable}" "{os.path.abspath(__file__)}"'

    try:
        with open(target_path) as existing:
            if existing.read() == launch_command:
                # Already registered with the current path; nothing to do.
                return
    except OSError:
        # No launcher yet (or unreadable); fall through and (re)write one.
        pass

    try:
        with open(target_path, 'w') as bat_file:
            bat_file.write(launch_command)
    except OSError:
        # A locked-down Startup folder must not crash the app itself.
        pass

def main(argv=None):
    """Build the window and start the reminder loop."""
    global root, button, reminder_interval_ms
    reminder_interval_ms = _parse_interval_minutes(argv if argv is not None else sys.argv) * 60 * 1000
    # Create window
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


if __name__ == "__main__":
    main()

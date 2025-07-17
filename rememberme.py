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

def remind():
    quote = random.choice(quotes)
    messagebox.showinfo("⏰ RememberMe", f"Time to study!\n\n{quote}")

def start_reminder():
    remind()
    # Repeat every 1 hour (3600000 ms) — you can change to 10 min (600000)
    root.after(3600000, start_reminder)

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
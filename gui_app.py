import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import time

def run_script():
    script_path = r"\Users\SmadarENB3\OneDrive\Desktop\ofek\programing\python\main_script.py"
    python_path = r"\Users\SmadarENB3\AppData\Local\Programs\Python\Python311\python.exe"
    # Update status
    status_label.config(text="Status: Download in progress...")

    subprocess.run([python_path, script_path , "DRIVE"])

    status_label.config(text="Status: Download finished.")

# Create the main window
root = tk.Tk()
root.title("Download Songs")
root.geometry("400x250")
root.configure(bg='#f5f5f5')  # Soft light gray background

# Create and configure the style
style = ttk.Style()
style.configure("TFrame", background='#f5f5f5')
style.configure("TLabel", background='#f5f5f5', font=('Arial', 12))
style.configure("TButton", padding=6, relief="flat", font=('Arial', 12))
style.configure("TProgressbar", thickness=20, background='#7d8c8d')

# Create a frame for layout
frame = ttk.Frame(root, padding="20")
frame.pack(expand=True, fill=tk.BOTH)

# Add a title label
title_label = ttk.Label(frame, text="Welcome to the Song Downloader")
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Add an instruction label
instruction_label = ttk.Label(frame, text="Click the button below to start downloading:")
instruction_label.grid(row=1, column=0, columnspan=2, pady=5)

# Create and place a button
run_button = ttk.Button(frame, text="Start Download", command=run_script)
run_button.grid(row=2, column=0, columnspan=2, pady=20)

# Add an additional label for status updates
status_label = ttk.Label(frame, text="Status: Waiting for action...")
status_label.grid(row=4, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()
import tkinter as tk
from tkinter import ttk

def get_time():
    selected_hour = hour_var.get()
    selected_minute = minute_var.get()
    print(f"Selected Time: {selected_hour:02}:{selected_minute:02}")

root = tk.Tk()
root.title("Pilih Waktu")

# Variables to store the selected hour and minute
hour_var = tk.IntVar()
minute_var = tk.IntVar()

# Create the spinbox for hours (0-23)
hour_spinbox = ttk.Spinbox(root, from_=0, to=23, textvariable=hour_var, wrap=True, width=5, font=('Helvetica', 16))
hour_spinbox.grid(row=0, column=0, padx=5, pady=5)

# Create the spinbox for minutes (0-59)
minute_spinbox = ttk.Spinbox(root, from_=0, to=59, textvariable=minute_var, wrap=True, width=5, font=('Helvetica', 16))
minute_spinbox.grid(row=0, column=1, padx=5, pady=5)

# Button to print the selected time
select_button = ttk.Button(root, text="Select Time", command=get_time)
select_button.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()

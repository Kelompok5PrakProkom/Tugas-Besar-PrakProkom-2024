import os
import csv
from tkinter import ttk
import ttkbootstrap as ttkb

def see_date():
    date = cal.entry.get()
    start_time = time_combobox.get()
    duration = duration_combobox.get()
    booking_info = f"{date} at {start_time} for {duration} hours"
    date_label.config(text=booking_info, foreground='#2a9fd6')
    save_to_csv(date, start_time, duration)

def save_to_csv(date, start_time, duration):
    file_path = 'booking_data.csv'
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Start Time", "Duration (hours)"])  # Menulis header jika file belum ada
        writer.writerow([date, start_time, duration])

root = ttkb.Window(themename="cyborg")
root.title('Calendar')

cal = ttkb.DateEntry(root, dateformat='%d/%m/%y', bootstyle="primary")
cal.pack(padx=40, pady=20)

time_label = ttk.Label(root, text="Select Time:", font=('Helvetica', 12))
time_label.pack(pady=5)

time_values = [f"{hour:02d}:00" for hour in range(8, 18)]
time_combobox = ttk.Combobox(root, values=time_values, state="readonly")
time_combobox.current(0)  # Set default time to 08:00
time_combobox.pack(padx=40, pady=20)

duration_label = ttk.Label(root, text="Select Duration (hours):", font=('Helvetica', 12))
duration_label.pack(pady=5)

duration_values = [str(i) for i in range(1, 9)]  # Durasi dari 1 hingga 9 jam
duration_combobox = ttk.Combobox(root, values=duration_values, state="readonly")
duration_combobox.current(0)  # Set default duration to 1 hour
duration_combobox.pack(padx=40, pady=20)

btn = ttkb.Button(root, text="Simpan data", bootstyle="primary-outline", command=see_date)
btn.pack(padx=40, pady=20)

date_label = ttk.Label(root, text="No date selected", font=('Helvetica', 12), foreground='#2a9fd6')
date_label.pack(padx=40, pady=20)

root.mainloop()
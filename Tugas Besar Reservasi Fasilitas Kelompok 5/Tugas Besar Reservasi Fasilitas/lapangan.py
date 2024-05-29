import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttkb
from fpdf import FPDF
from datetime import datetime
import customtkinter as ctk
from customtkinter import CTk, CTkButton, CTkToplevel, CTkLabel
from PIL import ImageTk, Image

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

class BookingApp:
    def __init__(self, root, facility_name):
        self.root = root
        self.facility_name = facility_name
        self.root.title(f"Reservasi {facility_name}")
        self.root.geometry("400x390")
        self.user_email = self.get_user_email()
        self.init_booking_section()

    def get_user_email(self):
        try:
            with open('current_user.txt', 'r') as file:
                email = file.readline().strip()
                return email
        except FileNotFoundError:
            messagebox.showerror("Error", "current_user.txt not found!")
            self.root.destroy()

    def init_booking_section(self):
        booking_frame = ttkb.Frame(self.root)
        booking_frame.pack(padx=10, pady=10, fill='x')

        cal_label = ttk.Label(booking_frame, text="Select Date:", font=('Helvetica', 12))
        cal_label.pack(pady=5)

        self.cal = ttkb.DateEntry(booking_frame, dateformat='%d/%m/%y', bootstyle="primary")
        self.cal.pack(padx=40, pady=5)
        self.cal.bind("<<DateEntrySelected>>", self.update_available_times)

        time_label = ttk.Label(booking_frame, text="Select Time:", font=('Helvetica', 12))
        time_label.pack(pady=5)

        self.time_values = [f"{hour:02d}:00" for hour in range(8, 18)]
        self.time_combobox = ttk.Combobox(booking_frame, values=self.time_values, state="readonly")
        self.time_combobox.current(0)
        self.time_combobox.pack(padx=40, pady=5)

        duration_label = ttk.Label(booking_frame, text="Select Duration (hours):", font=('Helvetica', 12))
        duration_label.pack(pady=5)

        duration_values = [str(i) for i in range(1, 9)]
        self.duration_combobox = ttk.Combobox(booking_frame, values=duration_values, state="readonly")
        self.duration_combobox.current(0)
        self.duration_combobox.pack(padx=40, pady=5)

        btn = ttkb.Button(booking_frame, text="Save Booking", bootstyle="primary-outline", command=self.see_date)
        btn.pack(padx=40, pady=10)

        self.date_label = ttk.Label(booking_frame, text="No date selected", font=('Helvetica', 12), foreground='#2a9fd6')
        self.date_label.pack(pady=5)

        name_label = ttk.Label(booking_frame, text="Name:", font=('Helvetica', 12))
        name_label.pack(pady=5)
        self.entry_name = ttk.Entry(booking_frame, font=('Helvetica', 12))
        self.entry_name.pack(padx=40, pady=5)

        email_label = ttk.Label(booking_frame, text="Email:", font=('Helvetica', 12))
        email_label.pack(pady=5)
        self.entry_email = ttk.Entry(booking_frame, font=('Helvetica', 12))
        self.entry_email.insert(0, self.user_email)
        self.entry_email.config(state='readonly')
        self.entry_email.pack(padx=40, pady=5)

        self.update_available_times()

    def see_date(self):
        date = self.cal.entry.get()
        start_time = self.time_combobox.get()
        duration = int(self.duration_combobox.get())
        if self.is_booked(date, start_time, duration):
            self.date_label.config(text=f"Slot already booked on {date} at {start_time}", foreground='red')
        else:
            booking_info = f"{date} at {start_time} for {duration} hours"
            self.date_label.config(text=booking_info, foreground='#2a9fd6')
            self.save_to_csv(date, start_time, duration)
            self.generate_invoice(date, start_time, duration)
            self.update_available_times()

    def save_to_csv(self, date, start_time, duration):
        file_path = f'{self.facility_name}_booking_data.csv'
        file_exists = os.path.isfile(file_path)

        name = self.entry_name.get()
        email = self.user_email

        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Date", "Start Time", "Duration (hours)", "Name", "Email"])
            writer.writerow([date, start_time, duration, name, email])

    def is_booked(self, date, start_time, duration):
        file_path = f'{self.facility_name}_booking_data.csv'
        if not os.path.exists(file_path):
            return False

        start_hour = int(start_time.split(":")[0])
        booked_hours = set(range(start_hour, start_hour + duration))

        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                booked_date, booked_time, booked_duration = row[:3]
                if booked_date == date:
                    booked_start_hour = int(booked_time.split(":")[0])
                    booked_end_hour = booked_start_hour + int(booked_duration)
                    if booked_hours & set(range(booked_start_hour, booked_end_hour)):
                        return True
        return False
    
    def generate_invoice(self, date, start_time, duration):
        name = self.entry_name.get()
        email = self.user_email
        if not name or not email:
            messagebox.showerror("Error", "Name and Email must be provided!")
            return

        facility = self.facility_name
        
        invoice_text = (
            f"Invoice Pemesanan Fasilitas\n"
            f"============================\n"
            f"Nama     : {name}\n"
            f"Email     : {email}\n"
            f"Fasilitas : {facility}\n"
            f"============================\n"
            f"Tanggal  : {date}\n"
            f"Waktu     : {start_time}\n"
            f"Durasi     : {duration} jam\n"
        )
        self.save_invoice(invoice_text, name, date)

    def save_invoice(self, text, name, date):
        filename = f"Invoice_{name}_{date.replace('/', '-')}.pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in text.split('\n'):
            pdf.cell(200, 10, txt=line, ln=True, align='L')
        pdf.output(filename)
        messagebox.showinfo("Invoice Generated", f"Invoice saved as {filename}")

    def update_available_times(self, event=None):
        date = self.cal.entry.get()
        unavailable_times = set()
        
        file_path = f'{self.facility_name}_booking_data.csv'
        if os.path.exists(file_path):
            with open(file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    booked_date, booked_time, booked_duration = row[:3]
                    if booked_date == date:
                        booked_start_hour = int(booked_time.split(":")[0])
                        booked_end_hour = booked_start_hour + int(booked_duration)
                        unavailable_times.update(range(booked_start_hour, booked_end_hour))
        
        updated_time_values = []
        for time in self.time_values:
            hour = int(time.split(":")[0])
            if hour in unavailable_times:
                updated_time_values.append(f"{time} (booked)")
            else:
                updated_time_values.append(time)
        
        self.time_combobox.config(values=updated_time_values)
        self.time_combobox.current(0)


def start_app():
    app = CTk()
    BookingApp(app, "Lapangan")  
    app.mainloop()

if __name__ == "__main__":
    start_app()

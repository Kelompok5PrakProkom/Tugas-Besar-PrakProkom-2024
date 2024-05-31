import os
import csv
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import customtkinter as ctk
from customtkinter import CTk, CTkButton, CTkLabel, CTkEntry, CTkComboBox
from PIL import ImageTk, Image
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

facility_name = "Working Space"

app = ctk.CTk()
app.attributes("-fullscreen", True)
app.title('Reservasi Fasilitas')


# Load background image
img1 = ImageTk.PhotoImage(Image.open("Tugas Besar Reservasi Fasilitas Kelompok 5/Tugas Besar Reservasi Fasilitas/assets/bglain.png"))
canvas = ctk.CTkCanvas(app)
canvas.pack(fill='both', expand=True)
canvas.create_image(0, 0, anchor='nw', image=img1)
# Move the background label to the back

def get_user_email():
    try:
        with open('current_user.txt', 'r') as file:
            email = file.readline().strip()
            return email
    except FileNotFoundError:
        messagebox.showerror("Error", "current_user.txt not found!")
        app.destroy()


def update_available_times(event=None):
    date = cal.get()
    unavailable_times = set()

    file_path = f'{facility_name}_booking_data.csv'
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
    for time in time_values:
        hour = int(time.split(":")[0])
        if hour in unavailable_times:
            updated_time_values.append(f"{time} (booked)")
        else:
            updated_time_values.append(time)

    time_combobox.configure(values=updated_time_values)
    time_combobox.set(updated_time_values[0])


def is_booked(date, start_time, duration):
    file_path = f'{facility_name}_booking_data.csv'
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


def save_to_csv(date, start_time, duration):
    file_path = f'{facility_name}_booking_data.csv'
    file_exists = os.path.isfile(file_path)

    name = entry_name.get()
    email = user_email

    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Start Time", "Duration (hours)", "Name", "Email"])
        writer.writerow([date, start_time, duration, name, email])


def justify_text(pdf, text, x, y, width):
    lines = text.split("\n")
    for line in lines:
        words = line.split()
        if len(words) == 0:
            pdf.ln(10)
            continue

        space_width = pdf.get_string_width(' ')
        line_width = sum(pdf.get_string_width(word) for word in words) + space_width * (len(words) - 1)

        if line_width <= width:
            pdf.set_xy(x, y)
            pdf.multi_cell(width, 10, line, align='J')
            y += 10
            continue

        output = []
        while words:
            while words and sum(pdf.get_string_width(word) for word in output + [words[0]]) + space_width * len(output) <= width:
                output.append(words.pop(0))

            if words:
                total_spaces = len(output) - 1
                if total_spaces > 0:
                    extra_space = (width - sum(pdf.get_string_width(word) for word in output)) / total_spaces
                else:
                    extra_space = 0

                for i in range(len(output) - 1):
                    output[i] += ' ' * (int(extra_space / space_width))

            pdf.set_xy(x, y)
            pdf.multi_cell(width, 10, ' '.join(output), align='J')
            y += 10
            output = []

        if output:
            pdf.set_xy(x, y)
            pdf.multi_cell(width, 10, ' '.join(output), align='J')
            y += 10


def save_invoice(text, name, date):
    filename = f"Invoice_{name}_{date.replace('/', '-')}.pdf"
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", 'B', 30)
    pdf.cell(0, 30, "UnitySpace", ln=True, align='C')

    pdf.set_font("Arial", size=12)

    text_width = 100
    text_height = 70
    page_width = 210
    border_x = (page_width - text_width) / 2
    border_y = 45

    pdf.set_draw_color(0, 0, 0)
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(border_x, border_y, text_width, text_height, 'D')

    text_x = border_x + 2
    text_y = border_y + 2
    justify_text(pdf, text, text_x, text_y, text_width - 4)

    if os.path.exists('Tugas Besar Reservasi Fasilitas/assets/logo.png'):
        logo_width = 35
        logo_x = (page_width - logo_width) / 2
        pdf.image('Tugas Besar Reservasi Fasilitas/assets/logo.png', x=logo_x, y=border_y + text_height + 10, w=logo_width)

    pdf.output(filename)
    messagebox.showinfo("Invoice Generated", f"Invoice saved as {filename}")
    return filename


def send_email_with_invoice(recipient_email, invoice_filename):
    sender_email = "kelompok5prakprokom@gmail.com"
    sender_password = "tvsh fnti qfgt eieq"

    subject = "Invoice Reservasi Working Space"
    body = "Berikut ini kami kirimkan invoice reservasi fasilitas Working Space yang telah anda pesan."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with open(invoice_filename, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f'attachment; filename={invoice_filename}',
    )
    msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        messagebox.showinfo("Email Sent", f"Invoice emailed to {recipient_email}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {str(e)}")


def see_date():
    date = cal.get()
    start_time = time_combobox.get()
    duration = int(duration_combobox.get())
    name = entry_name.get()
    email = user_email

    if is_booked(date, start_time, duration):
        date_label.configure(text=f"Slot already booked on {date} at {start_time}", text_color='red')
    elif  not name or not email :
        messagebox.showerror("Error", "Name and Email must be provided!")
        return
    else:
        booking_info = f"{date} at {start_time} for {duration} hours"
        date_label.configure(text=booking_info, text_color='#2a9fd6')
        save_to_csv(date, start_time, duration)
        invoice_filename = save_invoice(
            f"Nama     : {entry_name.get()}\n"
            f"Email     : {user_email}\n"
            f"Fasilitas : {facility_name}\n\n"
            f"Tanggal  : {date}\n"
            f"Waktu     : {start_time}\n"
            f"Durasi     : {duration} jam\n",
            entry_name.get(),
            date
        )
        send_email_with_invoice(user_email, invoice_filename)
        update_available_times()

def balikmilih():
    app.destroy()
    import book_fasilitas
    return

user_email = get_user_email()

booking_frame = ctk.CTkFrame(
    app, 
    width=600, 
    height=800,
    fg_color="#C8E2FF",
    bg_color="#FDB4B4",
    corner_radius=25
)
canvas.create_window(960,540, anchor='center', window=booking_frame)

cal_label = ctk.CTkLabel(
    app, 
    text="Reservasi", 
    font=('Rockwell', 40),
    fg_color="#C8E2FF")
canvas.create_window(960, 200, anchor='center', window=cal_label)

name_label = ctk.CTkLabel(
    app, 
    text="Name:", 
    font=('Helvetica', 24),
    fg_color="#C8E2FF")
canvas.create_window(960, 270, anchor='center', window=name_label)

entry_name = ctk.CTkEntry(
    app, 
    font=('Helvetica', 18),
    width= 200)
canvas.create_window(960, 310, anchor='center', window=entry_name)

email_label = ctk.CTkLabel(
    app, 
    text="Email:", 
    font=('Helvetica', 24),
    fg_color="#C8E2FF")
canvas.create_window(960, 360, anchor='center', window=email_label)

entry_email = ctk.CTkEntry(
    app, 
    font=('Helvetica', 18),
    width= 275)
entry_email.insert(0, user_email)
entry_email.configure(state='readonly')
canvas.create_window(960, 400, anchor='center', window=entry_email)

cal_label = ctk.CTkLabel(
    app, 
    text="Pilih Tanggal:", 
    font=('Helvetica', 24),
    fg_color="#C8E2FF")
canvas.create_window(960, 450, anchor='center', window=cal_label)

cal = DateEntry(
    app, 
    date_pattern='dd/mm/yy',
    font = ('Helvetica',14))
canvas.create_window(960, 490, anchor='center', window=cal)
cal.bind("<<DateEntrySelected>>", update_available_times)

time_label = ctk.CTkLabel(
    app, 
    text="Select Time:", 
    font=('Helvetica', 24),
    fg_color="#C8E2FF")
canvas.create_window(960, 530, anchor='center', window=time_label)

time_values = [f"{hour:02d}:00" for hour in range(8, 18)]
time_combobox = ctk.CTkComboBox(
    app, 
    values=time_values,
    font = ("Helvetica",18))
time_combobox.set(time_values[0])
canvas.create_window(960, 570, anchor='center', window=time_combobox)

duration_label = ctk.CTkLabel(
    app, 
    text="Select Duration (hours):", 
    font=('Helvetica', 24),
    fg_color="#C8E2FF")
canvas.create_window(960, 610, anchor='center', window=duration_label)

duration_values = [str(i) for i in range(1, 9)]
duration_combobox = ctk.CTkComboBox(
    app, 
    values=duration_values,
    font = ("Helvetica", 18))
duration_combobox.set(duration_values[0],)
canvas.create_window(960, 650, anchor='center', window=duration_combobox)

date_label = ctk.CTkLabel(
    app, 
    text="No date selected",
    font=('Helvetica', 18),
    text_color='#2a9fd6',
    fg_color="#C8E2FF")
canvas.create_window(960, 690, anchor='center', window=date_label)

btn = ctk.CTkButton(
    app, 
    text="Save Booking", 
    command=see_date,
    height=40,
    font = ("Helvetica",18),
    hover_color="#0C3598")
canvas.create_window(960, 730, anchor='center', window=btn)

btnout = ctk.CTkButton(
    app, 
    text="Kembali Pilih Fasilitas", 
    command=balikmilih,
    height=40,
    font = ("Helvetica",18),
    fg_color="#F80000",
    hover_color="#8D0000")
canvas.create_window(960, 900, anchor='center', window=btnout)


update_available_times()

app.mainloop()

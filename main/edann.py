import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
from PIL import Image, ImageTk
import pandas as pd
from datetime import datetime, timedelta
import csv

# Setup nama file untuk database excel
DATABASE_FILE = "booking_database.xlsx"

# Daftar fasilitas dan deskripsinya
facilities = {
    "Lapangan": "Area terbuka di lingkungan fakultas yang berfungsi sebagai pusat kegiatan akademik, olahraga, dan sosial.",
    "Ruang Multimedia": "Ruang yang disediakan untuk mendukung berbagai kegiatan berbasis teknologi dan audiovisual, seperti presentasi, konferensi video, pemutaran film, dan pembuatan konten digital.",
    "Ruang Seminar": "Ruang yang disediakan untuk mengadakan diskusi, presentasi, dan pelatihan. Dilengkapi dengan peralatan audiovisual seperti proyektor, layar, dan sistem suara.",
    "Working Space": "Ruang yang disediakan kepada mahasiswa untuk belajar, bekerja, serta berkolaborasi. Dilengkapi dengan internet lancar serta colokan listrik."
}

# Fungsi untuk membuat/menyimpan data ke database
def save_to_database(facility, date, start_time, end_time):
    try:
        df = pd.read_excel(DATABASE_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Facility", "Date", "Start Time", "End Time"])

    # Check if the slot is already booked
    if ((df['Facility'] == facility) & (df['Date'] == date) & (df['Start Time'] == start_time) & (df['End Time'] == end_time)).any():
        messagebox.showerror("Error", "Slot ini sudah terbooking!")
    elif ((df['Facility'] == facility) & (df['Date'] == date) & (df['End Time'] > start_time)).any():
        messagebox.showerror("Error", "Slot ini sudah terbooking!")
        return

    new_booking = {"Facility": facility, "Date": date, "Start Time": start_time, "End Time": end_time}
    df = df._append(new_booking, ignore_index=True)
    df.to_excel(DATABASE_FILE, index=False)
    messagebox.showinfo("Success", "Booking berhasil disimpan!")

# Fungsi untuk memproses booking waktu
def book_time(facility, date, start_time, duration):
    start_datetime = datetime.strptime(start_time, "%H:%M")
    end_datetime = start_datetime + timedelta(hours=duration)
    end_time = end_datetime.strftime("%H:%M")
    response = messagebox.askyesno("Confirm Booking", f"Apakah Anda yakin ingin memesan {facility} dari jam {start_time} hingga jam {end_time} pada tanggal {date}?")
    if response:
        save_to_database(facility, date, start_time, end_time)

# Fungsi untuk menampilkan pilihan waktu dan durasi
def show_time_duration_picker(facility, date):
    try:
        df = pd.read_excel(DATABASE_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Facility", "Date", "Start Time", "End Time"])

    booked_times = df[(df['Facility'] == facility) & (df['Date'] == date)]
    
    time_window = tk.Toplevel(root)
    time_window.title(f"Pilih Waktu dan Durasi untuk {facility} pada {date}")

    tk.Label(time_window, text="Pilih Waktu Mulai:").pack(pady=5)

    start_times = [f"{hour:02d}:00" for hour in range(9, 18)]
    available_start_times = []
    for time in start_times:
        start_datetime = datetime.strptime(time, "%H:%M")
        end_datetime = start_datetime + timedelta(hours=1)
        if not ((booked_times['Start Time'] <= time) & (booked_times['End Time'] > time)).any():
            available_start_times.append(time)

        
    time_frame = tk.Frame(time_window)
    time_frame.pack(pady=5)
    
    start_time_combobox = ttk.Combobox(time_window, values=available_start_times, width=5)
    start_time_combobox.pack(pady=5)
    if available_start_times:
        start_time_combobox.set(available_start_times[0])
    else:
        start_time_combobox.set("")

    tk.Label(time_window, text="Pilih Durasi (jam):").pack(pady=5)
    duration_spinbox = tk.Spinbox(time_window, from_=1, to=8, width=5)
    duration_spinbox.pack(pady=5)

    book_button = tk.Button(time_window, text="Book", state="disabled" if not available_start_times else "normal", command=lambda: book_time(facility, date, start_time_combobox.get(), int(duration_spinbox.get())))
    book_button.pack(pady=20)

    # Display already booked times in red
    for time in start_times:
        time_label = tk.Label(time_frame, text=time, width=8, relief=tk.SUNKEN)
        time_label.grid(row=0, column=start_times.index(time), padx=2)
        if time in available_start_times:
            time_label.bind("<Button-1>", lambda e, t=time: start_time_combobox.set(t))
            time_label.configure(bg="lightgreen")
        else:
            time_label.configure(bg="red")

# Fungsi untuk menampilkan kalender untuk memilih tanggal
def show_calendar(facility):
    calendar_window = tk.Toplevel(root)
    calendar_window.title(f"Pilih Tanggal untuk {facility}")

    cal = Calendar(calendar_window, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(pady=20)

    select_date_button = tk.Button(calendar_window, text="Select Date", command=lambda: show_time_duration_picker(facility, cal.get_date()))
    select_date_button.pack(pady=20)

# Fungsi untuk menampilkan deskripsi dan memulai booking
def show_description(facility):
    description = facilities[facility]
    response = messagebox.askokcancel(f"{facility}", description)
    if response:  # If user clicks OK, show the calendar
        show_calendar(facility)

# Setup GUI utama
root = tk.Tk()
root.title("Facility Booking System")

# Setup menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=lambda: root.quit())

label = tk.Label(root, text="Choose a Facility to Book:", font=("Helvetica", 16))
label.pack(pady=20)

# Frame untuk menampung fasilitas
frame = tk.Frame(root)
frame.pack(pady=20)

# Fungsi untuk memuat gambar
def load_image(path, size):
    img = Image.open(path)
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

# Load images for each facility
images = {
    "Lapangan": load_image("main/lapangan.jpg", (150, 150)),
    "Ruang Multimedia": load_image("main/multimedia.jpg", (150, 150)),
    "Ruang Seminar": load_image("main/seminar.jpg", (150, 150)),
    "Working Space": load_image("main/workingspace.jpg", (150, 150))
}

# Menambahkan fasilitas ke frame
for facility in facilities:
    facility_frame = tk.Frame(frame)
    facility_frame.pack(side=tk.LEFT, padx=10)

    img_label = tk.Label(facility_frame, image=images[facility])
    img_label.pack()
    img_label.bind("<Button-1>", lambda e, f=facility: show_description(f))

    facility_label = tk.Label(facility_frame, text=facility, font=("Helvetica", 12, "bold"))
    facility_label.pack(pady=5)

# Tambahkan tombol Quit
quit_button = tk.Button(root, text="Quit", command=lambda: root.quit(), font=("Helvetica", 12), bg="red", fg="white")
quit_button.pack(pady=20)

root.mainloop()


def register():
    username = register_username_entry.get()
    password = register_password_entry.get()
    email = register_email_entry.get()

    dataakun = []

    with open("main\dataakun.csv", "r") as file:
        csv_reader = csv.reader(file, delimiter=",")
        for row in csv_reader:
            if len(row) > 0:
                dataakun.append({'username': row[0], 'password': row[1],'email': row[2]})

    username_ada = False

    for akun in dataakun:
        if username == akun['username']:
            messagebox.showerror("Error", "Username sudah ada! Ganti yang lain!")
            username_ada = True
            break

    if not username_ada:  
        try:
            if "@" not in email or "." not in email:
                raise ValueError("Invalid email format. Please enter a valid email address.")

            databaru = {'username': username, 'password': password, 'email': email}

            with open("main\dataakun.csv", "a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=databaru.keys())
                writer.writerow(databaru)

            messagebox.showinfo("Success", "Berhasil Register")
            return halaman_login()

        except ValueError as e:
            messagebox.showerror("Error", f"Email is not valid: {e}")
            return halaman_reg()



def login():
    username = login_username_entry.get()
    password = login_password_entry.get()

    dataakun = []
    with open("main\dataakun.csv", "r") as file:
        csv_reader = csv.reader(file, delimiter=",")
        for row in csv_reader:
            if len(row) > 0:
                dataakun.append({'username': row[0], 'password': row[1]})

    datalogin = []
    for i in dataakun:
        if username == i['username'] and password == i['password']:
            datalogin.append(i)
            messagebox.showinfo("Success", "Berhasil Login")
            break 

    if len(datalogin) == 0:
        messagebox.showerror("Error", "Data Tidak Ditemukan")


def show_register_page():
    login_frame.destroy()
    halaman_reg()

def halaman_login():
    global login_frame
    root = tk.Tk()    
    root.title("Login")
    root.geometry('1920x1080')
    root.configure(bg="white")
    root.resizable(True, True)

    login_frame = tk.Frame(root)
    login_frame.pack(pady=20)

    login_username_label = tk.Label(login_frame, text="Username")
    login_username_label.grid(row=0, column=0, padx=(20, 0))
    global login_username_entry
    login_username_entry = tk.Entry(login_frame)
    login_username_entry.grid(row=0, column=1)

    login_password_label = tk.Label(login_frame, text="Password")
    login_password_label.grid(row=1, column=0, padx=(20, 0))
    global login_password_entry
    login_password_entry = tk.Entry(login_frame, show="*")
    login_password_entry.grid(row=1, column=1)

    login_button = tk.Button(login_frame, text="Login", command=login)
    login_button.grid(row=2, column=1, pady=(10, 0))

    register_button = tk.Button(login_frame, text="Register", command=show_register_page)
    register_button.grid(row=2, column=0, pady=(10, 0))

    root.mainloop()

def halaman_reg():
    root = tk.Tk()
    root.title("Register")
    root.geometry('1920x1080')
    root.configure(bg="white")
    root.resizable(True, True)

    register_frame = tk.Frame(root)
    register_frame.pack(pady=20)

    register_username_label = tk.Label(register_frame, text="Username")
    register_username_label.grid(row=0, column=0, padx=(20, 0))
    global register_username_entry
    register_username_entry = tk.Entry(register_frame)
    register_username_entry.grid(row=0, column=1)

    register_password_label = tk.Label(register_frame, text="Password")
    register_password_label.grid(row=1, column=0, padx=(20, 0))
    global register_password_entry
    register_password_entry = tk.Entry(register_frame, show="*")
    register_password_entry.grid(row=1, column=1)

    register_email_label = tk.Label(register_frame, text="Email")
    register_email_label.grid(row=2, column=0, padx=(20, 0))
    global register_email_entry
    register_email_entry = tk.Entry(register_frame)
    register_email_entry.grid(row=2, column=1)

    register_button = tk.Button(register_frame, text="Register", command=register)
    register_button.grid(row=3, column=1, pady=(10, 0))

    root.mainloop()

halaman_login()

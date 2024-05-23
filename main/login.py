import tkinter as tk
from tkinter import messagebox
import csv



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
            return

    if len(datalogin) == 0:
        messagebox.showerror("Error", "Data Tidak Ditemukan")


def show_register_page():
    login_frame.destroy()
    halaman_reg()

def halaman_login():
    global root
    global login_frame
    root = tk.Tk()    
    root.title("Login")
    root.geometry('1920x1080')
    root.configure(bg="white")
    root.resizable(True, True)

    login_frame = tk.Frame(root, width= 400, height=600)
    login_frame.place(x=1440, y=540)

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
    register_frame.place(x=100, y=100)
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

import tkinter
import customtkinter
import pandas as pd
import os
from PIL import ImageTk,Image
from tkinter import messagebox
from customtkinter import CTkButton, CTkImage


customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green


def register_user():
    email = entry1.get()
    password = entry2.get()
    confirm_password = entry3.get()

    if password == confirm_password:
        if os.path.exists("Akun.xlsx"):
            df = pd.read_excel("Akun.xlsx")
        else:
            df = pd.DataFrame(columns=['Email', 'Password'])

        if email in df['Email'].values:
                messagebox.showerror("Error", "User sudah ada!")
        else:
            new_user = pd.DataFrame({'Email': [email], 'Password': [password]})
            df = pd.concat([df, new_user], ignore_index=True)
            df.to_excel("Akun.xlsx", index=False)
            messagebox.showinfo("Success", "Registrasi Berhasi!")
            app.destroy()
            import main_login  # Assuming the main login module is named main.py
    else:
        messagebox.showerror("Error", "Password tidak sama!")


app = customtkinter.CTk()  #creating cutstom tkinter window
app.geometry("1920x1080")
app.title('Register')


img1=ImageTk.PhotoImage(Image.open("Tugas Besar Reservasi Fasilitas/assets/pattern.png"))
l1=customtkinter.CTkLabel(master=app,image=img1, text = "")
l1.pack()

#creating custom frame
frame=customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
frame.place(relx=0.75, rely=0.25, anchor=tkinter.N)

l2=customtkinter.CTkLabel(master=frame, text="Register",font=('Century Gothic',44))
l2.place(x=50, y=20)

entry1=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Email')
entry1.place(x=50, y=90)

entry2=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
entry2.place(x=50, y=125)

entry3=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Konfirmasi Password', show="*")
entry3.place(x=50, y=160)

#Create custom button
button1 = customtkinter.CTkButton(master=frame, width=220, text="Sign Up", command=register_user, corner_radius=6)
button1.place(x=50, y=240)

def keluar():
    app.destroy()
    import main_login

imgexit = Image.open("Tugas Besar Reservasi Fasilitas/assets/logo.png")

btnexit = CTkButton(master=app, text="Kembali", corner_radius=32, fg_color="#222083", hover_color="#C850C0", border_color="#FFCC70", border_width=2, image=CTkImage(dark_image=imgexit, light_image=imgexit), bg_color="#0B0B2C", command=keluar, font=("Arial", 15))
btnexit.place(relx=0.98, rely=0.07, anchor="se") 

# You can easily integrate authentication system 

app.mainloop()
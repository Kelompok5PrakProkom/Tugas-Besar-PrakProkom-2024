import tkinter
import customtkinter
from PIL import ImageTk, Image
import pandas as pd
import os
from tkinter import messagebox
from customtkinter import CTkButton, CTkImage

customtkinter.set_appearance_mode("light") 
customtkinter.set_default_color_theme("dark-blue") 

app = customtkinter.CTk()  # creating custom tkinter window
app.geometry("1920x1080")
app.title('Login')

# Function to handle the Login button click
def button_function():
    # Check if the user exists in the database
    if os.path.exists("Akun.xlsx"):
        df = pd.read_excel("Akun.xlsx")
        email = entry1.get()
        password = entry2.get()

        # Validate the username and password
        if ((df['Email'] == email) & (df['Password'] == password)).any():
            with open("current_user.txt", "w") as file:
                file.write(email)
            app.destroy()  # Destroy the current window
            import book_fasilitas
        else:
            messagebox.showerror("Error", "Email atau Password Tidak Valid")
    else:
        messagebox.showerror("Error", "You don't have an account!")

# Function to handle the Forget Password button click
def belum_punya_akun():
    app.destroy()  # Destroy the current window
    import register  # Assuming register.py handles user registration


img1 = ImageTk.PhotoImage(Image.open("Tugas Besar Reservasi Fasilitas/assets/pattern.png"))
l1 = customtkinter.CTkLabel(master=app, image=img1, text="")
l1.pack()

# creating custom frame
frame = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
frame.place(relx=0.75, rely=0.25, anchor=tkinter.N)

l2 = customtkinter.CTkLabel(master=frame, text="Log In", font=('Century Gothic', 44))
l2.place(x=50, y=35)

entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Email')
entry1.place(x=50, y=110)

entry2 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
entry2.place(x=50, y=155)

l3 = customtkinter.CTkButton(master=frame, text="Belum Punya Akun?", font=('Century Gothic', 12), fg_color='#e5e5e5', text_color="Black", command=belum_punya_akun)
l3.place(x=155, y=195)

# Create custom button
button1 = customtkinter.CTkButton(master=frame, width=220, text="Login", command=button_function, corner_radius=6)
button1.place(x=50, y=240)

def keluar():
    app.quit()

imgexit = Image.open("Tugas Besar Reservasi Fasilitas/assets/logo.png")

btnexit = CTkButton(master=app, text="Keluar", corner_radius=32, fg_color="#222083", hover_color="#C850C0", border_color="#FFCC70", border_width=2, image=CTkImage(dark_image=imgexit, light_image=imgexit), bg_color="#0B0B2C", command=keluar, font=("Arial", 15))
btnexit.place(relx=0.98, rely=0.07, anchor="se")

app.mainloop()

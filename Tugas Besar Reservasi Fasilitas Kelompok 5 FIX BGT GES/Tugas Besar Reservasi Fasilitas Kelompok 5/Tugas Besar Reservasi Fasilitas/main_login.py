import tkinter
import customtkinter
from PIL import ImageTk, Image
import pandas as pd
import os
from tkinter import messagebox
from customtkinter import CTkButton, CTkImage

def login_main():
    customtkinter.set_appearance_mode("light") 
    customtkinter.set_default_color_theme("dark-blue") 

    app = customtkinter.CTk()  # creating custom tkinter window
    app.attributes("-fullscreen", True)
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
                import book_fasilitas as bf
                bf.jalan_book()
                return
            else:
                messagebox.showerror("Error", "Email atau Password Tidak Valid")
        else:
            messagebox.showerror("Error", "You don't have an account!")

    # Function to handle the Forget Password button click
    def belum_punya_akun():
        app.destroy()  # Destroy the current window
        import register as rg # Assuming register.py handles user registration
        rg.register_akun()
        return

    img1 = ImageTk.PhotoImage(Image.open("Tugas Besar Reservasi Fasilitas Kelompok 5/Tugas Besar Reservasi Fasilitas/assets/bgbgt.png"))
    l1 = customtkinter.CTkLabel(
        master=app, 
        image=img1, 
        text="")
    l1.pack()

    # creating custom frame
    frame = customtkinter.CTkFrame(
        master=l1, 
        width=420, 
        height=460, 
        fg_color="#C8E2FF", 
        bg_color="#FDB4B4",
        corner_radius=20)
    frame.place(
        relx=0.75, 
        rely=0.25, 
        anchor=tkinter.N)

    l2 = customtkinter.CTkLabel(
        master=frame, 
        text="Log In", 
        font=('Century Gothic', 44))
    l2.place(x=75, y=35) 


    entry1 = customtkinter.CTkEntry(
        master=frame, 
        width=270, 
        placeholder_text='Email', 
        font=("Century Gothic", 22))
    entry1.place(x=75, y=110)

    entry2 = customtkinter.CTkEntry(
        master=frame, 
        width=270, 
        placeholder_text='Password', 
        font= ("Century Gothic", 22),
        show="*")
    entry2.place(x=75, y=165)

    l3 = customtkinter.CTkButton(
        master=frame, 
        text="Belum Punya Akun?", 
        font=('Century Gothic', 14), 
        fg_color='#C8E2FF',
        hover_color='#C8E2FF', 
        text_color="Black", 
        command=belum_punya_akun)
    l3.place(x=180, y=340)

    # Create custom button
    button1 = customtkinter.CTkButton(
        master=frame, 
        width=270, 
        text="Login",
        font=("Century Gothic", 24), 
        command=button_function, 
        corner_radius=6)
    button1.place(x=75, y=300)

    def keluar():
        app.quit()

    imgexit = Image.open("Tugas Besar Reservasi Fasilitas Kelompok 5/Tugas Besar Reservasi Fasilitas/assets/logo.png")

    btnexit = CTkButton(
        master=app, 
        text="Keluar", 
        corner_radius=32,
        height=30, 
        fg_color="#F80000", 
        hover_color="#8D0000", 
        border_color="#C8E2FF", 
        border_width=2, 
        image=CTkImage(dark_image=imgexit, light_image=imgexit), 
        bg_color="#FDB4B4", 
        command=keluar, 
        font=("Arial", 18))
    btnexit.place(relx=0.98, rely=0.07, anchor="se")

    app.mainloop()
login_main()
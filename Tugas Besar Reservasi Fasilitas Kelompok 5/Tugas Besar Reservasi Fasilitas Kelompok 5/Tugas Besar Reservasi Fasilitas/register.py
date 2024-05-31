import tkinter
import customtkinter
import pandas as pd
import os
from PIL import ImageTk,Image
from tkinter import messagebox
from customtkinter import CTkButton, CTkImage

def register_akun():

    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("dark-blue")


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
                import main_login as ml
                ml.login_main()
                return
        else:
            messagebox.showerror("Error", "Password tidak sama!")

    def keluar():
        app.destroy()
        import main_login as ml
        ml.login_main()
        return

    app = customtkinter.CTk()  #creating cutstom tkinter window
    app.attributes("-fullscreen",True)
    app.title('Register')


    img1=ImageTk.PhotoImage(Image.open("Tugas Besar Reservasi Fasilitas Kelompok 5/Tugas Besar Reservasi Fasilitas/assets/bgbgt.png"))
    l1=customtkinter.CTkLabel(
        master=app,
        image=img1, 
        text = "")
    l1.pack()

    #creating custom frame
    frame = customtkinter.CTkFrame(
        master=l1, 
        width=420, 
        height=460, 
        fg_color="#C8E2FF", 
        bg_color="#FDB4B4")
    frame.place(
        relx=0.75, 
        rely=0.25, 
        anchor=tkinter.N)

    l2=customtkinter.CTkLabel(
        master=frame, 
        text="Register",
        font=('Century Gothic',44))
    l2.place(x=75, y=35)

    entry1=customtkinter.CTkEntry(
        master=frame, 
        width=270, 
        placeholder_text='Email', 
        font=("Century Gothic", 22))
    entry1.place(x=75, y=110)

    entry2=customtkinter.CTkEntry(
        master=frame, 
        width=270, 
        placeholder_text='Password', 
        show="*", 
        font=("Century Gothic", 22))
    entry2.place(x=75, y=165)

    entry3=customtkinter.CTkEntry(
        master=frame,
        width=270, 
        placeholder_text='Konfirmasi Password', 
        show="*", 
        font=("Century Gothic", 22))
    entry3.place(x=75, y=220)

    #Create custom button
    button1 = customtkinter.CTkButton(
        master=frame, 
        width=270, 
        text="Sign Up",
        font=("Century Gothic", 24), 
        command=register_user, 
        corner_radius=6)
    button1.place(x=75, y=300)


    imgexit = Image.open("Tugas Besar Reservasi Fasilitas Kelompok 5/Tugas Besar Reservasi Fasilitas/assets/logo.png")

    btnexit = CTkButton(
        master=app, 
        text="Kembali", 
        corner_radius=32, 
        height= 30, 
        fg_color="#F80000", 
        hover_color="#8D0000", 
        border_color="#FFCC70", 
        border_width=2, 
        image=CTkImage(dark_image=imgexit, light_image=imgexit), 
        bg_color="#FDB4B4", 
        command=keluar, 
        font=("Arial", 18))
    btnexit.place(relx=0.98, rely=0.07, anchor="se") 

    app.mainloop()

register_akun()
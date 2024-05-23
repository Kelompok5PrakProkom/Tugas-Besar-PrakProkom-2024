from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from login import Login

def halaman_login () :
    window = tk.Tk ()
    window.title ('Halaman Login')
    window.geometry ('1920x1080')
    window.configure (bg = '#3533cd')
    window.resizable (True, True)

    img = Image.open('bgr.png')
    resized_img = img.resize((1920, 1080))
    resized_img_tk = ImageTk.PhotoImage(resized_img)
    Label(window, image=resized_img_tk, bg='#3533cd').place(x=0, y=0)

    frame = Frame(window, width = 400, height = 600, bg = 'white')
    frame.place(x=1300,y=200)

    heading = Label(frame, text = 'Login', font = 'montserrat 40 bold', bg = 'white', fg = 'black')
    heading.place(x=130,y=50)

    username = Entry(frame, width = 25, fg= 'black', border='20', bg='#87CEFA', font = (30))
    username.place(x=50,y=180)

    username = Entry(frame, width = 25, fg= 'black', border='20', bg='#87CEFA', font = (30), show = '*')
    username.place(x=50,y=250)

    Button(frame, width =39, height=1, text = 'Login', fg='White', bg = 'blue').place(x=50,y=480)
    Button(frame, width =39, height=1, text = 'Sign In', fg='White', bg = 'blue', command=halaman_register).place(x=50,y=530)

    img_unity = Image.open('unity.png')
    resized_img_unity = img_unity.resize((606, 378))
    resized_img_tk_unity = ImageTk.PhotoImage(resized_img_unity)
    Label(window, image=resized_img_tk_unity).place(x=350, y=270)



    window.mainloop ()

def halaman_register():
    
    window = tk.Tk()
    window.title('Halaman Register')
    window.geometry('1920x1080')
    window.configure(bg='white')
    window.resizable(True, True)

    frame = Frame(window, width=800, height=600, bg='green')
    frame.place(x=100, y=100)

    heading = Label(frame, text='Halaman Register', font='arial 20 bold', bg='green', fg='white')
    heading.place(x=50, y=50)

    username = Entry(frame, width=25, fg='black', border='2', bg='yellow', font=(11))
    username.place(x=50, y=100)

    password = Entry(frame, width=25, fg='black', border='2', bg='yellow', font=(11), show='*')
    password.place(x=50, y=130)

    confirm_password = Entry(frame, width=25, fg='black', border='2', bg='yellow', font=(11), show='*')
    confirm_password.place(x=50, y=160)

    Button(frame, width=39, height=1, text='Register', fg='White', bg='blue').place(x=50, y=200)
    Button(frame, width=39, height=1, text='Back to Login', fg='White', bg='blue', command=window.destroy).place(x=50, y=230)


    window.mainloop()




halaman_login ()
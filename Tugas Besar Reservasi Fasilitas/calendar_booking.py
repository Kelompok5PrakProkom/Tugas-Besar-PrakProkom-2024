import customtkinter
from PIL import ImageTk, Image

app = customtkinter.CTk()  #creating cutstom tkinter window
app.geometry("1920x1080")
app.title('Register')


img1=ImageTk.PhotoImage(Image.open("assets/pattern.png"))
l1=customtkinter.CTkLabel(master=app,image=img1, text = "")
l1.pack()

app.mainloop()
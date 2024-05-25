import tkinter
import customtkinter
from customtkinter import CTk, CTkButton, CTkToplevel, CTkLabel, CTkImage
from PIL import ImageTk, Image
from tkinter import Frame

customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk() 
app.geometry("1920x1080")
app.title('Reservasi Fasilitas')

img1 = ImageTk.PhotoImage(Image.open("assets/pilihanfasilitas.png"))
l1 = customtkinter.CTkLabel(master=app, image=img1, text="")
l1.pack()

frame=customtkinter.CTkFrame(master=l1, width=1920, height=390, fg_color="#EBEBEB")
frame.place(relx=0.51, rely=0.51, anchor=tkinter.CENTER)

def keluar():
    app.destroy()  # Destroy the current window
    import main_login

imgpopup = Image.open("assets/logo.png")

btnexit = CTkButton(master=app, text="Kembali", corner_radius=32, fg_color="#222083", hover_color="#C850C0", border_color="#FFCC70", border_width=2, image=CTkImage(dark_image=imgpopup, light_image=imgpopup), bg_color="#3230C0", command=keluar, font=("Arial", 15))
btnexit.place(relx=0.98, rely=0.07, anchor="se") 

# Fungsi untuk menampilkan jendela pop-up
def show_popup(image_path, description):
    popup = CTkToplevel(app)
    popup.geometry("500x500")
    popup.title("Detail Fasilitas")
    popup.resizable(False,False)

    imgpopup = ImageTk.PhotoImage(Image.open("assets/background.png"))
    l1 = customtkinter.CTkLabel(master=popup, image=imgpopup, text="")
    l1.pack()

    framepopup=customtkinter.CTkFrame(master=l1, width=402, height=510, fg_color="#EBEBEB")
    framepopup.place(relx=0.50, rely=0.50, anchor=tkinter.CENTER)

    # Ensure the popup stays in front
    popup.transient(app)
    popup.grab_set()

    img = Image.open(image_path)
    img = img.resize((300, 300), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)

    frame1=customtkinter.CTkFrame(master=popup, width=270, height=270, fg_color="#3230C0", corner_radius=15)
    frame1.place(relx=0.5, rely=0.6, anchor=tkinter.S)
    
    # Keep a reference to prevent garbage collection
    label_image = CTkLabel(master=popup, image=img_tk, text="")
    label_image.image = img_tk  # Keep a reference to prevent garbage collection
    label_image.pack(pady=20)
    label_image.place(relx=0.5, rely=0.57, anchor=tkinter.S)

    frame2=customtkinter.CTkFrame(master=popup, width=400, height=110, fg_color="#14134D", corner_radius=15)
    frame2.place(relx=0.5, rely=0.615, anchor=tkinter.N)

    label_description = CTkLabel(master=popup, text=description, wraplength=400, font=("Arial", 18), text_color="white", fg_color="#14134D")
    label_description.pack(pady=20)
    label_description.place(relx=0.5, rely=0.665, anchor="n") 

    # Keep a reference to prevent garbage collection
    popup.image = img_tk

    img3 = Image.open("assets/logo.png")

    def book():
        app.destroy()
        import calendar_booking

    btn = CTkButton(master=popup, text="Booking Sekarang", corner_radius=32, fg_color="#222083", hover_color="#C850C0", border_color="#FFCC70", border_width=2, image=CTkImage(dark_image=img3, light_image=img3), font=("Arial", 15), command=book)
    btn.place(relx=0.5, rely=0.85, anchor="n") 


    

# Memuat dan mengatur gambar untuk tombol
image_paths = [
    "assets/lapangan.png",  # Ganti dengan path ke gambar Anda
    "assets/seminar.png",
    "assets/multimedia.png",
    "assets/workingspace.png"
]

descriptions = [
    "Area terbuka di lingkungan fakultas yang berfungsi sebagai pusat kegiatan akademik, olahraga, dan sosial",
    "Ruang yang disediakan untuk mengadakan diskusi, presentasi dan pelatihan. Dilengkapi dengan peralatan audiovisual seperti proyektor, layar, dll.",
    "Ruang yang disediakan untuk mendukung berbagai kegiatan berbasis teknologi dan audiovisual. Seperti presentasi,konferensi video, dll.",
    "Ruang yang disediakan kepada mahasiswa untuk belajar, bekerja, serta berkolaboras. Dilengkapi dengan internet lancar serta colokan listrik"
]

# Mengatur parameter tombol
button_width = 350
button_height = 345
spacing = 10  # Spasi antara tombol
header_height = 220  # Tinggi header
num_buttons = 4  # Jumlah tombol

# Menghitung total lebar semua tombol dan spasi
total_width = num_buttons * button_width + (num_buttons - 1) * spacing

# Menghitung posisi awal x untuk menempatkan tombol secara terpusat
start_x = (app.winfo_screenwidth() - total_width) // 2
button_y = header_height + spacing

# Membuat dan menempatkan tombol
buttons = []
for i in range(num_buttons):
    x = start_x + i * (button_width + spacing)
    image = Image.open(image_paths[i])
    image = image.resize((button_width, button_height), Image.LANCZOS)
    image_tk = ImageTk.PhotoImage(image)

    button = customtkinter.CTkButton(
        app,
        image=image_tk,
        text="",  # Hapus teks tombol agar hanya gambar yang terlihat
        width=button_width,
        height=button_height,
        fg_color="black",
        corner_radius=30,
        command=lambda i=i: show_popup(image_paths[i], descriptions[i])
    )
    button.place(x=x, y=button_y)
    buttons.append(button)

app.mainloop()

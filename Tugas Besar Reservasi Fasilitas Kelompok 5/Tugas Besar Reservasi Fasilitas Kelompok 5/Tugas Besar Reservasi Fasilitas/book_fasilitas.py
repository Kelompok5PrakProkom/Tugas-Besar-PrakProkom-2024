import tkinter as tk
import customtkinter
from customtkinter import CTk, CTkButton, CTkToplevel, CTkLabel, CTkImage
from PIL import ImageTk, Image
import importlib


def jalan_book():
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("dark-blue")

    app = customtkinter.CTk() 
    app.attributes("-fullscreen", True)
    app.title('Reservasi Fasilitas')

    img1 = ImageTk.PhotoImage(Image.open("Tugas Besar Reservasi Fasilitas Kelompok 5/Tugas Besar Reservasi Fasilitas/assets/pilihanfasilitas.png"))
    l1 = customtkinter.CTkLabel(master=app, image=img1, text="")
    l1.pack()
 
    frame = customtkinter.CTkFrame(
        master=l1, 
        width=1920, 
        height=390, 
        fg_color="#EBEBEB")
    frame.place(
        relx=0.50, 
        rely=0.50, 
        anchor=tk.CENTER)

    def keluar():
        app.destroy()  # Destroy the current window
        import main_login as ml
        ml.login_main()
        return

    def balik():
        app.destroy()
        jalan_book()


    imgpopup = Image.open("Tugas Besar Reservasi Fasilitas Kelompok 5/Tugas Besar Reservasi Fasilitas/assets/logo.png")

    btnexit = CTkButton(
        master=app, 
        text="Log Out", 
        corner_radius=32, 
        fg_color="#F80000", 
        hover_color="#8D0000", 
        border_color="#C8E2FF", 
        border_width=2, 
        image=CTkImage(dark_image=imgpopup, light_image=imgpopup), 
        bg_color="#FDB4B4", 
        command=keluar, 
        font=("Arial", 18))
    btnexit.place(
        relx=0.98, 
        rely=0.07, 
        anchor="se") 

    # Function to show the popup
    def show_popup(image_path, description, module_name, facility_name):
        popup = CTkToplevel(app)
        popup.attributes("-fullscreen", True)
        popup.title("Detail Fasilitas")
        popup.resizable(True, True)

        imgpopup = ImageTk.PhotoImage(Image.open("Tugas Besar Reservasi Fasilitas Kelompok 5/Tugas Besar Reservasi Fasilitas/assets/bglain.png"))
        l1 = customtkinter.CTkLabel(master=popup, image=imgpopup, text="")
        l1.pack()

        framepopup = customtkinter.CTkFrame(
            master=l1, 
            width=500, 
            height=510, 
            fg_color="#9FCDFF", 
            bg_color="#FDB4B4")
        framepopup.place(relx=0.50, rely=0.50, anchor=tk.CENTER)

        # Ensure the popup stays in front
        popup.transient(app)
        popup.grab_set()

        img = Image.open(image_path)
        img = img.resize((500, 500), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        frame1 = customtkinter.CTkFrame(
            master=popup, 
            width=270, 
            height=270, 
            fg_color="#9FCDFF")
        frame1.place(
            relx=0.5, 
            rely=0.6, 
            anchor=tk.S)
        
        # Keep a reference to prevent garbage collection
        label_image = CTkLabel(master=popup, image=img_tk, text="")
        label_image.image = img_tk  # Keep a reference to prevent garbage collection
        label_image.pack(pady=20)
        label_image.place(relx=0.5, rely=0.61, anchor=tk.S)

        frame2 = customtkinter.CTkFrame(
            master=popup, 
            width=500, 
            height=65, 
            fg_color="#9FCDFF", 
            corner_radius=0)
        frame2.place(
            relx=0.5, 
            rely=0.615, 
            anchor=tk.N)

        header_label = CTkLabel(
            master=popup, 
            text=facility_name, 
            font=("Rockwell", 42, "bold"), 
            text_color="black",
            fg_color="#FDB4B4")
        header_label.pack(pady=10)
        header_label.place(relx=0.5, rely=0.075, anchor="n")

        label_description = CTkLabel(
            master=popup, 
            text=description, 
            wraplength=500, 
            font=("Comic Sans MS", 22), 
            text_color="black", 
            fg_color="#9FCDFF")
        label_description.pack(pady=20)
        label_description.place(relx=0.5, rely=0.62, anchor="n") 

        # Keep a reference to prevent garbage collection
        popup.image = img_tk

        img3 = Image.open("Tugas Besar Reservasi Fasilitas Kelompok 5/Tugas Besar Reservasi Fasilitas/assets/logo.png")

        def book():
            try:
                app.destroy()
                module = importlib.import_module(module_name)
                if hasattr(module, 'start_app'):
                    module.start_app()
                else:
                    print(f"Module {module_name} does not have a start_app function.")
            except ImportError:
                print(f"Module {module_name} tidak ditemukan.")

        btn = CTkButton(
            master=popup, 
            text="Booking Sekarang", 
            corner_radius=32, 
            fg_color="#222083", 
            hover_color="#C850C0", 
            border_color="#FFCC70", 
            border_width=2, 
            bg_color="#FDB4B4", 
            image=CTkImage(dark_image=img3, light_image=img3), 
            font=("Comic Sans MS", 24), 
            command=book)
        btn.place(relx=0.5, rely=0.85, anchor="n") 

        # Define the exit button
        exitbtn = customtkinter.CTkButton(
            popup,
            text="Kembali",
            corner_radius=32,
            fg_color="#F80000",
            hover_color="#8D0000",
            border_color="#C8E2FF",
            border_width=2,
            bg_color="#FDB4B4",
            image=CTkImage(dark_image=img3, light_image=img3),
            font=("Arial", 18),
            command=balik)
        exitbtn.place(
            relx=0.98, 
            rely=0.07, 
            anchor="se") 

    # Load and set images for buttons
    image_paths = [
        "Tugas Besar Reservasi Fasilitas Kelompok 5/Tugas Besar Reservasi Fasilitas/assets/lapangan.png",
        "Tugas Besar Reservasi Fasilitas Kelompok 5/Tugas Besar Reservasi Fasilitas/assets/seminar.png",
        "Tugas Besar Reservasi Fasilitas Kelompok 5/Tugas Besar Reservasi Fasilitas/assets/multimedia.png",
        "Tugas Besar Reservasi Fasilitas Kelompok 5/Tugas Besar Reservasi Fasilitas/assets/workingspace.png"
    ]

    descriptions = [
        "Area terbuka di lingkungan fakultas yang berfungsi sebagai pusat kegiatan akademik, olahraga, dan sosial",
        "Ruang yang disediakan untuk mengadakan diskusi, presentasi dan pelatihan. Dilengkapi dengan peralatan audiovisual seperti proyektor, layar, dll.",
        "Ruang yang disediakan untuk mendukung berbagai kegiatan berbasis teknologi dan audiovisual. Seperti presentasi,konferensi video, dll.",
        "Ruang yang disediakan kepada mahasiswa untuk belajar, bekerja, serta berkolaboras. Dilengkapi dengan internet lancar serta colokan listrik"
    ]

    facility_names = [
        "LAPANGAN",
        "RUANG SEMINAR",
        "RUANG MULTIMEDIA",
        "WORKING SPACE"
    ]

    modules = [
        "lapangan",
        "ruang_seminar",
        "ruang_multimedia",
        "working_space"
    ]

    # Configure button parameters
    button_width = 360
    button_height = 345
    spacing = 100  # Spacing between buttons
    header_height = 260  # Header height
    num_buttons = 4  # Number of buttons

    # Calculate total width of all buttons and spacing
    total_width = (num_buttons * button_width + (num_buttons - 1) * spacing) + 50 

    # Calculate the starting x position to center the buttons
    start_x = (app.winfo_screenwidth() - total_width) // 2
    button_y = header_height + spacing

    # Create and place buttons
    buttons = []
    for i in range(num_buttons):
        x = start_x + i * (button_width + spacing)
        image = Image.open(image_paths[i])
        image = image.resize((button_width, button_height), Image.LANCZOS)
        image_tk = ImageTk.PhotoImage(image)

        button = customtkinter.CTkButton(
            app,
            image=image_tk,
            text="",  # Remove button text to show only the image
            width=button_width,
            height=button_height,
            fg_color="#F0CAA4",
            bg_color="#EBEBEB",
            corner_radius=30,
            command=lambda i=i: show_popup(image_paths[i], descriptions[i], modules[i], facility_names[i])
        )
        button.place(x=x, y=button_y)
        buttons.append(button)

    app.mainloop()
jalan_book()
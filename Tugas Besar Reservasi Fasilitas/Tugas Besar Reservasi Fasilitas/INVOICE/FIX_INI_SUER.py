import customtkinter as ctk
from tkinter import messagebox
from fpdf import FPDF
import os
import csv
from tkinter import ttk
import ttkbootstrap as ttkb

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

class InvoiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Invoice Generator")
        self.root.geometry("600x600")

        # Nama
        self.label_name = ctk.CTkLabel(root, text="Nama:")
        self.label_name.pack(pady=5)
        self.entry_name = ctk.CTkEntry(root)
        self.entry_name.pack(pady=5)

        # Kalender
        self.label_date = ctk.CTkLabel(root, text="Pilih Tanggal:")
        self.label_date.pack(pady=5)
        self.cal = ttkb.DateEntry(root, dateformat='%d/%m/%y', bootstyle="primary")
        self.cal.pack(pady=5)

        # Waktu
        self.label_time = ctk.CTkLabel(root, text="Pilih Waktu:")
        self.label_time.pack(pady=5)
        self.time_values = [f"{hour:02d}:00" for hour in range(8, 18)]
        self.time_combobox = ttk.Combobox(root, values=self.time_values, state="readonly")
        self.time_combobox.current(0)  # Set default time to 08:00
        self.time_combobox.pack(pady=5)

        # Durasi
        self.label_duration = ctk.CTkLabel(root, text="Pilih Durasi (jam):")
        self.label_duration.pack(pady=5)
        self.duration_values = [str(i) for i in range(1, 9)]  # Durasi dari 1 hingga 9 jam
        self.duration_combobox = ttk.Combobox(root, values=self.duration_values, state="readonly")
        self.duration_combobox.current(0)  # Set default duration to 1 hour
        self.duration_combobox.pack(pady=5)

        # Tombol untuk membuat invoice
        self.button_generate = ctk.CTkButton(root, text="Generate Invoice", command=self.generate_invoice)
        self.button_generate.pack(pady=20)

        # Area untuk menampilkan invoice
        self.text_invoice = ctk.CTkTextbox(root, height=200)
        self.text_invoice.pack(pady=10)

    def generate_invoice(self):
        name = self.entry_name.get()
        date = self.cal.entry.get()
        start_time = self.time_combobox.get()
        duration = self.duration_combobox.get()

        if not name or not date or not start_time or not duration:
            messagebox.showerror("Error", "Semua field harus diisi!")
            return

        # Data pemesanan simulasi (bisa diganti dengan data yang sebenarnya)
        invoice_details = [
            {"Tanggal": "01/01/2024", "Start": "08:00", "End": "10:00"},
            {"Tanggal": "01/01/2024", "Start": "10:00", "End": "12:00"}
        ]

        email = "contoh@email.com"  # Email simulasi (bisa diganti dengan email yang sebenarnya)

        # Generate invoice text
        invoice_text = (
            f"Invoice Pemesanan Fasilitas\n"
            f"============================\n"
            f"Nama      : {name}\n"
            f"Email     : {email}\n"
            f"Tanggal   : {date}\n"
            f"Start     : {start_time}\n"
            f"Durasi    : {duration} jam\n"
            f"============================\n"
        )

        for detail in invoice_details:
            invoice_text += (
                f"Tanggal   : {detail['Tanggal']}\n"
                f"Start     : {detail['Start']}\n"
                f"End       : {detail['End']}\n"
                f"----------------------------\n"
            )

        self.text_invoice.delete(1.0, ctk.END)
        self.text_invoice.insert(ctk.END, invoice_text)

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for line in invoice_text.split('\n'):
            pdf.cell(200, 10, txt=line, ln=True, align='L')

        pdf_filename = f"Invoice_{name.replace(' ', '_')}.pdf"
        try:
            pdf.output(pdf_filename)
            if os.path.exists(pdf_filename):
                messagebox.showinfo("Success", f"Invoice berhasil disimpan sebagai {pdf_filename}")
            else:
                messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan invoice sebagai PDF!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Set theme
    ctk.set_default_color_theme("blue")  # Set color theme

    root = ctk.CTk()
    app = InvoiceApp(root)
    root.mainloop()

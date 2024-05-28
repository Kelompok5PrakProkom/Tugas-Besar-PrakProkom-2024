import customtkinter as ctk
from tkinter import messagebox, filedialog
from fpdf import FPDF
import os
import csv
from tkinter import ttk
import ttkbootstrap as ttkb

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
        
        # Tombol untuk memilih file CSV
        self.button_select_files = ctk.CTkButton(root, text="Pilih File CSV", command=self.select_files)
        self.button_select_files.pack(pady=20)
        
        # Tombol untuk membuat invoice
        self.button_generate = ctk.CTkButton(root, text="Generate Invoice", command=self.generate_invoice)
        self.button_generate.pack(pady=20)
        
        # Area untuk menampilkan invoice
        self.text_invoice = ctk.CTkTextbox(root, height=200)
        self.text_invoice.pack(pady=10)

        self.book1_path = ''
        self.akun_path = ''

    def select_files(self):
        self.book1_path = filedialog.askopenfilename(title="Pilih Book1.csv", filetypes=[("CSV files", ".csv")])
        self.akun_path = filedialog.askopenfilename(title="Pilih Akun.csv", filetypes=[("CSV files", ".csv")])
        if not self.book1_path.endswith('.csv') or not self.akun_path.endswith('.csv'):
            messagebox.showerror("Error", "Anda harus memilih file CSV yang valid!")
            self.book1_path = ''
            self.akun_path = ''

    def generate_invoice(self):
        name = self.entry_name.get()
        date = self.cal.entry.get()
        start_time = self.time_combobox.get()
        duration = self.duration_combobox.get()
        
        if not name or not date or not start_time or not duration:
            messagebox.showerror("Error", "Semua field harus diisi!")
            return

        if not self.book1_path or not self.akun_path:
            messagebox.showerror("Error", "Anda harus memilih kedua file CSV!")
            return
        
        # Membaca data dari file CSV
        invoice_details = []
        try:
            with open(self.book1_path, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    # Debug log
                    print(f"Checking row: {row}")
                    if row[1] == date:
                        invoice_details.append({
                            "Tanggal": row[1],  # Asumsi kolom tanggal ada di kolom kedua
                            "Start": row[2],    # Asumsi kolom start ada di kolom ketiga
                            "End": row[3]       # Asumsi kolom end ada di kolom keempat
                        })
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membaca file CSV: {e}")
            return
        
        if not invoice_details:
            messagebox.showerror("Error", "Tidak ada data untuk tanggal yang dipilih!")
            return
        
        # Membaca email pengguna dari file CSV Akun.csv
        email = ""
        try:
            with open(self.akun_path, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    if row[0] == name:  # Asumsi kolom nama ada di kolom pertama
                        email = row[1]
                        break
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membaca file CSV Akun: {e}")
            return
        
        if not email:
            messagebox.showerror("Error", "Email untuk nama yang diberikan tidak ditemukan!")
            return
        
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
        
        # Save booking data to CSV
        self.save_to_csv(date, start_time, duration)

    def save_to_csv(self, date, start_time, duration):
        file_path = 'booking_data.csv'
        file_exists = os.path.isfile(file_path)
        
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Date", "Start Time", "Duration (hours)"])  # Menulis header jika file belum ada
            writer.writerow([date, start_time, duration])

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Set theme
    ctk.set_default_color_theme("blue")  # Set color theme
    
    root = ctk.CTk()
    app = InvoiceApp(root)
    root.mainloop()

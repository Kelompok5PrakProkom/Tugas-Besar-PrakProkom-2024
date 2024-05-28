import customtkinter as ctk
root = ctk.CTk()

class MultiSelectFrame(ctk.CTkFrame):
    def __init__(self, master, values):
        super().__init__(master)
        self.selected_values = set()  # Use a set for faster membership checks
        self.checkboxes = {}
        for value in values:
            checkbox = ctk.CTkCheckBox(self, text=value)
            checkbox.pack()
            self.checkboxes[value] = checkbox
            checkbox.bind("<Button-1>", self.on_checkbox_click)

    def on_checkbox_click(self, event):
        checkbox = event.widget
        value = checkbox.text
        if checkbox.get():
            self.selected_values.add(value)
        else:
            self.selected_values.discard(value)

    def get_selected(self):
        return list(self.selected_values)  # Convert set to list for compatibility

# ... rest of your code ...

facility_selection_label = ctk.CTkLabel(root, text="Fasilitas Pilihan (pilih beberapa):")
facility_multiselect = MultiSelectFrame(root, list(available_facilities.keys()))
facility_multiselect.pack()


import customtkinter

class SettingsView(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("200x200")
        self.title("Configuracion")
        
        labelTitle = customtkinter.CTkLabel(self, text="label")
        labelTitle.pack()
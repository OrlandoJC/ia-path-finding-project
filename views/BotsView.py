import customtkinter
from PIL import Image, ImageTk

class BotsView(customtkinter.CTkToplevel):
    def __init__(self, paths, onDrawPath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x210")
        self.config(background="white")
        self.title("Visualización")

        self.label = customtkinter.CTkLabel(self, text="Ver camino del agente", fg_color="white", font=("Comic Sans MS",14))
        self.label.pack(padx=20, pady=20)

        self.paths = paths
        self.onDrawPath = onDrawPath

        combobox = customtkinter.CTkComboBox(master=self,
                                     values=["Bot 1", "Bot 2", "Bot 3", "Bot 4", "Bot 5", "Bot 6", "Bot 7", "Bot 8"],
                                     command=self.combobox_callback, button_color="#6495ED", text_color="black", state="readonly")
        combobox.pack(padx=20, pady=10)
        combobox.set("Seleccionar bot..")  # set initial value
        
        #Principal State
        self.tamaño=customtkinter.CTkLabel(self, text="Esperando..", fg_color="white", font=("Comic Sans MS",14)) 
        self.tamaño.pack(padx=20, pady=15)
        self.img = img = ImageTk.PhotoImage(file=r'img\robot.png')
        self.label_imagen= customtkinter.CTkLabel(self,image=self.img,text=" ", anchor=customtkinter.NW, fg_color="white", bg_color="white")
        self.label_imagen.pack()

    def combobox_callback(self, choice):
        print("combobox dropdown clicked:", choice)
        self.colors = ["#6495ED", "#FF7F50", "#CCCCFF", "#40E0D0", "#9FE2BF", "#FFBF00", "#AC65FC", "#FC8D65"]
        path_to_draw = None
        color_to_path = "#6495ED"

        if choice == "Bot 1":
            path_to_draw = self.paths[0][1]
            color_to_path = self.colors[0]
            longitud = len(path_to_draw)

        elif choice == "Bot 2":
            path_to_draw = self.paths[1][1]
            color_to_path = self.colors[1]
            longitud = len(path_to_draw)

        elif choice == "Bot 3":
            path_to_draw = self.paths[2][1]
            color_to_path = self.colors[2]
            longitud = len(path_to_draw)

        elif choice == "Bot 4":
            path_to_draw = self.paths[3][1]
            color_to_path = self.colors[3]
            longitud = len(path_to_draw)

        elif choice == "Bot 5":
            path_to_draw = self.paths[4][1]
            color_to_path = self.colors[4]
            longitud = len(path_to_draw)

        elif choice == "Bot 6":
            path_to_draw = self.paths[5][1]
            color_to_path = self.colors[5]
            longitud = len(path_to_draw)

        elif choice == "Bot 7":
            path_to_draw = self.paths[6][1]
            color_to_path = self.colors[6]
            longitud = len(path_to_draw)

        elif choice == "Bot 8":
            path_to_draw = self.paths[7][1]
            color_to_path = self.colors[7]
            longitud = len(path_to_draw)

        self.tamaño.configure(text=f"El {choice} realizará {longitud} movimientos", font=("Comic Sans MS",14)) #Update values
        self.onDrawPath(path_to_draw, color_to_path)

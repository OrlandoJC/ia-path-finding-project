import customtkinter

class BotsView(customtkinter.CTkToplevel):
    def __init__(self, paths, onDrawPath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x150")
        self.config(background="white")
        self.title("Visualizacion")

        self.label = customtkinter.CTkLabel(self, text="Ver camino del bot", fg_color="white")
        self.label.pack(padx=20, pady=20)

        self.paths = paths
        self.onDrawPath = onDrawPath

        combobox = customtkinter.CTkComboBox(master=self,
                                     values=["Bot 1", "Bot 2", "Bot 3", "Bot 4", "Bot 5", "Bot 6", "Bot 7", "Bot 8"],
                                     command=self.combobox_callback, button_color="#6495ED", text_color="black", state="readonly")
        combobox.pack(padx=20, pady=10)
        combobox.set("Seleccionar bot..")  # set initial value

    def combobox_callback(self, choice):
        print("combobox dropdown clicked:", choice)
        self.colors = ["#6495ED", "#FF7F50", "#CCCCFF", "#40E0D0", "#9FE2BF", "#FFBF00", "#AC65FC", "#FC8D65"]
        path_to_draw = None
        color_to_path = "#6495ED"

        if choice == "Bot 1":
            path_to_draw = self.paths[0][1]
            color_to_path= self.colors[0]
            
        if choice == "Bot 2":
            path_to_draw = self.paths[1][1]
            color_to_path= self.colors[1]

        if choice == "Bot 3":
            path_to_draw = self.paths[2][1]
            color_to_path= self.colors[2]

        if choice == "Bot 4":
            path_to_draw = self.paths[3][1]
            color_to_path= self.colors[3]

        if choice == "Bot 5":
            path_to_draw = self.paths[4][1]
            color_to_path= self.colors[4]

        if choice == "Bot 6":
            path_to_draw = self.paths[5][1]
            color_to_path= self.colors[5]

        if choice == "Bot 7":
            path_to_draw = self.paths[6][1]
            color_to_path= self.colors[6]

        if choice == "Bot 8":
            path_to_draw = self.paths[7][1]
            color_to_path= self.colors[7]


        self.onDrawPath(path_to_draw, color_to_path)
            

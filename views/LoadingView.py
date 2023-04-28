import customtkinter

class LoadingView(customtkinter.CTkToplevel):
    def __init__(self, isLoading, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("350x90")
        self.config(background="white")
        self.resizable(False, False)
        self.title("")

        self.attributes("-topmost", True)
        
        self.protocol("WM_DELETE_WINDOW", lambda: None)
        # self.protocol("WM_ICONIFY_WINDOW", lambda: None)
        self.attributes("-disabled", 1)

        
        # Obtener el ancho y la altura de la pantalla
        ancho_pantalla = self.winfo_screenwidth()
        altura_pantalla = self.winfo_screenheight()

        # Obtener el ancho y la altura de la ventana
        ancho_ventana = 350 # Coloca aquí el ancho de tu ventana
        altura_ventana = 90 # Coloca aquí la altura de tu ventana

        # Calcular la posición x e y para que la ventana esté centrada
        posicion_x = int(ancho_pantalla / 2 - ancho_ventana / 2) + 10
        posicion_y = int(altura_pantalla / 2 - altura_ventana / 2)

        # Establecer la posición de la ventana en el centro de la pantalla
        self.geometry("{}x{}+{}+{}".format(ancho_ventana, altura_ventana, posicion_x, posicion_y))

        self.isLoading = isLoading

        self.textos = ["Buscando caminos posibles...", "Calculando recompensas...", "Generando tabla Q...", "Buscando la ruta mas optima", "Sí, sí esta funcionando 😁"]

        # Variable de índice
        self.indice = 0
        self.texto_variable = customtkinter.StringVar()

        self.texto_variable.set("Entrenando agentes..")

        label_title = customtkinter.CTkLabel(self, text="Cargando",fg_color="white", bg_color="white")
        label_subtitle = customtkinter.CTkLabel(self, textvariable=self.texto_variable,fg_color="white", bg_color="white")

        progressbar = customtkinter.CTkProgressBar(self, orientation="horizontal", mode="indeterminate", fg_color="#F4F4F4")
        progressbar.start()

        progressbar.pack(pady=10)
        label_title.pack(pady=0)
        label_subtitle.pack()

        self.after(5000, self.cambiar_texto)

    def cambiar_texto(self):
        self.indice = (self.indice + 1) % len(self.textos)
        self.texto_variable.set(self.textos[self.indice])

        self.after(5000, self.cambiar_texto)
    
        


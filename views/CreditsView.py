import customtkinter
from PIL import Image, ImageTk

class Credits(customtkinter.CTkToplevel):
    def __init__(self, isLoading, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("350x90")
        self.config(background="white")
        self.resizable(False, False)
        self.title("")

        self.attributes("-topmost", True)

        # Obtener el ancho y la altura de la pantalla
        ancho_pantalla = self.winfo_screenwidth()
        altura_pantalla = self.winfo_screenheight()

        # Obtener el ancho y la altura de la ventana
        ancho_ventana = 350 # Coloca aquí el ancho de tu ventana
        altura_ventana = 500 # Coloca aquí la altura de tu ventana

        # Calcular la posición x e y para que la ventana esté centrada
        posicion_x = int(ancho_pantalla / 2 - ancho_ventana / 2) + 10
        posicion_y = int(altura_pantalla / 2 - altura_ventana / 2)

        # Establecer la posición de la ventana en el centro de la pantalla
        self.geometry("{}x{}+{}+{}".format(ancho_ventana, altura_ventana, posicion_x, posicion_y))

        
        self.img = img = ImageTk.PhotoImage(file=r'img\tecnologia.png')
        self.img2 = img2 = ImageTk.PhotoImage(file=r'img\servicios-digitales.png')
        self.img3 = img3 = ImageTk.PhotoImage(file=r'img\logo.png')
        label_title = customtkinter.CTkLabel(self,text="Creditos\n",fg_color="white", bg_color="white", font=("Comic Arial Black\n", 16))
        label_nombre = customtkinter.CTkLabel(self, text="Equipo3\n\nCuxin Yama Orlando de Jesus\n\nCanche Cab Gabriel Ivan\n\nDzib Tun Manuel Jesus",fg_color="white", bg_color="white", font=("Comic Sans MS",14))
        label_imagen= customtkinter.CTkLabel(self,image=self.img,text=" ", anchor=customtkinter.NW, fg_color="white", bg_color="white")
        label_imagen1= customtkinter.CTkLabel(self,image=self.img2,text=" ", anchor=customtkinter.NW, fg_color="white", bg_color="white")
        label_imagen2= customtkinter.CTkLabel(self,image=self.img3,text=" ", anchor=customtkinter.NW, fg_color="white", bg_color="white")

        label_title.pack(pady=0)
        label_imagen1.pack()
        label_nombre.pack()
        label_imagen.pack()
        label_imagen2.pack()
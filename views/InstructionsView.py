import customtkinter
from PIL import Image, ImageTk

class Instructions(customtkinter.CTkToplevel):
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

        
        self.img = img = ImageTk.PhotoImage(file=r'img\instruccion.png')
        label_title = customtkinter.CTkLabel(self,text="Instrucciones",fg_color="white", bg_color="white", font=("Comic Arial Black\n", 16))
        label_ruta = customtkinter.CTkLabel(self, text="Buscar ruta corta\n1. Seleccionar el paquete(Cuadrado) \n2. Dar click a Buscar Ruta\n",fg_color="white", bg_color="white", font=("Comic Sans MS",14))
        label_obstaculo= customtkinter.CTkLabel(self, text="Agregar obstáculo \n1. Dar click a Añadir Obstáculo\n 2. Poner un número de 1 a 6\n3. Colocar obstáculo en donde gustes\n", fg_color="white", bg_color="white",font=("Comic Sans MS",14) )
        label_paquete= customtkinter.CTkLabel(self, text="Agregar paquete \n1. Dar click a Añadir Paquete\n3. Colocar paquete en donde gustes\n", fg_color="white", bg_color="white", font=("Comic Sans MS", 14))
        label_borrar= customtkinter.CTkLabel(self, text="Borrar \n1. Seleccionar un paquete u obstáculo en el mapa\n2. Dar click a Borrar\n", fg_color="white", bg_color="white", font=("Comic Sans MS", 14) )
        label_imagen= customtkinter.CTkLabel(self,image=self.img,text=" ", anchor=customtkinter.NW, fg_color="white", bg_color="white")
        label_imagen1= customtkinter.CTkLabel(self,image=self.img,text=" ", anchor=customtkinter.NW, fg_color="white", bg_color="white")
        label_imagen2= customtkinter.CTkLabel(self,image=self.img,text=" ", anchor=customtkinter.NW, fg_color="white", bg_color="white")
        label_imagen3= customtkinter.CTkLabel(self,image=self.img,text=" ", anchor=customtkinter.NW, fg_color="white", bg_color="white")
        

        label_title.pack(pady=0)
        label_ruta.pack()
        label_imagen.pack()
        label_obstaculo.pack()
        label_imagen1.pack()
        label_paquete.pack()
        label_imagen2.pack()
        label_borrar.pack()
        label_imagen3.pack()
        


import customtkinter
from tkinter import LabelFrame
from tkinter import Spinbox
import tkinter.font as tkFont
import math
from tkinter.messagebox import askokcancel, showinfo, WARNING
from PIL import Image, ImageTk
from utils.graphics import colocarCaja, crearCuadricula, colocarObstaculo, boxByReference, obstacleReference, createDot, createLine
from utils.imagetk import getImageTk
from database.mapa import map, obstacles
import time
import threading
from tkinter import messagebox
from ia.GraphSearch import ejecutar_en_paralelo

# settings
from config.canvas import CanvasSetting
from config.app import AppConfig

# views
from views.configView import SettingsView
from views.BotsView import BotsView
from views.LoadingView import LoadingView
from views.InstructionsView import Instructions
from views.CreditsView import Credits

# environment
from config.enviroment import *

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry(AppConfig.SIZE)
        self.configure(fg_color=AppConfig.BG_COLOR)
        # self.resizable(False, False)
        self.title(AppConfig.TITLE)

        # Obtener el ancho y la altura de la pantalla
        ancho_pantalla = self.winfo_screenwidth()
        altura_pantalla = self.winfo_screenheight()

        # Obtener el ancho y la altura de la ventana
        ancho_ventana = 850 # Coloca aquí el ancho de tu ventana
        altura_ventana = 570 # Coloca aquí la altura de tu ventana

        # Calcular la posición x e y para que la ventana esté centrada
        posicion_x = int(ancho_pantalla / 2 - ancho_ventana / 2)
        posicion_y = int(altura_pantalla / 2 - altura_ventana / 2)

        # Establecer la posición de la ventana en el centro de la pantalla
        self.geometry("{}x{}+{}+{}".format(ancho_ventana, altura_ventana, posicion_x, posicion_y))

        # global state
        self.user_add_box = False
        self.user_del_box = False
        self.user_sel_box = True
        
        self.user_obstacle = False
        self.user_obstacle_size = 1

        self.last_shadow_box = None
        self.last_shadow_obs = None
        self.window_loading = None

        self.rendered_path = []
        self.obstacles_add = []
        self.obstacles_add.extend(obstacles)

        self.currentTagSelected = None
        self.current_coord_selected = (15, 10)

        self.is_loading = customtkinter.BooleanVar()
        self.is_loading.set(False)

        self.global_alpha = customtkinter.DoubleVar(value=0.1)
        self.global_gamma = customtkinter.DoubleVar(value=0.99)
        self.global_epsil = customtkinter.DoubleVar(value=0.1)
        self.global_episd = customtkinter.DoubleVar(value=10000)

        self.main_program()

    def main_program(self):
        # customtkinter.CTkLabel(master=self, text="Mapa").pack()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=3)

        self.canvas = customtkinter.CTkCanvas(
            master=self,
            width=CanvasSetting.SIZE_WIDTH,
            height=CanvasSetting.SIZE_HEIGHT,
            bg=CanvasSetting.BACKGROUND_COLOR
        )

        self.canvas.bind('<Motion>', self.motion_action)
        self.canvas.bind('<Button-1>', self.click_on_canvas)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.canvas.grid(
            column=2,
            row=0, 
        )

        crearCuadricula(self.canvas)
        colocarCaja(self.canvas, 14, 8)

        self.img = img = ImageTk.PhotoImage(file=r'img\robot.png')
        self.canvas.create_image(45, 670,  image=img, anchor=customtkinter.NW)
        self.canvas.create_image(105, 670, image=img, anchor=customtkinter.NW)
        self.canvas.create_image(165, 670, image=img, anchor=customtkinter.NW)
        self.canvas.create_image(225, 670, image=img, anchor=customtkinter.NW)
        self.canvas.create_image(285, 670, image=img, anchor=customtkinter.NW)
        self.canvas.create_image(345, 670, image=img, anchor=customtkinter.NW)
        self.canvas.create_image(405, 670, image=img, anchor=customtkinter.NW)
        self.canvas.create_image(465, 670, image=img, anchor=customtkinter.NW)

        for obstacle in obstacles:
            x, l, y = obstacle
            colocarObstaculo(self.canvas, x, y, l - x)

        buttonFrame = customtkinter.CTkFrame(self, fg_color="white")

        frame_label_properties = LabelFrame(
            buttonFrame, 
            text="Propiedades del algoritmo", 
            bg="white", 
            fg="#2F2E2E", 
            padx=10, 
            pady=50, 
          
            font=tkFont.Font(size=12, weight="bold"))
        
        frame_label_insert = LabelFrame(
            buttonFrame, 
            text="Insertar elemento", 
            bg="white", 
            fg="#2F2E2E", 
            padx=50, 
            pady=50, 
            font=tkFont.Font(size=12, weight="bold"))
        
        frame_label_options = LabelFrame(
            buttonFrame, 
            text="Opciones de seleccion", 
            bg="white", 
            fg="#2F2E2E", 
            padx=50, 
            pady=50, 
            font=tkFont.Font(size=12, weight="bold"))
        

        frame_label_properties.columnconfigure(0, weight=1)
        frame_label_properties.columnconfigure(1, weight=1)
        frame_label_properties.columnconfigure(2, weight=1)
        frame_label_properties.columnconfigure(3, weight=1)

        frame_label_properties.rowconfigure(0, weight=1)
        frame_label_properties.rowconfigure(1, weight=1)

        
        button_delete = customtkinter.CTkButton(frame_label_options, text="❎ Borrar", command=self.delete_box,text_color="white", fg_color="#FF7C7C")
        button_adding = customtkinter.CTkButton(frame_label_insert, text="🛑  Destino", command=self.add_box, text_color="white", fg_color="#8F8FFA")
        button_obstac = customtkinter.CTkButton(frame_label_insert, text="🧱 Obstáculo", command=self.add_obstacle, text_color="white",fg_color="#8F8FFA")
        button_solved = customtkinter.CTkButton(buttonFrame, text="⭐ Buscar camino", command=self.search_path, text_color="white", fg_color="#7D7DE7")
        
        #labels del algoritmo de qlearning

        """
            alpha = 0.1
            gamma = 0.99
            epsilon = 0.1
            num_episodes = 10000
        """
        label_alpha = customtkinter.CTkLabel(frame_label_properties, text="alpha:")
        self.spinb_alpha = Spinbox(frame_label_properties, from_=0.1, to=0.5, buttonbackground="#8F8FFA", relief="solid", foreground="black", width=3, textvariable=self.global_alpha, font=("Arial", 10), increment=0.1)

        label_gamma = customtkinter.CTkLabel(frame_label_properties, text="gamma:")
        self.spinb_gamma = Spinbox(frame_label_properties, from_=0.90, to=0.99, buttonbackground="#8F8FFA", relief="solid", foreground="black", width=3, textvariable=self.global_gamma, font=("Arial", 10), increment=0.01)

        label_epsilon = customtkinter.CTkLabel(frame_label_properties, text="epsilon:")
        self.spinb_epsilon = Spinbox(frame_label_properties, from_=0, to=1, buttonbackground="#8F8FFA", relief="solid", foreground="black", width=3, increment=0.01, textvariable=self.global_epsil ,font=("Arial", 10))

        label_episodes = customtkinter.CTkLabel(frame_label_properties, text="episodios:")
        self.spinb_episodes = Spinbox(frame_label_properties, from_=1000, to=100000, buttonbackground="#8F8FFA", relief="solid", foreground="black", width=5, increment=1, textvariable=self.global_episd, font=("Arial", 10))

        label_alpha.grid(column = 0, row = 0, sticky="w", )
        self.spinb_alpha.grid(column=1, row=0, sticky="w", padx=10)

        label_gamma.grid(column = 2, row = 0, sticky="e", padx=15)
        self.spinb_gamma.grid(column=3, row=0, sticky="w")

        label_epsilon.grid(column = 0, row = 1, sticky="w", )
        self.spinb_epsilon.grid(column=1, row=1, sticky="w", padx=10)

        label_episodes.grid(column = 2, row = 1, sticky="e", padx=10)
        self.spinb_episodes.grid(column=3, row=1, sticky="w")

        #se añade al labelframe
        button_delete.pack()
        button_obstac.pack(pady=10)
        button_adding.pack()

        #el labelframe se añade al buttonframe
        frame_label_properties.pack(pady=10)
        frame_label_insert.pack(pady=10)
        frame_label_options.pack(pady=10)

        button_solved.pack(side="bottom", pady=10, fill="x", ipady=10)

        home_icon = getImageTk("img/instructions.png")
        info_icon = getImageTk("img/information.png")
        barFrame = customtkinter.CTkFrame(self, fg_color="#8F8FFA")

        button_home = customtkinter.CTkButton(barFrame, 
            text="", 
            image=home_icon, 
            fg_color="#8F8FFA", 
            hover_color="#6767D4", 
            width=19, 
            cursor="hand2",
            command=self.info)
        button_home.pack(pady=150)
        button_credits = customtkinter.CTkButton(barFrame, 
            text="", 
            image=info_icon, 
            fg_color="#8F8FFA", 
            hover_color="#6767D4", 
            width=19, 
            cursor="hand2",
            command=self.creditos)
        button_credits.pack()

        barFrame.grid(column=0, row=0, sticky="NS", ipadx=10)
        buttonFrame.grid(column=1, row=0, ipadx=10, padx=10, sticky="NS")

    """
        This function gets executed when user moves his mouse on the canvas
    """
    def motion_action(self, event):
        x = math.floor(event.x / 30)
        y = math.floor(event.y / 30)

        if self.user_add_box:
            self.canvas.delete(self.last_shadow_box)
            self.last_shadow_box = boxByReference(self.canvas, x, y)

        if self.user_obstacle:
            self.canvas.delete(self.last_shadow_obs)
            self.last_shadow_obs = obstacleReference(self.canvas, x, y, self.user_obstacle_size)

    """
        This function gets executed when user clicks on canvas
    """
    def click_on_canvas(self, event):
        x = math.floor(event.x / 30)
        y = math.floor(event.y / 30)

        current_id = self.canvas.find_withtag("current")
        curreng_tg = self.canvas.gettags(current_id)

        if self.user_sel_box:
            if "box" in curreng_tg and "current" in curreng_tg :
                coords = self.canvas.bbox(current_id)

                if self.currentTagSelected is None :  # CAMBIAR POR ID NO TAG
                    self.currentTagSelected = current_id
                    self.canvas.itemconfigure(current_id, fill='#E93251')
                else :
                    current_selected_tg = self.canvas.gettags(self.currentTagSelected)

                    if "obstacle" in current_selected_tg :
                        self.canvas.itemconfigure(self.currentTagSelected, fill='#34495E')
                    else :
                        self.canvas.itemconfigure(self.currentTagSelected, fill='#33A1FF')

                    self.canvas.itemconfigure(current_id, fill='#E93251')
                    self.currentTagSelected = current_id

        if self.user_add_box :
            if x > 21 :
                messagebox.showwarning(
                    title="Error",
                    message="No se pudo añadir el destino porque \n ya sobrepasó los limites del mapa.\n Por favor intente de nuevo."
                )
                self.user_add_box = True
            else :
                colocarCaja(self.canvas, x, y)
                self.user_add_box = False

        if self.user_obstacle:
            full_osbtacle_size = x + self.user_obstacle_size

            if full_osbtacle_size  > 23 :
                messagebox.showwarning(
                    title="Error",
                    message="No se puede añadir el obstáculo porque \n va a sobrepasar los limites del mapa.\n Por favor intente de nuevo."
                )
            else :
                colocarObstaculo(self.canvas, x, y, self.user_obstacle_size)
                self.user_obstacle = False
                self.obstacles_add = list(self.obstacles_add)
                self.obstacles_add.append((x, x + self.user_obstacle_size, y))
                self.obstacles_add = tuple(self.obstacles_add)

    def delete_box(self):
        if self.currentTagSelected :
            answer = askokcancel(
                title='Confirmación',
                message='Esta acción borrará la caja seleccionada. ¿Estás seguro?',
                icon=WARNING
            )

            if answer :
                selected_box = self.canvas.find_withtag(self.currentTagSelected)
                current_selected_tg = self.canvas.gettags(self.currentTagSelected)

                if "obstacle" in current_selected_tg :
                    coords = self.canvas.bbox(selected_box)
                    x_pos = int((coords[0] + 1) / 30)
                    span  = int((coords[2] + 1) / 30)
                    y_pos = int((coords[1] + 1) / 30)

                    tuple_seek = (x_pos, span, y_pos)
                    
                    for i, tupla in enumerate(self.obstacles_add) :
                        if tupla == tuple_seek :
                            lista_tupla = list(self.obstacles_add) 
                            lista_tupla.pop(i)  
                            self.obstacles_add = tuple(lista_tupla)
        
                self.canvas.delete(self.currentTagSelected)
        else :
            messagebox.showwarning(
                title="Borrar elemento", 
                message="No has seleccionado ningún objeto. Has click en un obstáculo u objetivo para eliminarlo.")

    """
        This function sets the global variable user_add_box to let click_on_cavas know if it has to draw a box instead of selecting an existent one
    """
    def add_box(self):
        self.user_add_box = True

    def is_a_valid_box_selected(self):
        selected_tags = self.canvas.gettags(self.currentTagSelected)

        if "obstacle" in selected_tags:
            return False
        
        return True

    def search_path(self):
        if self.currentTagSelected is None : 
            messagebox.showwarning(
                title="Borrar elemento", 
                message="No has seleccionado ningún objeto. Has click en objetivo para buscar caminos."
            )
            return

        if not self.is_a_valid_box_selected() : 
            return

        if self.rendered_path :
            self.clean_canvas()

        self.is_loading.set(True)

        self.window_loading = LoadingView(self.is_loading, self)
        self.window_loading.focus()  # if window exists focus it
       
        # Crear un hilo separado para ejecutar la función en paralelo
        t = threading.Thread(target=self.ejecutar_en_paralelo_async)
        t.start()

    """
        This function calls the searching path algorithtm and draws the result coordinates on the canvas
    """
    def ejecutar_en_paralelo_async(self):
        
        selected_box = self.canvas.find_withtag(self.currentTagSelected)
        coords = self.canvas.bbox(selected_box)

        alpha = float(self.spinb_alpha.get())
        gamma = float(self.spinb_gamma.get())
        epsilon = float(self.spinb_epsilon.get())
        episodes = int(self.spinb_episodes.get())

        x = coords[0] + 30
        y = coords[1] + 60

        goal_coord_x, goal_coord_y = int(x / 30 + 1), int(y / 30 + 1)
        goal_coords = (goal_coord_x, goal_coord_y)

        # r = 3
        # self.canvas.create_oval(x-r + 2, y-r + 2, x+r + 2, y+r + 2, fill="#33A1FF")
        inicio = time.time()

        # Llamar a la función para ejecutar en paralelo
        resultados = ejecutar_en_paralelo(goal_coords, self.obstacles_add, alpha, gamma, epsilon, episodes)

        # Tiempo total de ejecución
        tiempo_total = time.time() - inicio

        print(f"Tiempo total: {tiempo_total} segundos")

        self.is_loading.set(False)
 
        if self.window_loading :
            self.window_loading.destroy()

        # Imprimir los resultados obtenidos
        print("Resultados:")

        recompensas = []

        for resultado in resultados:
            recompensas.append(resultado)

        short_path = min(recompensas)

        # print(recompensas)
        print("El camino más corto es : ")

        print(short_path[1])

        messagebox.showinfo(
            title="Ruta mas corta encontrada", 
            message="A continuación se dibujará en el mapa la ruta más corta encontrada por el agente que corresponde"
        )

        ruta = short_path[1]

        self.draw_individual_path(ruta, True, "#33A1FF")

        self.toplevel_window = BotsView(recompensas, self.draw_individual_path, self)
        self.toplevel_window.focus()  # if window exists focus it
        
    def clean_canvas(self):
        for path_element in self.rendered_path:
            self.canvas.delete(path_element)

        self.rendered_path = []

    def on_button_release(self, event):
        # print("Mouse Up:", event.x, event.y)
        pass

    def add_obstacle(self):
        dialog = customtkinter.CTkInputDialog(
            text="Tamaño de obstáculo:", 
            title="Obstáculo"
        )

        self.user_obstacle = True    
        self.user_obstacle_size = int( dialog.get_input( ) )

        if self.user_obstacle_size > 21 :
            messagebox.showwarning(
                title="Error", 
                message="No se pudo añadir el obstáculo porque \n va a sobrepasar los limites del mapa.\n Por favor inserte un tamaño menor a 22."
            )
            self.user_obstacle = False
        else :
            pass

    def draw_individual_path(self, path, with_time = False, color =""):
        if self.rendered_path:
            self.clean_canvas()

        parejas = []
        ruta = path

        for i in range(len(ruta) - 1):
            par = (ruta[i], ruta[i + 1])
            parejas.append(par)

        for par in parejas:
            tupla1 = par[0]
            tupla2 = par[1]
            x1, y1 = tupla1
            x2, y2 = tupla2

            if with_time : self.after(50)

            line = createLine(self.canvas, x1, y1, x2, y2)
            x, y, r = x2 * 30, y2 * 30, 3
            # dot = createDot(self.canvas, x, y , r )
            self.rendered_path.append(line)
            # self.rendered_path.append(dot)
            
    def info (self):
        instrucciones = Instructions(self.is_loading, self)
        instrucciones.focus()  # if window exists focus it

    def creditos(self):
        credito = Credits(self.is_loading, self)
        credito.focus()  # if window exists focus it

if __name__ == "__main__":
    app = App()
    app.mainloop()

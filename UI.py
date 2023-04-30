import customtkinter
import math
from tkinter.messagebox import askokcancel, showinfo, WARNING
from PIL import Image, ImageTk
from utils.graphics import colocarCaja, crearCuadricula, colocarObstaculo, boxByReference, obstacleReference, createDot, createLine
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
        ancho_ventana = 560 # Coloca aquí el ancho de tu ventana
        altura_ventana = 690 # Coloca aquí la altura de tu ventana

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

        self.main_program()

    def main_program(self):
        customtkinter.CTkLabel(master=self, text="Mapa").pack()

        self.canvas = customtkinter.CTkCanvas(
            master=self,
            width=CanvasSetting.SIZE_WIDTH,
            height=CanvasSetting.SIZE_HEIGHT,
            bg=CanvasSetting.BACKGROUND_COLOR
        )

        self.canvas.bind('<Motion>', self.motion_action)
        self.canvas.bind('<Button-1>', self.click_on_canvas)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.canvas.pack(
            anchor=customtkinter.CENTER,
            expand=False
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
        buttonFrame.columnconfigure(0, weight=1)
        buttonFrame.columnconfigure(1, weight=1)
        buttonFrame.columnconfigure(2, weight=1)
        
        button_delete = customtkinter.CTkButton(buttonFrame, text="❎ Borrar selección", command=self.delete_box,text_color="white", )
        button_adding = customtkinter.CTkButton(buttonFrame, text="🛑 Añadir destino", command=self.add_box, text_color="white", )
        button_obstac = customtkinter.CTkButton(buttonFrame, text="🧱 Añadir obstáculo", command=self.add_obstacle, text_color="white",)
        button_solved = customtkinter.CTkButton(buttonFrame, text="⭐ Buscar camino", command=self.search_path, text_color="white", fg_color="#67DA75")
        button_instruc= customtkinter.CTkButton(buttonFrame, text="❔ Instrucciones", text_color="white", command=self.info, fg_color="#FD3E73")
        button_credits= customtkinter.CTkButton(buttonFrame, text="📋 Créditos", text_color="white", command=self.creditos, fg_color="#FD3E73")

        button_delete.grid(row=0, column=0, padx=10, pady=10)
        button_adding.grid(row=0, column=1, padx=10, pady=10)
        button_solved.grid(row=1, column=0, padx=10, pady=10)
        button_obstac.grid(row=0, column=2, padx=10, pady=10)
        button_instruc.grid(row=1, column=2, padx=10, pady=10)
        button_credits.grid(row=1, column=1, padx=10, pady=10)

        buttonFrame.pack(fill=customtkinter.X)

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

        x = coords[0] + 30
        y = coords[1] + 60

        goal_coord_x, goal_coord_y = int(x / 30 + 1), int(y / 30 + 1)
        goal_coords = (goal_coord_x, goal_coord_y)

        # r = 3
        # self.canvas.create_oval(x-r + 2, y-r + 2, x+r + 2, y+r + 2, fill="#33A1FF")
        inicio = time.time()

        # Llamar a la función para ejecutar en paralelo
        resultados = ejecutar_en_paralelo(goal_coords, self.obstacles_add)

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
            dot = createDot(self.canvas, x, y , r )
            self.rendered_path.append(line)
            self.rendered_path.append(dot)
            
    def info (self):
        instrucciones = Instructions(self.is_loading, self)
        instrucciones.focus()  # if window exists focus it

    def creditos(self):
        credito = Credits(self.is_loading, self)
        credito.focus()  # if window exists focus it

if __name__ == "__main__":
    app = App()
    app.mainloop()

import customtkinter
import math
from tkinter.messagebox import askokcancel, showinfo, WARNING
from PIL import Image, ImageTk
from utils.graphics import colocarCaja, crearCuadricula
from ia.GraphSearch import GraphSearch
from bd.mapa import map

#settings
from config.canvas import CanvasSetting
from config.app import AppConfig

#views
from views.config import SettingsView

#environment
from config.enviroment import *

class App(customtkinter.CTk):
    def __init__(self) :
        super().__init__()

        self.geometry(AppConfig.SIZE)
        self.configure(fg_color=AppConfig.BG_COLOR)
        self.resizable(False, False)
        self.title(AppConfig.TITLE)
   
        # global state
        self.user_add_box = False
        self.user_del_box = False
        self.user_sel_box = True
        
        self.currentTagSelected = None

        self.main_program()

    def main_program (self) :
        customtkinter.CTkLabel(master = self, text="Mapa").pack()
        
        self.canvas = customtkinter.CTkCanvas(
            master=self, 
            width=CanvasSetting.SIZE_WIDTH, 
            height=CanvasSetting.SIZE_HEIGHT, 
            bg=CanvasSetting.BACKGROUND_COLOR
        )
        
        self.canvas.bind('<Motion>', self.motion_action )
        self.canvas.bind('<Button-1>', self.click_on_canvas)
    
        self.canvas.pack(
            anchor=customtkinter.CENTER, 
            expand=False
        )

        crearCuadricula(self.canvas)
        colocarCaja(self.canvas, 14, 8)

        self.img = img = ImageTk.PhotoImage(file=r'img\robo.png')
        self.canvas.create_image(45, 670,image=img, anchor=customtkinter.NW)

        # as the project is not completed, buttons will be placed in a separated frame
        buttonFrame = customtkinter.CTkFrame(self, fg_color="white")
        buttonFrame.columnconfigure(0, weight=1)
        buttonFrame.columnconfigure(1, weight=1)
        buttonFrame.columnconfigure(2, weight=1)
        
        button_delete = customtkinter.CTkButton(buttonFrame, text="delete box", command=self.delete_box, text_color="white")
        button_adding = customtkinter.CTkButton(buttonFrame, text="add box", command=self.add_box, text_color="white")
        button_solved = customtkinter.CTkButton(buttonFrame, text="find path", command=self.search_path, text_color="white")

        button_delete.grid(row=0, column=0, padx=10, pady=10)
        button_adding.grid(row=0, column=1, padx=10, pady=10)
        button_solved.grid(row=0, column=2, padx=10, pady=10)

        buttonFrame.pack(fill=customtkinter.X)

        #end of button's frame
    """
        This function gets executed when user moves his mouse on the canvas
    """
    def motion_action(self, event):            
        # print(event.x / 30, event.y / 30, event.widget)
        pass
    """
        This function gets executed when user clicks on canvas
    """
    def click_on_canvas(self, event):
        x = math.floor(event.x / 30)
        y = math.floor(event.y / 30)
        
        current_id = self.canvas.find_withtag("current")
        curreng_tg = self.canvas.gettags(current_id)

        if self.user_sel_box :
            if "box" in curreng_tg and "current" in curreng_tg :
                coords = self.canvas.bbox(current_id)
                print(coords)

                if self.currentTagSelected is None : #CAMBIAR POR ID NO TAG
                    self.currentTagSelected = current_id
                    self.canvas.itemconfigure(current_id, fill='red')
                else :
                    self.canvas.itemconfigure(self.currentTagSelected, fill='#33A1FF')
                    self.canvas.itemconfigure(current_id, fill='red', outline ="red")
                    self.currentTagSelected = current_id

        if self.user_add_box :
            colocarCaja(self.canvas, x, y)
  
    def delete_box (self):
        answer = askokcancel(
            title='Confirmacion',
            message='Esta accion borrará la caja seleccionada. ¿Estas seguro?',
            icon = WARNING
        )
        # code for deleting a box ...

    """
        This function sets the global variable user_add_box to let click_on_cavas know if it has to draw a box instead of selecting an existent one
    """
    def add_box (self):

        pass
    
    """
        This function calls the searching path algorithtm and draws the result coordinates on the canvas
    """
    def search_path(self) :
        # x = vertical, y = horizonal
        start = (2, 23)
        end = (15, 10)
        search = GraphSearch(map, start, end)
        ruta = search.findPath() 

        parejas = []

        for i in range(len(ruta) - 1):
            par = (ruta[i], ruta[i+1])
            parejas.append(par)

        for par in parejas:
            tupla1 = par[0]
            tupla2 = par[1]
            x1, y1 = tupla1
            x2, y2 = tupla2
            
            self.canvas.create_line(x1*30 + 2, y1*30+2, x2*30 + 2, y2*30+2, width=3, fill="#33A1FF")  
            x, y, r = x2*30, y2*30, 3
            self.canvas.create_oval(x-r + 2, y-r + 2, x+r + 2, y+r + 2, fill="#33A1FF")
            
if __name__ == "__main__":
    app = App()
    app.mainloop()  
def colocarCaja(canvas, x, y, start=0, base=30):
  canvas.create_rectangle((start + x * base, start + y * base), (start + x * base + 60, start + y * base+60), fill='#33A1FF', outline='#33A1FF', tags = ("box","box{x}{y}"))

def boxByReference(canvas, x, y, start=0, base=30):
  return canvas.create_rectangle((start + x * base, start + y * base), (start + x * base + 60, start + y * base+60), fill='#b3dbff', outline='#b3dbff', tags = ("box","box{x}{y}"))

def colocarObstaculo(canvas, x, y, tam, start=0, base=30):
  canvas.create_rectangle((start + x * base, start + y * base), (start + x * base + tam*30, start + y * base+30), fill='#77554E', outline='#77554E', tags = ("box", "obstacle","box{x}{y}"))

def obstacleReference(canvas, x, y, tam, start=0, base=30):
  return canvas.create_rectangle((start + x * base, start + y * base), (start + x * base + tam*30, start + y * base+30), fill='#77554E', outline='#77554E', tags = ("box", "obstacle","box{x}{y}"))

def crearCuadricula(canvas):
  for i in range(30):
    canvas.create_line((0, 30 + (i * 30)), (700, 30 + (i * 30)),width=1, fill="#EBEBFC")  # horizontal
    canvas.create_line((30 + (i * 30), 0), (30 + (i * 30), 700), width=1, fill="#EBEBFC")  # vertical

def dibujarArista(canvas, x, y, size, base = 30):
  canvas.create_line(90, 100, 120, 100)
  # self.canvas.create_line(90, 180, 150, 180, width=3) #linea horizontal
  # self.canvas.create_line(180, 150, 180, 240, width=3) #linea vertical
  
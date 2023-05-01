from PIL import Image, ImageTk

def getImageTk(path): 
    image = Image.open(path)
    return ImageTk.PhotoImage(image)

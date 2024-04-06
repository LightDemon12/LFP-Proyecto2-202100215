from tkinter import Tk
from tkinter.filedialog import askopenfilename

def seleccionar_archivo():
    Tk().withdraw()  # Evita que se muestre una ventana vacía de Tkinter
    ruta_archivo = askopenfilename()  # Muestra un cuadro de diálogo para seleccionar un archivo
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()  # Leer el contenido del archivo
    return ruta_archivo, contenido
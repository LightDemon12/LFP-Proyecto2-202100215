from tkinter import Tk
from tkinter.filedialog import askopenfilename

def seleccionar_archivo():
    Tk().withdraw()  # Evita que se muestre una ventana vacía de Tkinter
    ruta_archivo = askopenfilename()  # Muestra un cuadro de diálogo para seleccionar un archivo
    return r'{}'.format(ruta_archivo)
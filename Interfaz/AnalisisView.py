import tkinter as tk
from tkinter import Menu, Text
from Logica.seleccion_archivo import seleccionar_archivo  # Importar la función seleccionar_archivo
from Logica.Guardar_archivo import guardar_como, guardar, nuevo  # Importar las funciones guardar_como, guardar y nuevo

def AnalisisView():
    ventana = tk.Tk()
    ventana.geometry('720x480')
    ventana.title('Área de análisis')  # Aquí se define el nombre de la ventana

    # Crear marco para el área de texto
    frame = tk.Frame(ventana)
    frame.grid(sticky='nsew', padx=50, pady=50)

    # Crear área de texto
    text_area = Text(frame)
    text_area.grid(sticky='nsew')

    # Crear barra de menú
    barra_menu = Menu(ventana)
    ventana.config(menu=barra_menu)

    # Función para abrir un archivo y cargar su contenido en el área de texto
    def abrir_archivo():
        global ruta_archivo  # Declarar ruta_archivo como global para que pueda ser accedida desde otras funciones
        ruta_archivo, contenido = seleccionar_archivo()  # Usar la función seleccionar_archivo
        text_area.delete('1.0', tk.END)  # Borrar el contenido actual del área de texto
        text_area.insert(tk.END, contenido)  # Insertar el contenido del archivo en el área de texto

    # Función para guardar el contenido del área de texto en un nuevo archivo
    def guardar_como_cmd():
        global ruta_archivo  # Declarar ruta_archivo como global para que pueda ser modificada desde esta función
        ruta_archivo = guardar_como(text_area)  # Usar la función guardar_como

    # Función para guardar el contenido del área de texto en el archivo actualmente abierto
    def guardar_cmd():
        guardar(text_area, ruta_archivo)  # Usar la función guardar

    # Función para crear un nuevo archivo
    def nuevo_cmd():
        global ruta_archivo  # Declarar ruta_archivo como global para que pueda ser modificada desde esta función
        ruta_archivo = nuevo(text_area, ruta_archivo)  # Usar la función nuevo

    # Crear opciones de menú
    archivo_menu = Menu(barra_menu, tearoff=0)
    archivo_menu.add_command(label="Nuevo", command=nuevo_cmd)
    archivo_menu.add_command(label="Guardar", command=guardar_cmd)
    archivo_menu.add_command(label="Abrir", command=abrir_archivo)  # Agregar la opción "Abrir" al menú
    archivo_menu.add_command(label="Guardar como", command=guardar_como_cmd)  # Agregar la opción "Guardar como" al menú
    archivo_menu.add_command(label="Salir", command=ventana.destroy)  # Cerrar el programa
    barra_menu.add_cascade(label="Archivo", menu=archivo_menu)
    
    # Configurar el grid
    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_rowconfigure(0, weight=1)

    # Configurar el grid del marco
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    ventana.mainloop()

if __name__ == "__main__":
    AnalisisView()
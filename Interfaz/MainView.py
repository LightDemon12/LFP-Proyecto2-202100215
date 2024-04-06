import tkinter as tk
from tkinter import Menu, Text
from Interfaz.TokensView import TokensView  # Importar la función TokensView
from Logica.seleccion_archivo import seleccionar_archivo  # Importar la función seleccionar_archivo

def MainView():
    ventana = tk.Tk()
    ventana.geometry('720x480')
    ventana.title('Área de código')  # Aquí se define el nombre de la ventana

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
        ruta_archivo, contenido = seleccionar_archivo()  # Usar la función seleccionar_archivo
        text_area.delete('1.0', tk.END)  # Borrar el contenido actual del área de texto
        text_area.insert(tk.END, contenido)  # Insertar el contenido del archivo en el área de texto
    # Crear opciones de menú
    archivo_menu = Menu(barra_menu, tearoff=0)
    archivo_menu.add_command(label="Nuevo")
    archivo_menu.add_command(label="Guardar")
    archivo_menu.add_command(label="Abrir", command=abrir_archivo)  # Agregar la opción "Abrir" al menú
    archivo_menu.add_command(label="Salir", command=ventana.quit)  # Cerrar el programa
    barra_menu.add_cascade(label="Archivo", menu=archivo_menu)





    # Agregar opción de menú para abrir la ventana TokensView
    def open_tokens_view():
        ventana.destroy()  # Cerrar la ventana MainView
        TokensView()  # Abrir la ventana TokensView

    barra_menu.add_command(label="Tokens", command=open_tokens_view)

    # Configurar el grid
    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_rowconfigure(0, weight=1)

    # Configurar el grid del marco
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    ventana.mainloop()

if __name__ == "__main__":
    MainView()
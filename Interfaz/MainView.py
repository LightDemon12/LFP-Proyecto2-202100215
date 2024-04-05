import tkinter as tk
from tkinter import Menu, Text
from Interfaz.TokensView import TokensView  # Importar la función TokensView

def MainView():
    ventana = tk.Tk()
    ventana.geometry('720x480')
    ventana.title('Área de código')  # Aquí se define el nombre de la ventana

    # Crear barra de menú
    barra_menu = Menu(ventana)
    ventana.config(menu=barra_menu)

    # Crear opciones de menú
    archivo_menu = Menu(barra_menu, tearoff=0)
    archivo_menu.add_command(label="Nuevo")
    archivo_menu.add_command(label="Abrir")
    archivo_menu.add_command(label="Guardar")
    archivo_menu.add_command(label="Salir", command=ventana.quit)
    barra_menu.add_cascade(label="Archivo", menu=archivo_menu)

    # Agregar opción de menú para abrir la ventana TokensView
    barra_menu.add_command(label="Tokens", command=TokensView)

    # Crear marco para el área de texto
    frame = tk.Frame(ventana)
    frame.grid(sticky='nsew', padx=50, pady=50)

    # Configurar el grid
    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_rowconfigure(0, weight=1)

    # Crear área de texto
    text_area = Text(frame)
    text_area.grid(sticky='nsew')

    # Configurar el grid del marco
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    ventana.mainloop()

if __name__ == "__main__":
    MainView()
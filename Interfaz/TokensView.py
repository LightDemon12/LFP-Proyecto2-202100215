import tkinter as tk
from tkinter import Menu, ttk

def TokensView():
    ventana = tk.Tk()
    ventana.geometry('720x480')
    ventana.title('Menú Tokens')  # Aquí se define el nombre de la ventana

    # Crear barra de menú
    barra_menu = Menu(ventana)
    ventana.config(menu=barra_menu)

    # Crear opciones de menú
    archivo_menu = Menu(barra_menu, tearoff=0)

    # Agregar opción de menú para regresar a la ventana MainView
    def open_main_view():
        ventana.destroy()  # Cerrar la ventana TokensView
        from Interfaz.MainView import MainView  # Importar la función MainView aquí
        MainView()  # Abrir la ventana MainView

    barra_menu.add_command(label="Regresar", command=open_main_view)

    # Crear marco para la tabla
    frame = tk.Frame(ventana)
    frame.grid(sticky='nsew', padx=50, pady=50)

    # Configurar el grid
    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_rowconfigure(0, weight=1)

    # Crear tabla
    tabla = ttk.Treeview(frame, columns=('Correlativo', 'Token', 'NumeroToken', 'Lexema', 'Columna', 'Fila'), show='headings')
    tabla.grid(sticky='nsew')

    # Configurar las columnas
    for column in ('Correlativo', 'Token', 'NumeroToken', 'Lexema', 'Columna', 'Fila'):
        tabla.heading(column, text=column)
        tabla.column(column, stretch=True, width=int(ventana.winfo_width() / 6))  # Hacer que la columna se ajuste al tamaño de la ventana

    # Configurar el grid del marco
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    # Configurar bordes entre cada fila
    tabla.tag_configure('oddrow', background='white')
    tabla.tag_configure('evenrow', background='lightgray')

    ventana.mainloop()

if __name__ == "__main__":
    TokensView()
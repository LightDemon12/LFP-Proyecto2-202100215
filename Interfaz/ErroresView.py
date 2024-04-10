import tkinter as tk
from tkinter import Menu, ttk
from Logica.Analizador_Lexico import errores

def ErroresView(errores):
    ventana = tk.Tk()
    ventana.geometry('1200x720')
    ventana.title('Menú Errores')

    barra_menu = Menu(ventana)
    ventana.config(menu=barra_menu)

    def open_main_view():
        ventana.destroy()
        from Interfaz.MainView import MainView
        MainView()

    barra_menu.add_command(label="Regresar", command=open_main_view)

    frame = tk.Frame(ventana)
    frame.grid(sticky='nsew', padx=50, pady=50)

    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_rowconfigure(0, weight=1)

    tabla = ttk.Treeview(frame, columns=('TipoError', 'Linea', 'Columna', 'TokenLexico', 'Descripcion'), show='headings')
    tabla.grid(sticky='nsew')

    for column in ('TipoError', 'Linea', 'Columna', 'TokenLexico', 'Descripcion'):
        tabla.heading(column, text=column)
        tabla.column(column, stretch=True, width=int(ventana.winfo_width() / 5), anchor='center')  # Añadir anchor='center'

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    tabla.tag_configure('oddrow', background='white')
    tabla.tag_configure('evenrow', background='lightgray')

    for error in errores:
        if error.tipo == 'LEXICO':
            descripcion = 'Descripción para error léxico'
        elif error.tipo == 'sintactico':
            descripcion = 'Descripción para error sintáctico'
        else:
            descripcion = 'Descripción para otros tipos de errores'
        tabla.insert('', 'end', values=(error.tipo, error.linea, error.columna, error.valor, descripcion))

    ventana.mainloop()  # Llamar a mainloop() una vez, después de haber insertado todos los errores

if __name__ == "__main__":
    ErroresView(errores)
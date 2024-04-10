import tkinter as tk
from tkinter import Menu, ttk
from Logica.Analizador_Lexico import palabras_procesadas
def TokensView(palabras_procesadas):
    ventana = tk.Tk()
    ventana.geometry('1200x720')
    ventana.title('Menú Tokens')

    barra_menu = Menu(ventana)
    ventana.config(menu=barra_menu)

    archivo_menu = Menu(barra_menu, tearoff=0)

    def open_main_view():
        from Interfaz.MainView import MainView
        ventana.destroy()
        MainView()

    barra_menu.add_command(label="Regresar", command=open_main_view)

    frame = tk.Frame(ventana)
    frame.grid(sticky='nsew', padx=50, pady=50)

    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_rowconfigure(0, weight=1)

    tabla = ttk.Treeview(frame, columns=('Correlativo', 'Token', 'NumeroToken', 'Lexema', 'Columna', 'Fila'), show='headings')
    tabla.grid(sticky='nsew')

    for column in ('Correlativo', 'Token', 'NumeroToken', 'Lexema', 'Columna', 'Fila'):
        tabla.heading(column, text=column)
        tabla.column(column, stretch=True, width=int(ventana.winfo_width() / 6))

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    tabla.tag_configure('oddrow', background='white')
    tabla.tag_configure('evenrow', background='lightgray')

    for i, palabra in enumerate(palabras_procesadas, start=1):
        tabla.insert('', 'end', values=(i, palabra.tipo, i, palabra.valor, palabra.columna, palabra.linea))

    ventana.mainloop()

if __name__ == "__main__":
    TokensView(palabras_procesadas)
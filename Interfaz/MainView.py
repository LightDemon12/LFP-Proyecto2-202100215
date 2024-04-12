import tkinter as tk
from tkinter import Menu, Text
import tkinter.messagebox as messagebox
from Interfaz.TokensView import TokensView  # Importar la función TokensView
from Interfaz.ErroresView import ErroresView  # Importar la función ErroresView
from Interfaz.AnalisisView import AnalisisView  # Importar la función MainView
from Logica.seleccion_archivo import seleccionar_archivo, get_contenido  # Importar la función seleccionar_archivo
from Logica.Guardar_archivo import guardar_como, guardar, nuevo  # Importar las funciones guardar_como, guardar y nuevo
from Logica.Analizador_Lexico import clasificar_palabra, leer_archivo, buscar_palabras_clave  # Importar las funciones clasificar_palabra y leer_archivo
from Logica.Analizador_Sintactico import Parser, generar_traduccion
from Logica.orden import leer_archivo_bson
  # Importar la función analizar_sintaxis
contenido_textarea = ""

def cargar_contenido_textarea():
    global contenido_textarea
    global text_area
    text_area.delete('1.0', tk.END)  # Borrar el contenido actual del área de texto
    text_area.insert(tk.END, contenido_textarea)  # Rellena el TextArea con el contenido guardado

def MainView():
    ventana = tk.Tk()
    ventana.geometry('1200x720')
    ventana.title('Área de código')  # Aquí se define el nombre de la ventana
    global contenido_textarea
    global text_area  # Hacer text_area una variable global

    # Crear marco para el área de texto
    frame = tk.Frame(ventana)
    frame.grid(sticky='nsew', padx=50, pady=50)

    # Crear área de texto
    text_area = Text(frame)
    text_area.grid(sticky='nsew')
    cargar_contenido_textarea()
    # Crear barra de menú
    barra_menu = Menu(ventana)
    ventana.config(menu=barra_menu)


    # Función para abrir un archivo y cargar su contenido en el área de texto
    def abrir_archivo():
        global ruta_archivo
        global contenido_textarea  # Acceder a contenido_textarea
        ruta_archivo, contenido = seleccionar_archivo()  # Usar la función seleccionar_archivo
        text_area.delete('1.0', tk.END)  # Borrar el contenido actual del área de texto
        text_area.insert(tk.END, contenido)  # Insertar el contenido del archivo en el área de texto
        contenido_textarea = contenido  # Actualizar contenido_textarea con el contenido del archivo
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

    # Agregar opción de menú para abrir la ventana TokensView
    def open_tokens_view():
        global contenido_textarea
        global text_area
        contenido_textarea = text_area.get("1.0", tk.END)
        print("Token presionado")
        palabras_procesadas, errores = leer_archivo(ruta_archivo)
        buscar_palabras_clave(palabras_procesadas, errores)
        # Imprimir las palabras procesadas
        print("Palabras procesadas:")
        for palabra in palabras_procesadas:
            print(f"Valor: {palabra.valor}, Tipo: {palabra.tipo}, Línea: {palabra.linea}, Columna: {palabra.columna}")
        
        # Imprimir los errores
        print("\nErrores:")
        for error in errores:
            print(f"Valor: {error.valor}, Tipo: {error.tipo}, Línea: {error.linea}, Columna: {error.columna}")
        ventana.destroy()  # Cerrar la ventana MainView
        TokensView(palabras_procesadas)  # Abrir la ventana TokensView con palabras_procesadas

    # Agregar opción de menú para abrir la ventana ErroresView
    def open_errores_view():
        global contenido_textarea
        global text_area
        contenido_textarea = text_area.get("1.0", tk.END)
        print("Token presionado")
        palabras_procesadas, errores = leer_archivo(ruta_archivo)
        buscar_palabras_clave(palabras_procesadas, errores)
        # Imprimir los errores
        print("\nErrores:")
        for error in errores:
            print(f"Valor: {error.valor}, Tipo: {error.tipo}, Línea: {error.linea}, Columna: {error.columna}")
        ventana.destroy()  # Cerrar la ventana MainView
        ErroresView(errores)  # Abrir la ventana ErroresView con errores

    def open_Analisis_view():
        global contenido_textarea
        global text_area
        global Errorsin  # Declaramos Errorsin como global
        global traduccion  # Declaramos traduccion como global
        contenido_textarea = text_area.get("1.0", tk.END)
        palabras_procesadas, errores = leer_archivo(ruta_archivo)  # Obtenemos las palabras procesadas
        if errores:  # Si la lista errores tiene objetos dentro
            show_error_and_destroy("Se encontraron errores léxicos. No se puede continuar con el análisis sintáctico.")
        else:
            parser = Parser(palabras_procesadas)  # Pasamos una referencia a la ventana MainView
            start_tokens = ['CrearBD', 'CrearColeccion']  # Lista de tokens que indican cuándo empezar a copiar
            try:
                temp_list = parser.extract_until_semicolon(start_tokens)
                parser.extract_commands()  # Llama a la nueva función extract_commands
            except ValueError as e:
                show_error_and_destroy(str(e))
                ErroresView(parser.Errorsin)  # Abre la vista de errores pasando la lista de errores
                return
            if parser.Errorsin:  # Si la lista Errorsin no está vacía (es decir, hay errores)
                show_error_and_destroy("Se encontraron errores sintácticos. Por favor, revisa la vista de errores.")
                ErroresView(parser.Errorsin)  # Abre la vista de errores pasando la lista de errores
            else:
                generar_traduccion(parser.traduccion, 'archivo_salida.BSON')  # Llama a la función generar_traduccion()
                # Llama a la función leer_archivo_bson después de generar la traducción
                estado_db, estado_colec, eliminar_db, eliminar_colec, errorestruc = leer_archivo_bson('archivo_salida.BSON')
                if errorestruc:  # Si la lista errorestruc tiene elementos
                    show_error_and_destroy("Se encontraron errores estructurales. Por favor, revisa la vista de errores.")
                    ErroresView(errorestruc)  # Abre la vista de errores pasando la lista de errores
                else:
                    ventana.destroy()
                    AnalisisView()

    def show_error_and_destroy(message):
        messagebox.showerror("Error", message)
        ventana.destroy()

    barra_menu.add_command(label="Tokens", command=open_tokens_view)
    barra_menu.add_command(label="Errores", command=open_errores_view)
    barra_menu.add_command(label="Analizar", command=open_Analisis_view)

    # Configurar el grid
    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_rowconfigure(0, weight=1)

    # Configurar el grid del marco
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    ventana.mainloop()

if __name__ == "__main__":
    MainView()
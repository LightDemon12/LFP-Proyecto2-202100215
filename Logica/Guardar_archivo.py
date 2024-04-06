from tkinter import filedialog, messagebox

def guardar_como(text_area):
    ruta_archivo = filedialog.asksaveasfilename(defaultextension=".txt")  # Abrir cuadro de diálogo de guardado de archivos
    contenido = text_area.get('1.0', 'end')  # Obtener el contenido del área de texto
    with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(contenido)  # Escribir el contenido en el archivo
    return ruta_archivo  # Devolver la ruta del archivo guardado

def guardar(text_area, ruta_archivo):
    contenido = text_area.get('1.0', 'end')  # Obtener el contenido del área de texto
    with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(contenido)  # Escribir el contenido en el archivo

def nuevo(text_area, ruta_archivo):
    if ruta_archivo:  # Si hay un archivo abierto
        if messagebox.askyesno("Guardar", "¿Desea guardar los cambios antes de crear un nuevo archivo?"):
            guardar(text_area, ruta_archivo)  # Guardar los cambios
    text_area.delete('1.0', 'end')  # Limpiar el área de texto
    return ruta_archivo  # Devolver la ruta del archivo actual
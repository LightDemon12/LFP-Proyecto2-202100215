from Logica.TokenModels import Token, Reservada, Instruccion, Numero, Palabra, CaracterEspecial, Error, Conexion
caracteres = []
def clasificar_palabra(palabra, linea_actual, columna_actual):
    caracteres_especiales = ['{', '}', ':', '"', ',', ';', '[', ']','=','.', '#']

    tipo_palabra = None
    linea_palabra = linea_actual
    columna_palabra = columna_actual
    
    for caracter in palabra:
        if caracter == '\n':
            linea_palabra += 1
            columna_palabra = 1
        else:
            if caracter in caracteres_especiales:
                caracteres.append((caracter, 'ESPECIAL', linea_palabra, columna_palabra))
            elif caracter.isalpha():
                caracteres.append((caracter, 'LETRA', linea_palabra, columna_palabra))
            elif caracter.isdigit():
                caracteres.append((caracter, 'DIGITO', linea_palabra, columna_palabra))
            else:
                caracteres.append((caracter, 'OTRO', linea_palabra, columna_palabra))
            columna_palabra += 1
    
    # Determinar el tipo de la palabra
    if palabra.startswith('"') and palabra.endswith('"'):
        tipo_palabra = 'CADENA'
    elif palabra.isalpha() and not palabra.isdigit():
        tipo_palabra = 'IDENTIFICADOR'
    elif palabra.isdigit():
        tipo_palabra = 'NUMERO'
    else:
        tipo_palabra = 'OTRO'

    return caracteres, tipo_palabra, linea_palabra, columna_palabra
palabras_procesadas = []
errores = []


def leer_archivo(ruta_archivo):
    palabras_reservadas = ["CrearBD", "EliminarBD", "CrearColeccion", "EliminarColeccion", "InsertarUnico", "ActualizarUnico", "EliminarUnico", "BuscarTodo", "BuscarUnico"]
    conexion = ["nueva", "elimina", "colec", "eliminacolec", "insertadoc", "$set", "todo"]
    caracteres_especiales = ['{', '}', ':', '"', ',', ';', '[', ']', '=', '.', '#', '(', ')', '=', '$', '”', '“','-', '/', '*']
    palabras_procesadas = []
    errores = []
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as file:
            contenido = file.read()
            palabra_actual = ''
            linea_actual = 1
            columna_actual = 1
            
            for caracter in contenido:
                if caracter == '\n':
                    linea_actual += 1
                    columna_actual = 1
                elif caracter in caracteres_especiales:
                    if palabra_actual:
                        if palabra_actual in palabras_reservadas:
                            palabras_procesadas.append(Reservada(palabra_actual, linea_actual, columna_actual - len(palabra_actual)))
                        elif palabra_actual.isdigit():
                            palabras_procesadas.append(Numero(palabra_actual, linea_actual, columna_actual - len(palabra_actual)))
                        elif palabra_actual in conexion:
                            palabras_procesadas.append(Conexion(palabra_actual, linea_actual, columna_actual - len(palabra_actual)))
                        else:
                            palabras_procesadas.append(Palabra(palabra_actual, linea_actual, columna_actual - len(palabra_actual)))
                        palabra_actual = ''
                    palabras_procesadas.append(CaracterEspecial(caracter, linea_actual, columna_actual))
                elif caracter.isalnum():
                    palabra_actual += caracter
                elif caracter.isspace():
                    if palabra_actual:
                        if palabra_actual in palabras_reservadas:
                            palabras_procesadas.append(Reservada(palabra_actual, linea_actual, columna_actual - len(palabra_actual)))
                        elif palabra_actual.isdigit():
                            palabras_procesadas.append(Numero(palabra_actual, linea_actual, columna_actual - len(palabra_actual)))
                        elif palabra_actual in conexion:
                            palabras_procesadas.append(Conexion(palabra_actual, linea_actual, columna_actual - len(palabra_actual)))
                        else:
                            palabras_procesadas.append(Palabra(palabra_actual, linea_actual, columna_actual - len(palabra_actual)))
                        palabra_actual = ''
                else:
                    errores.append(Error(caracter, 'LEXICO', linea_actual, columna_actual))
                columna_actual += 1
            
            if palabra_actual:
                if palabra_actual in palabras_reservadas:
                    palabras_procesadas.append(Reservada(palabra_actual, linea_actual, columna_actual - len(palabra_actual)))
                elif palabra_actual.isdigit():
                    palabras_procesadas.append(Numero(palabra_actual, linea_actual, columna_actual - len(palabra_actual)))
                elif palabra_actual in conexion:
                    palabras_procesadas.append(Conexion(palabra_actual, linea_actual, columna_actual - len(palabra_actual)))
                else:
                    palabras_procesadas.append(Palabra(palabra_actual, linea_actual, columna_actual - len(palabra_actual)))
                
            return palabras_procesadas, errores
    except FileNotFoundError:
        print("El archivo no se pudo encontrar.")
        return  None, None

def buscar_palabras_clave(palabras_procesadas, errores):
    palabras_clave = ["CrearBD", "CrearColeccion"]
    
    for palabra_clave in palabras_clave:
        encontrada = False
        for token in palabras_procesadas:
            if token.valor == palabra_clave:
                encontrada = True
                break
        if not encontrada:
            errores.append(Error(palabra_clave, 'NO ENCONTRADO', "NO EXISTE", "NO EXISTE"))
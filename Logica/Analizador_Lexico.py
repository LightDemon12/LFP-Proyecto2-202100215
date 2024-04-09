from Logica.TokenModels import CrearBD, EliminarBD, CrearColeccion, EliminarColeccion, InsertarUnico, ActualizarUnico, EliminarUnico, BuscarTodo, BuscarUnico, Texto, Equal, Colon, OpenBrace, CloseBrace, OpenParen, CloseParen, Semicolon, Quote, Comma

caracteres = []
palabras_procesadas = []
errores = []

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
                if caracter == '=':
                    caracteres.append(Equal(caracter, linea_palabra, columna_palabra))
                elif caracter == ':':
                    caracteres.append(Colon(caracter, linea_palabra, columna_palabra))
                elif caracter == '{':
                    caracteres.append(OpenBrace(caracter, linea_palabra, columna_palabra))
                elif caracter == '}':
                    caracteres.append(CloseBrace(caracter, linea_palabra, columna_palabra))
                elif caracter == '(':
                    caracteres.append(OpenParen(caracter, linea_palabra, columna_palabra))
                elif caracter == ')':
                    caracteres.append(CloseParen(caracter, linea_palabra, columna_palabra))
                elif caracter == ';':
                    caracteres.append(Semicolon(caracter, linea_palabra, columna_palabra))
                elif caracter == '"':
                    caracteres.append(Quote(caracter, linea_palabra, columna_palabra))
                elif caracter == ',':
                    caracteres.append(Comma(caracter, linea_palabra, columna_palabra))
            elif caracter.isalpha():
                if palabra == 'CrearBD':
                    palabras_procesadas.append(CrearBD(palabra, linea_palabra, columna_palabra))
                elif palabra == 'EliminarBD':
                    palabras_procesadas.append(EliminarBD(palabra, linea_palabra, columna_palabra))
                elif palabra == 'CrearColeccion':
                    palabras_procesadas.append(CrearColeccion(palabra, linea_palabra, columna_palabra))
                elif palabra == 'EliminarColeccion':
                    palabras_procesadas.append(EliminarColeccion(palabra, linea_palabra, columna_palabra))
                elif palabra == 'InsertarUnico':
                    palabras_procesadas.append(InsertarUnico(palabra, linea_palabra, columna_palabra))
                elif palabra == 'ActualizarUnico':
                    palabras_procesadas.append(ActualizarUnico(palabra, linea_palabra, columna_palabra))
                elif palabra == 'EliminarUnico':
                    palabras_procesadas.append(EliminarUnico(palabra, linea_palabra, columna_palabra))
                elif palabra == 'BuscarTodo':
                    palabras_procesadas.append(BuscarTodo(palabra, linea_palabra, columna_palabra))
                elif palabra == 'BuscarUnico':
                    palabras_procesadas.append(BuscarUnico(palabra, linea_palabra, columna_palabra))
                else:
                    palabras_procesadas.append(Texto(palabra, linea_palabra, columna_palabra))
            elif caracter.isdigit():
                palabras_procesadas.append(Texto(palabra, linea_palabra, columna_palabra))
            else:
                errores.append((caracter, 'OTRO', linea_palabra, columna_palabra))
            columna_palabra += 1

def leer_archivo(ruta_archivo):
    instrucciones = {
        "CrearBD": CrearBD,
        "EliminarBD": EliminarBD,
        "CrearColeccion": CrearColeccion,
        "EliminarColeccion": EliminarColeccion,
        "InsertarUnico": InsertarUnico,
        "ActualizarUnico": ActualizarUnico,
        "EliminarUnico": EliminarUnico,
        "BuscarTodo": BuscarTodo,
        "BuscarUnico": BuscarUnico
    }
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
                elif caracter in ['{', '}', ':', '"', ',', ';', '[', ']', '=', '.', '#']:
                    if palabra_actual:
                        if palabra_actual in instrucciones:
                            palabras_procesadas.append(instrucciones[palabra_actual](palabra_actual, linea_actual, columna_actual - len(palabra_actual)))
                        elif palabra_actual.isdigit():
                            palabras_procesadas.append(Texto(palabra_actual, linea_actual, columna_actual - len(palabra_actual)))
                        else:
                            palabras_procesadas.append(Texto(palabra_actual, linea_actual, columna_actual - len(palabra_actual)))
                        palabra_actual = ''
                    palabras_procesadas.append(Texto(caracter, linea_actual, columna_actual))
                elif caracter.isalnum():
                    palabra_actual += caracter
                elif caracter.isspace():
                    if palabra_actual:
                        if palabra_actual in instrucciones:
                            palabras_procesadas.append(instrucciones[palabra_actual](palabra_actual, linea_actual, columna_actual - len(palabra_actual)))
                        elif palabra_actual.isdigit():
                            palabras_procesadas.append(Texto(palabra_actual, linea_actual, columna_actual - len(palabra_actual)))
                        else:
                            palabras_procesadas.append(Texto(palabra_actual, linea_actual, columna_actual - len(palabra_actual)))
                        palabra_actual = ''
                else:
                    errores.append((caracter, 'TIPO_DE_ERROR', linea_actual, columna_actual))
                columna_actual += 1
            
            if palabra_actual:
                if palabra_actual in instrucciones:
                    palabras_procesadas.append(instrucciones[palabra_actual](palabra_actual, linea_actual, columna_actual - len(palabra_actual)))
                elif palabra_actual.isdigit():
                    palabras_procesadas.append(Texto(palabra_actual, linea_actual, columna_actual - len(palabra_actual)))
                else:
                    palabras_procesadas.append(Texto(palabra_actual, linea_actual, columna_actual - len(palabra_actual)))
                
            return palabras_procesadas, errores
    except FileNotFoundError:
        print("El archivo no se pudo encontrar.")
        return None, None
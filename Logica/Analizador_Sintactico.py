from Logica.TokenModels import Error
from Interfaz.ErroresView import ErroresView
import tkinter.messagebox as messagebox

Errorsin = []
traduccion = []


class Parser:
    def __init__(self, palabras_procesadas):
        self.palabras_procesadas = palabras_procesadas
        self.current_token_index = 0
        self.valid_first_token = False
        self.Errorsin = []
        self.traduccion = []
        self.check_first_token()

    def current_token(self):
        try:
            return self.palabras_procesadas[self.current_token_index]
        except IndexError:
            return None

    def check_first_token(self):
        first_token = self.current_token()
        if first_token is not None and first_token.valor in ['CrearBD', 'CrearColeccion']:
            self.valid_first_token = True

    def extract_until_semicolon(self, start_tokens):
        if not self.valid_first_token:
            raise ValueError("El primer token no es válido")

        commands = []
        temp_list = []
        start_copying = False

        i = 0
        while i < len(self.palabras_procesadas):
            token = self.palabras_procesadas[i]
            if token.valor in start_tokens:
                start_copying = True
            if start_copying:
                temp_list.append(self.palabras_procesadas.pop(i))  # Elimina el token de la lista original
                i -= 1  # Ajusta el índice para tener en cuenta el token eliminado
            if token.valor == ';':
                start_copying = False
                if temp_list:  # Solo añade temp_list a commands si no está vacía
                    commands.append(temp_list)
                temp_list = []
            i += 1

        for command in commands:
            if command[0].valor == 'CrearBD':
                self.verificar_sintaxis_crearbd(command)
            elif command[0].valor == 'CrearColeccion':
                self.verificar_sintaxis_crearcollection(command)
            # Agrega más condiciones aquí para otros tipos de comandos

        return commands

    def verificar_sintaxis_crearbd(self, command):
        # Define la secuencia esperada de valores de tokens, con None para segundo token
        sec_esper = ['CrearBD', None, '=', 'nueva', 'CrearBD', '(', ')', ';']

        # Comprueba si los valores de los tokens en el comando coinciden con la secuencia esperada
        for i, (token, valor_esper) in enumerate(zip(command, sec_esper)):
            if i == 1 and not token.valor:
                # Si el segundo token está vacío, añade un error a self.Errorsin
                self.Errorsin.append(f"Error de sintaxis en el comando CrearBD: {command}")
                print("Error de sintaxis en el comando CrearBD: el segundo token está vacío")
                return
            elif valor_esper is not None and token.valor != valor_esper:
                # Si el valor esperado no es None y no coincide con el valor del token, añade un error a self.Errorsin
                self.Errorsin.append(f"Error de sintaxis en el comando CrearBD: {command}")
                print("Error de sintaxis en el comando CrearBD")
                return

        # Si todos los tokens coinciden con la secuencia esperada, imprime el comando
        print([token.valor for token in command])
        print("No hay errores de sintaxis en el comando CrearBD")

        # Si no hay errores, añade la traducción a self.traduccion
        db_name = command[1].valor  # El nombre de la base de datos es el segundo token
        self.traduccion.append(f"use {db_name}")

    def verificar_sintaxis_crearcollection(self, command):
        # Aquí es donde verificarías la sintaxis del comando CrearColeccion
        # Por ahora, solo imprime el comando
        print([token.valor for token in command])


def generar_traduccion(traduccion, archivo_salida):
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write('use admin\n')  # Escribe 'use admin' al inicio del archivo
        for linea in traduccion:  # Para cada línea en la lista traduccion
            f.write(linea + '\n')  # Escribe la línea en el archivo


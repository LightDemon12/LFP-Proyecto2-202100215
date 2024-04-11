from Logica.TokenModels import Error
from Interfaz.ErroresView import ErroresView
import tkinter.messagebox as messagebox

Errorsin = []
traduccion = []


class Parser:
    def __init__(self, palabras_procesadas, main_view):
        # Filtramos los espacios en blanco y luego invertimos la lista para usarla como una pila
        self.palabras_procesadas = [token for token in palabras_procesadas if token.valor.strip() != ''][::-1]
        self.current_token = None
        self.has_errors = False
        self.main_view = main_view  # Guardamos una referencia a la ventana MainView
        self.next_token()

    def next_token(self):
        try:
            self.current_token = self.palabras_procesadas.pop()  # Usamos pop para sacar el último elemento de la pila
        except IndexError:
            self.current_token = None
            raise StopIteration  # Lanzamos una excepción cuando se llega al final de la lista de tokens
        
    def parse(self):
        while self.current_token is not None and self.current_token.valor != ';':  # Continuamos hasta que encontramos un ';' o no hay más tokens
            self.parse_statement()
        if self.has_errors:
            print("El análisis sintáctico tiene errores.")
        else:
            print("El análisis sintáctico se completó sin errores.")

    def parse_statement(self):
        if self.current_token is not None:
            if self.current_token.valor == 'CrearBD':
                self.parse_crearbd_statement()
            elif self.current_token.valor == 'CrearColeccion':
                self.parse_crearcollection_statement()
            else:  # Si el token no es 'CrearBD' ni 'CrearColeccion'
                messagebox.showerror("Error", f"Error: Se esperaba 'CrearBD' o 'CrearColeccion', pero se encontró {self.current_token.valor}. La estructura es inválida para su creación.")
                self.has_errors = True  # Marcamos que hubo un error
                Errorsin.append(Error(self.current_token.valor, 'SINTACTICO', self.current_token.linea, self.current_token.columna))
                self.main_view.destroy()  # Cerramos la ventana MainView
                ErroresView(Errorsin)  # Abrimos la ventana ErroresView con la lista de errores
                return  # Salimos de la función para evitar seguir analizando el resto de los tokens

    def parse_crearbd_statement(self):
        self.expect('CrearBD')  # Esperamos el token 'CrearBD'
        print(f"Coincidencia: {self.current_token.valor}")  # Imprimimos el token

        db_name = self.current_token.valor  # Guardamos el nombre de la base de datos
        print(f"Nombre de la base de datos: {db_name}")  # Imprimimos el nombre de la base de datos
        traduccion.append(f"use {db_name}")  # Agregamos 'use {db_name}' a la lista traduccion
        self.next_token()  # Avanzamos al siguiente token

        self.expect('=')  # Esperamos el token '='
        print(f"Coincidencia: {self.current_token.valor}")  # Imprimimos el token

        self.expect('nueva')  # Esperamos el token 'nueva'
        print(f"Coincidencia: {self.current_token.valor}")  # Imprimimos el token

        self.expect('CrearBD')  # Esperamos el token 'CrearBD'
        print(f"Coincidencia: {self.current_token.valor}")  # Imprimimos el token

        self.expect('(')  # Esperamos el token '('
        print(f"Coincidencia: {self.current_token.valor}")  # Imprimimos el token

        self.expect(')')  # Esperamos el token ')'
        print(f"Coincidencia: {self.current_token.valor}")  # Imprimimos el token

        self.expect(';')  # Esperamos el token ';'
        print(f"Coincidencia: {self.current_token.valor}")  # Imprimimos el token
        return  # Salimos de la función después de encontrar el ';'


    def parse_crearcollection_statement(self):
        # Aquí irá tu código para analizar la declaración 'CrearColeccion'
        pass


    def expect(self, token_valor):
        if self.current_token.valor == token_valor:
            if token_valor == ';':  # Si el token es ';', salimos de la función
                return
            self.next_token()  # Avanzamos al siguiente token
        else:
            print(f"Error: Se esperaba {token_valor}, pero se encontró {self.current_token.valor}")
            self.has_errors = True  # Marcamos que hubo un error
            error = Error(self.current_token.valor, 'SINTACTICO', self.current_token.linea, self.current_token.columna)
            Errorsin.append(error)
            print(f"Objeto Error creado: Valor: {error.valor}, Tipo: {error.tipo}, Línea: {error.linea}, Columna: {error.columna}")
            if self.current_token.valor != ';':  # Solo avanzamos al siguiente token si el token actual no es ';'
                self.next_token()  # Avanzamos al siguiente token a pesar del error

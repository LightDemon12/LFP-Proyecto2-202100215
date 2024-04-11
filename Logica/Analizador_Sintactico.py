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
        self.Errorsin = []
        self.traduccion = []
        self.first_token = None
        self.next_token()

    def process_stack(self):
        if self.current_token is not None:
            self.parse_statement()
            # Programamos la próxima llamada a process_stack para que se ejecute después de un retraso de 100 milisegundos
            self.main_view.after(100, self.process_stack)
        else:
            # Aquí puedes poner cualquier código que quieras que se ejecute después de que se haya procesado toda la pila
            if self.has_errors:
                print("El análisis sintáctico tiene errores.")
            else:
                print("El análisis sintáctico se completó sin errores.")

    def parse(self):
        # Iniciamos el procesamiento de la pila
        self.process_stack()

    def next_token(self):
        try:
            self.current_token = self.palabras_procesadas.pop()  # Usamos pop para sacar el último elemento de la pila
        except IndexError:
            self.current_token = None
            raise StopIteration  # Lanzamos una excepción cuando se llega al final de la lista de tokens
        


    def parse_statement(self):
        while self.current_token is not None:  # Continuamos mientras haya tokens por procesar
            if self.first_token is None:  # Si es el primer token
                if self.current_token.valor not in ['CrearBD', 'CrearColeccion']:  # Si el primer token no es 'CrearBD' ni 'CrearColeccion'
                    messagebox.showerror("Error", f"Error: Se esperaba 'CrearBD' o 'CrearColeccion' como primer token, pero se encontró {self.current_token.valor}. La estructura es inválida para su creación.")
                    self.has_errors = True  # Marcamos que hubo un error
                    Errorsin.append(Error(self.current_token.valor, 'SINTACTICO', self.current_token.linea, self.current_token.columna))
                    self.main_view.destroy()  # Cerramos la ventana MainView
                    ErroresView(Errorsin)  # Abrimos la ventana ErroresView con la lista de errores
                else:
                    self.first_token = self.current_token.valor  # Guardamos el primer token
                    self.next_token()  # Avanzamos al siguiente token
            elif self.current_token.valor == 'CrearBD':
                self.parse_crearbd_statement()
            elif self.current_token.valor == 'CrearColeccion':
                self.parse_crearcollection_statement()
            elif self.current_token.valor == 'EliminarBD':
                self.parse_eliminarbd_statement()
            elif self.current_token.valor == 'EliminarColeccion':
                self.parse_eliminarcoleccion_statement()
            elif self.current_token.valor == 'InsertarUnico':
                self.parse_insertarunico_statement()
            elif self.current_token.valor == 'ActualizarUnico':
                self.parse_actualizarunico_statement()
            elif self.current_token.valor == 'EliminarUnico':
                self.parse_eliminarunico_statement()
            elif self.current_token.valor == 'BuscarTodo':
                self.parse_buscartodo_statement()
            elif self.current_token.valor == 'BuscarUnico':
                self.parse_buscarunico_statement()
            else:  # Si el token no es ninguno de los anteriores
                if len(self.palabras_procesadas) == 0:  # Si no hay más tokens
                    break  # Detenemos la función
                else:
                    self.next_token()  # Avanzamos al siguiente token

    def parse_crearbd_statement(self):
        self.expect('CrearBD')  # Esperamos el token 'CrearBD'
        print(f"Coincidencia: {self.current_token.valor}")  # Imprimimos el token

        db_name = self.current_token.valor  # Guardamos el nombre de la base de datos
        print(f"Nombre de la base de datos: {db_name}")  # Imprimimos el nombre de la base de datos
        self.traduccion.append(f"use {db_name}")  # Agregamos 'use {db_name}' a la lista traduccion
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
        self.parse_statement() 
        return  # Salimos de la función después de encontrar el ';'
    


    def parse_crearcollection_statement(self):
        self.next_token()  # Avanzamos al siguiente token, que debería ser 'colec'
        if self.current_token.valor != 'colec':
            self.Errorsin.append(f"Error de sintaxis: se esperaba 'colec', pero se obtuvo {self.current_token.valor}")
            return

        self.next_token()  # Avanzamos al siguiente token, que debería ser '='
        if self.current_token.valor != '=':
            self.Errorsin.append(f"Error de sintaxis: se esperaba '=', pero se obtuvo {self.current_token.valor}")
            return

        self.next_token()  # Avanzamos al siguiente token, que debería ser 'nueva'
        if self.current_token.valor != 'nueva':
            self.Errorsin.append(f"Error de sintaxis: se esperaba 'nueva', pero se obtuvo {self.current_token.valor}")
            return

        self.next_token()  # Avanzamos al siguiente token, que debería ser 'CrearColeccion'
        if self.current_token.valor != 'CrearColeccion':
            self.Errorsin.append(f"Error de sintaxis: se esperaba 'CrearColeccion', pero se obtuvo {self.current_token.valor}")
            return

        self.next_token()  # Avanzamos al siguiente token, que debería ser '('
        if self.current_token.valor != '(':
            self.Errorsin.append(f"Error de sintaxis: se esperaba '(', pero se obtuvo {self.current_token.valor}")
            return

        self.next_token()  # Avanzamos al siguiente token, que debería ser el nombre de la colección
        collection_name = self.current_token.valor  # Guardamos el nombre de la colección
        self.traduccion.append(f"db.createCollection('{collection_name}')")  # Agregamos la traducción a la lista

        self.next_token()  # Avanzamos al siguiente token, que debería ser ')'
        if self.current_token.valor != ')':
            self.Errorsin.append(f"Error de sintaxis: se esperaba ')', pero se obtuvo {self.current_token.valor}")
            return

        self.next_token()  # Avanzamos al siguiente token, que debería ser ';'
        if self.current_token.valor != ';':
            self.Errorsin.append(f"Error de sintaxis: se esperaba ';', pero se obtuvo {self.current_token.valor}")
            return

        self.next_token()  # Avanzamos al siguiente token

    def parse_eliminarbd_statement(self):
        self.expect('EliminarBD')  # Esperamos el token 'EliminarBD'
        while self.current_token.valor != ';':  # Continuamos hasta que encontramos ';'
            print(f"Token: {self.current_token.valor}")  # Imprimimos el token
            self.next_token()  # Avanzamos al siguiente token

    def parse_eliminarcoleccion_statement(self):
        self.expect('EliminarColeccion')  # Esperamos el token 'EliminarColeccion'
        while self.current_token.valor != ';':  # Continuamos hasta que encontramos ';'
            print(f"Token: {self.current_token.valor}")  # Imprimimos el token
            self.next_token()  # Avanzamos al siguiente token

    def parse_insertarunico_statement(self):
        self.expect('InsertarUnico')  # Esperamos el token 'InsertarUnico'
        while self.current_token.valor != ';':  # Continuamos hasta que encontramos ';'
            print(f"Token: {self.current_token.valor}")  # Imprimimos el token
            self.next_token()  # Avanzamos al siguiente token

    def parse_actualizarunico_statement(self):
        self.expect('ActualizarUnico')  # Esperamos el token 'ActualizarUnico'
        while self.current_token.valor != ';':  # Continuamos hasta que encontramos ';'
            print(f"Token: {self.current_token.valor}")  # Imprimimos el token
            self.next_token()  # Avanzamos al siguiente token

    def parse_eliminarunico_statement(self):
        self.expect('EliminarUnico')  # Esperamos el token 'EliminarUnico'
        while self.current_token.valor != ';':  # Continuamos hasta que encontramos ';'
            print(f"Token: {self.current_token.valor}")  # Imprimimos el token
            self.next_token()  # Avanzamos al siguiente token

    def parse_buscartodo_statement(self):
        self.expect('BuscarTodo')  # Esperamos el token 'BuscarTodo'
        while self.current_token.valor != ';':  # Continuamos hasta que encontramos ';'
            print(f"Token: {self.current_token.valor}")  # Imprimimos el token
            self.next_token()  # Avanzamos al siguiente token

    def parse_buscarunico_statement(self):
        self.expect('BuscarUnico')  # Esperamos el token 'BuscarUnico'
        while self.current_token.valor != ';':  # Continuamos hasta que encontramos ';'
            print(f"Token: {self.current_token.valor}")  # Imprimimos el token
            self.next_token()  # Avanzamos al siguiente token

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


def generar_traduccion(traduccion, archivo_salida):
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write('use admin\n')  # Escribe 'use admin' al inicio del archivo
        for linea in traduccion:  # Para cada línea en la lista traduccion
            f.write(linea + '\n')  # Escribe la línea en el archivo


class Parser:
    def __init__(self, palabras_procesadas):
        # Filtramos los espacios en blanco y luego invertimos la lista para usarla como una pila
        self.palabras_procesadas = [token for token in palabras_procesadas if token.valor.strip() != ''][::-1]
        self.current_token = None
        self.has_errors = False
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
        if self.current_token is not None and self.current_token.valor == 'CrearBD':
            self.parse_crearbd_statement()

    def parse_crearbd_statement(self):
        self.expect('CrearBD')  # Esperamos el token 'CrearBD'
        print(f"Coincidencia: {self.current_token.valor}")  # Imprimimos el token

        db_name = self.current_token.valor  # Guardamos el nombre de la base de datos
        print(f"Nombre de la base de datos: {db_name}")  # Imprimimos el nombre de la base de datos
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

    def expect(self, token_valor):
        if self.current_token.valor == token_valor:
            print(f"Coincidencia: {self.current_token.valor}")  # Imprimimos el token
            if token_valor == ';':  # Si el token es ';', salimos de la función
                return
            self.next_token()  # Avanzamos al siguiente token
        else:
            print(f"Error: Se esperaba {token_valor}, pero se encontró {self.current_token.valor}")
            self.has_errors = True  # Marcamos que hubo un error
            if self.current_token.valor != ';':  # Solo avanzamos al siguiente token si el token actual no es ';'
                self.next_token()  # Avanzamos al siguiente token a pesar del error
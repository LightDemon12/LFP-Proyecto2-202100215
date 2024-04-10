class Token:
    def __init__(self, valor, tipo, linea, columna):
        self.valor = valor
        self.tipo = tipo
        self.linea = linea
        self.columna = columna

class Reservada(Token):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'RESERVADA', linea, columna)

class Instruccion(Token):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'INSTRUCCION', linea, columna)

class Numero(Token):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'NUMERO', linea, columna)

class Palabra(Token):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'PALABRA', linea, columna)

class CaracterEspecial(Token):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'CARACTER_ESPECIAL', linea, columna)
        
class Conexion(Token):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'CONEXION', linea, columna)

class Error:
    def __init__(self, valor, tipo, linea, columna):
        self.valor = valor
        self.tipo = tipo
        self.linea = linea
        self.columna = columna

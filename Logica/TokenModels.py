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

    def __str__(self):
        return f"Palabra(valor={self.valor}, linea={self.linea}, columna={self.columna})"

    def __repr__(self):
        return self.__str__()
class CaracterEspecial(Token):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'CARACTER_ESPECIAL', linea, columna)

    def __str__(self):
        return f"CaracterEspecial(valor={self.valor}, linea={self.linea}, columna={self.columna})"

    def __repr__(self):
        return self.__str__()
        
class Conexion(Token):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'CONEXION', linea, columna)

class Error:
    def __init__(self, valor, tipo, linea, columna):
        self.valor = valor
        self.tipo = tipo
        self.linea = linea
        self.columna = columna

class MiBase:
    def __init__(self, nombre_unico, valor_booleano, tipo, indice):
        self.nombre_unico = nombre_unico
        self.valor_booleano = valor_booleano
        self.tipo = tipo
        self.indice = indice

class MiBase2:
    def __init__(self, nombre_unico, valor_booleano, tipo):
        self.nombre_unico = nombre_unico
        self.valor_booleano = valor_booleano
        self.tipo = tipo

class Cadena:
    def __init__(self, valor):
        self.valor = valor

    def __str__(self):
        return 'Cadena(' + self.valor + ')'

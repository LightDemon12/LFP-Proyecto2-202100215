class Token:
    def __init__(self, valor, tipo, linea, columna):
        self._valor = valor
        self._tipo = tipo
        self.linea = linea
        self.columna = columna

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, valor):
        self._valor = valor

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, tipo):
        self._tipo = tipo

class Instruccion(Token):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'INSTRUCCION', linea, columna)

class CrearBD(Instruccion):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'CREARBD', linea, columna)

class EliminarBD(Instruccion):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'ELIMINARBD', linea, columna)

class CrearColeccion(Instruccion):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'CREARCOLECCION', linea, columna)

class EliminarColeccion(Instruccion):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'ELIMINARCOLECCION', linea, columna)

class InsertarUnico(Instruccion):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'INSERTARUNICO', linea, columna)

class ActualizarUnico(Instruccion):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'ACTUALIZARUNICO', linea, columna)

class EliminarUnico(Instruccion):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'ELIMINARUNICO', linea, columna)

class BuscarTodo(Instruccion):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'BUSCARTODO', linea, columna)

class BuscarUnico(Instruccion):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'BUSCARUNICO', linea, columna)

class Texto(Token):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'TEXTO', linea, columna)

class Simbolo(Token):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'SIMBOLO', linea, columna)

class Equal(Simbolo):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'EQUAL', linea, columna)

class Colon(Simbolo):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'COLON', linea, columna)

class OpenBrace(Simbolo):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'OPENBRACE', linea, columna)

class CloseBrace(Simbolo):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'CLOSEBRACE', linea, columna)

class OpenParen(Simbolo):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'OPENPAREN', linea, columna)

class CloseParen(Simbolo):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'CLOSEPAREN', linea, columna)

class Semicolon(Simbolo):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'SEMICOLON', linea, columna)

class Quote(Simbolo):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'QUOTE', linea, columna)

class Comma(Simbolo):
    def __init__(self, valor, linea, columna):
        super().__init__(valor, 'COMMA', linea, columna)
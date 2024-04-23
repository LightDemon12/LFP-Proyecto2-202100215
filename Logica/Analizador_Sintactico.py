from Logica.TokenModels import Error, MiBase2, Cadena
from Interfaz.ErroresView import ErroresView
import tkinter.messagebox as messagebox

Errorsin = []
traduccion = []
Estado = []

class Parser:
    def __init__(self, palabras_procesadas):
        self.palabras_procesadas = palabras_procesadas
        self.current_token_index = 0
        self.valid_first_token = False
        self.Errorsin = []
        self.traduccion = []
        self.Estado = []
        self.check_first_token()
        self.por_procesar = []
    def current_token(self):
        try:
            return self.palabras_procesadas[self.current_token_index]
        except IndexError:
            return None

    def check_first_token(self):
        first_token = self.current_token()
        if first_token is not None and first_token.valor in ['CrearBD', 'CrearColeccion']:
            self.valid_first_token = True
        else:
            # Si el primer token no es 'CrearBD' o 'CrearColeccion', crea un objeto Error
            error = Error("inexistente", "SINTACTICO", first_token.linea, first_token.columna)
            self.Errorsin.append(error)

    def extract_until_semicolon(self, start_tokens):
        if not self.valid_first_token:
            raise ValueError("Estructura de comando no válida")

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

    def check_any_token(self):
        for token in self.palabras_procesadas:
            if token.valor in ['EliminarBD', 'EliminarColeccion', 'InsertarUnico', 'ActualizarUnico', 'EliminarUnico', 'BuscarTodo', 'BuscarUnico']:
                return True
        return False

    def extract_commands(self):
        if not self.check_any_token():
            return False

        commands = []
        temp_list = []
        start_copying = False

        i = 0
        while i < len(self.palabras_procesadas):
            token = self.palabras_procesadas[i]
            if token.valor in ['EliminarBD', 'EliminarColeccion', 'InsertarUnico', 'ActualizarUnico', 'EliminarUnico', 'BuscarTodo', 'BuscarUnico']:
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
            if command[0].valor == 'EliminarBD':
                self.verificar_sintaxis_eliminarbd(command)
            elif command[0].valor == 'EliminarColeccion':
                self.verificar_sintaxis_eliminarcollection(command)
            elif command[0].valor == 'InsertarUnico':
                self.verificar_sintaxis_insertarunico(command)
            elif command[0].valor == 'ActualizarUnico':
                self.verificar_sintaxis_actualizarunico(command)
            elif command[0].valor == 'EliminarUnico':
                self.verificar_sintaxis_eliminarunico(command)
            elif command[0].valor == 'BuscarTodo':
                self.verificar_sintaxis_buscartodo(command)
            elif command[0].valor == 'BuscarUnico':
                self.verificar_sintaxis_buscarunico(command)

        return commands



    def verificar_sintaxis_crearbd(self, command):
        # Define la secuencia esperada de valores de tokens, con None para segundo token
        sec_esper = ['CrearBD', None, '=', 'nueva', 'CrearBD', '(', ')', ';']

        # Comprueba si los valores de los tokens en el comando coinciden con la secuencia esperada
        for i, (token, valor_esper) in enumerate(zip(command, sec_esper)):
            if i == 1 and not token.valor:
                # Si el segundo token está vacío, añade un error a self.Errorsin
                error = Error("SINTACTICO", token.linea, token.columna, "El segundo token está vacío")
                self.Errorsin.append(error)
                print("Error de sintaxis en el comando CrearBD: el segundo token está vacío")
                return
            elif valor_esper is not None and token.valor != valor_esper:
                # Si el valor esperado no es None y no coincide con el valor del token, añade un error a self.Errorsin
                error = Error(token.valor, "SINTACTICO", token.linea, token.columna)
                self.Errorsin.append(error)
                print("Error de sintaxis en el comando CrearBD")
                return

        # Si todos los tokens coinciden con la secuencia esperada, imprime el comando
        print("No hay errores de sintaxis en el comando CrearBD")

        # Si no hay errores, añade la traducción a self.traduccion
        db_name = command[1].valor  # El nombre de la base de datos es el segundo token

        # Verifica si ya existe un objeto con el mismo db_name en la lista Estado y su valor booleano es True
        for estado_objeto in self.Estado:
            if estado_objeto.nombre_unico == db_name:
                if estado_objeto.valor_booleano:
                    error = Error(db_name, "ESTRUCTURA DUPLICADA", token.linea, token.columna)
                    self.Errorsin.append(error)
                    print("Error: Estructura duplicada")
                    return
                else:
                    estado_objeto.valor_booleano = True
                    print("El valor booleano ha sido cambiado a True")
                    return

        self.traduccion.append(f"use {db_name}")

        # Crea un objeto con el nombre de la base de datos, el valor booleano True, y el tipo "DB", y lo añade a la lista Estado
        estado_objeto = MiBase2(db_name, True, "DB")
        self.Estado.append(estado_objeto)


    def verificar_sintaxis_crearcollection(self, command):
        # Define la secuencia esperada valores de tokens
        sec_es = ['CrearColeccion', 'colec', '=', 'nueva', 'CrearColeccion', '(', '“']

        # Comprueba si los valores de los tokens en el comando coinciden con la secuencia esperada
        for i, (token, valor_esper) in enumerate(zip(command, sec_es)):
            if valor_esper is not None and token.valor != valor_esper:
                # Si el valor esperado no es None y no coincide con el valor del token, añade un error a self.Errorsin
                error = Error(token.valor, "SINTACTICO", token.linea, token.columna)
                self.Errorsin.append(error)
                print(f"Error de sintaxis en el comando CrearColeccion en la posición {i+1}")
                return

        # Busca el token '”'
        try:
            start_quote_index = next(i for i, token in enumerate(command) if token.valor == '“')
            end_quote_index = next(i for i, token in enumerate(command) if token.valor == '”')
        except StopIteration:
            error = Error("SINTACTICO", command[-1].linea, command[-1].columna, "Falta el token '”'")
            self.Errorsin.append(error)
            print("Error de sintaxis en el comando CrearColeccion: falta el token '”'")
            return

        # Recoge todos los tokens entre '“' y '”'
        tokens_between_quotes = command[start_quote_index+1:end_quote_index]

        # Comprueba los tokens después de '”'
        sec_es_after_quote = [')', ';']
        for i, (token, valor_esper) in enumerate(zip(command[end_quote_index+1:], sec_es_after_quote), start=end_quote_index+1):
            if token.valor != valor_esper:
                error = Error(token.valor, "SINTACTICO", token.linea, token.columna)
                self.Errorsin.append(error)
                print(f"Error de sintaxis en el comando CrearColeccion en la posición {i+1}")
                return

        # Si todos los tokens coinciden con la secuencia esperada, imprime el comando
        print("No hay errores de sintaxis en el comando CrearColeccion")

        # Crea un objeto con la estructura deseada y lo añade a la lista traduccion
        tokens_string = ' '.join(token.valor for token in tokens_between_quotes)
        traduccion_object = f"db.createCollection('{tokens_string}');"
        self.traduccion.append(traduccion_object)

        # Verifica si ya existe un objeto con el mismo nombre de colección en la lista Estado y su valor booleano es True
        for estado_objeto in self.Estado:
            if estado_objeto.nombre_unico == tokens_string and estado_objeto.valor_booleano:
                error = Error(tokens_string, "ESTRUCTURA DUPLICADA", token.linea, token.columna)
                self.Errorsin.append(error)
                print("Error: Estructura duplicada")
                return
            elif estado_objeto.nombre_unico == tokens_string and not estado_objeto.valor_booleano:
                estado_objeto.valor_booleano = True
                print("El valor booleano ha sido cambiado a True")
                return

        # Crea un objeto con el nombre de la colección, el valor booleano True, y el tipo "Coleccion", y lo añade a la lista Estado
        estado_objeto = MiBase2(tokens_string, True, "Coleccion")
        self.Estado.append(estado_objeto)


    def verificar_sintaxis_eliminarbd(self, command):
        # Define la secuencia esperada de valores de tokens
        sec_es = ['EliminarBD', 'elimina', '=', 'nueva', 'EliminarBD', '(', ')', ';']

        # Comprueba si los valores de los tokens en el comando coinciden con la secuencia esperada
        for i, (token, valor_esper) in enumerate(zip(command, sec_es)):
            if valor_esper is not None and token.valor != valor_esper:
                # Si el valor esperado no es None y no coincide con el valor del token, añade un error a self.Errorsin
                error = Error(token.valor, "SINTACTICO", token.linea, token.columna)
                self.Errorsin.append(error)
                print(f"Error de sintaxis en el comando EliminarBD en la posición {i+1}")
                return

        # Comprueba si el comando y la secuencia esperada tienen la misma longitud
        if len(command) != len(sec_es):
            error = Error("SINTACTICO", command[-1].linea, command[-1].columna, "El número de tokens no coincide con la secuencia esperada")
            self.Errorsin.append(error)
            print("Error de sintaxis en el comando EliminarBD: el número de tokens no coincide con la secuencia esperada")
            return

        # Si todos los tokens coinciden con la secuencia esperada, imprime el comando
        print("No hay errores de sintaxis en el comando EliminarBD")

        # Añade 'db.dropDatabase();' a la lista traduccion
        self.traduccion.append('db.dropDatabase();')
        print("Se ha añadido 'db.dropDatabase();' a la lista traduccion")



    def verificar_sintaxis_eliminarcollection(self, command):
        # Define la secuencia esperada de valores de tokens
        sec_es = ['EliminarColeccion', 'eliminacolec', '=', 'nueva', 'EliminarColeccion', '(', '“']

        # Comprueba si los valores de los tokens en el comando coinciden con la secuencia esperada
        for i, (token, valor_esper) in enumerate(zip(command, sec_es)):
            if valor_esper is not None and token.valor != valor_esper:
                # Si el valor esperado no es None y no coincide con el valor del token, añade un error a self.Errorsin
                error = Error(token.valor, "SINTACTICO", token.linea, token.columna)
                self.Errorsin.append(error)
                print(f"Error de sintaxis en el comando EliminarColeccion en la posición {i+1}")
                return

        # Busca el token '”'
        try:
            start_quote_index = next(i for i, token in enumerate(command) if token.valor == '“')
            end_quote_index = next(i for i, token in enumerate(command) if token.valor == '”')
        except StopIteration:
            error = Error("SINTACTICO", command[-1].linea, command[-1].columna, "Falta el token '”'")
            self.Errorsin.append(error)
            print("Error de sintaxis en el comando EliminarColeccion: falta el token '”'")
            return

        # Recoge todos los tokens entre '“' y '”'
        tokens_between_quotes = command[start_quote_index+1:end_quote_index]

        # Comprueba los tokens después de '”'
        sec_es_after_quote = [')', ';']
        for i, (token, valor_esper) in enumerate(zip(command[end_quote_index+1:], sec_es_after_quote), start=end_quote_index+1):
            if token.valor != valor_esper:
                error = Error(token.valor, "SINTACTICO", token.linea, token.columna)
                self.Errorsin.append(error)
                print(f"Error de sintaxis en el comando EliminarColeccion en la posición {i+1}")
                return

        # Si todos los tokens coinciden con la secuencia esperada, imprime el comando
        print("No hay errores de sintaxis en el comando EliminarColeccion")

        # Crea un objeto con la estructura deseada y lo añade a la lista traduccion
        tokens_string = ' '.join(token.valor for token in tokens_between_quotes)
        traduccion_object = f"db.{tokens_string}.drop();"
        self.traduccion.append(traduccion_object)
        print("Objeto añadido a la lista traduccion: ", traduccion_object)




    def verificar_sintaxis_insertarunico(self, command):
        # Define la secuencia esperada de valores de tokens
        sec_es = ['InsertarUnico', 'insertadoc', '=', 'nueva', 'InsertarUnico', '(', '“']

        # Comprueba si los valores de los tokens en el comando coinciden con la secuencia esperada
        for i, (token, valor_esper) in enumerate(zip(command, sec_es)):
            if valor_esper is not None and token.valor != valor_esper:
                # Si el valor esperado no es None y no coincide con el valor del token, añade un error a self.Errorsin
                error = Error(token.valor, "SINTACTICO", token.linea, token.columna)
                self.Errorsin.append(error)
                print(f"Error de sintaxis en el comando InsertarUnico en la posición {i+1}")
                return

        # Busca el token '”'
        try:
            start_quote_index = next(i for i, token in enumerate(command) if token.valor == '“')
            end_quote_index = next(i for i, token in enumerate(command) if token.valor == '”')
        except StopIteration:
            error = Error("SINTACTICO", command[-1].linea, command[-1].columna, "Falta el token '”'")
            self.Errorsin.append(error)
            print("Error de sintaxis en el comando InsertarUnico: falta el token '”'")
            return

        # Recoge todos los tokens entre '“' y '”'
        tokens_between_quotes = command[start_quote_index+1:end_quote_index]

        # Busca el token '{'
        try:
            start_brace_index = next(i for i, token in enumerate(command) if token.valor == '{')
            end_brace_index = next(i for i, token in enumerate(command) if token.valor == '}')
        except StopIteration:
            error = Error("SINTACTICO", command[-1].linea, command[-1].columna, "Falta el token '}'")
            self.Errorsin.append(error)
            print("Error de sintaxis en el comando InsertarUnico: falta el token '}'")
            return

        # Recoge todos los tokens entre '{' y '}'
        tokens_between_braces = command[start_brace_index+1:end_brace_index]
        if tokens_between_braces:
            tokens_between_braces.pop(0)  # Elimina el primer elemento

        # Comprueba los tokens después de '}'
        sec_es_after_brace = ['”', ')', ';']
        for i, (token, valor_esper) in enumerate(zip(command[end_brace_index+1:], sec_es_after_brace), start=end_brace_index+1):
            if token.valor != valor_esper:
                error = Error(token.valor, "SINTACTICO", token.linea, token.columna)
                self.Errorsin.append(error)
                print(f"Error de sintaxis en el comando InsertarUnico en la posición {i+1}")
                return

        # Si todos los tokens coinciden con la secuencia esperada, imprime el comando
        print("No hay errores de sintaxis en el comando InsertarUnico")

        # Crea un objeto con la estructura deseada y lo añade a la lista traduccion
        collection_name = ' '.join(token.valor for token in tokens_between_quotes)

        # Procesa los tokens entre las llaves
        document = ''
        remove_next_item = False
        for i, token in enumerate(tokens_between_braces):
            if remove_next_item:
                remove_next_item = False
                continue
            elif token.valor == ',':
                document += ','
                remove_next_item = True
            elif token.valor == ':':
                document = document[:-1] + ':'
            else:
                document += token.valor

        traduccion_object = f"db.{collection_name}.insertOne({{{document}}});"
        self.traduccion.append(traduccion_object)
        print("Objeto añadido a la lista traduccion: ", traduccion_object)

    def verificar_sintaxis_actualizarunico(self, command):
        # Define la secuencia esperada de tokens
        sec_es = ['ActualizarUnico', 'actualizadoc', '=', 'nueva', 'ActualizarUnico', '(', '“']

        # Comprueba si los valores de los tokens en el comando coinciden con la secuencia esperada
        for i, (token, valor_esper) in enumerate(zip(command, sec_es)):
            if valor_esper is not None and token.valor != valor_esper:
                # Si el valor esperado no es None y no coincide con el valor del token, añade un error a self.Errorsin
                error = Error(token.valor, "SINTACTICO", token.linea, token.columna)
                self.Errorsin.append(error)
                print(f"Error de sintaxis en el comando ActualizarUnico en la posición {i+1}")
                return

        # Busca el token '”'
        try:
            start_quote_index = next(i for i, token in enumerate(command) if token.valor == '“')
            end_quote_index = next(i for i, token in enumerate(command) if token.valor == '”')
        except StopIteration:
            error = Error("SINTACTICO", command[-1].linea, command[-1].columna, "Falta el token '”'")
            self.Errorsin.append(error)
            print("Error de sintaxis en el comando ActualizarUnico: falta el token '”'")
            return

        # Recoge todos los tokens entre '“' y '”' que no sean espacios en blanco
        collection_name = ''.join(token.valor for token in command[start_quote_index+1:end_quote_index] if token.valor.strip())

        # Busca el token '{'
        try:
            start_brace_index = next(i for i, token in enumerate(command) if token.valor == '{')
        except StopIteration:
            error = Error("SINTACTICO", command[-1].linea, command[-1].columna, "Falta el token '{'")
            self.Errorsin.append(error)
            print("Error de sintaxis en el comando ActualizarUnico: falta el token '{'")
            return

        # Busca el segundo token '”'
        try:
            end_quote_index_2 = next(i for i, token in enumerate(command[start_brace_index:]) if token.valor == '”')
        except StopIteration:
            error = Error("SINTACTICO", command[-1].linea, command[-1].columna, "Falta el segundo token '”'")
            self.Errorsin.append(error)
            print("Error de sintaxis en el comando ActualizarUnico: falta el segundo token '”'")
            return

        # Recoge todos los tokens después de '{' y antes del segundo '”'
        tokens_after_brace = command[start_brace_index:start_brace_index+end_quote_index_2]

        # Crea un objeto con la estructura deseada y lo añade a la lista traduccion
        tokens_string = ''.join(token.valor for token in tokens_after_brace)
        traduccion_object = f"db.{collection_name}.updateOne({tokens_string})"
        self.traduccion.append(traduccion_object)
        print("Objeto añadido a la lista traduccion: ", traduccion_object)



    def verificar_sintaxis_eliminarunico(self, command):
        # Define la secuencia esperada de valores de tokens
        sec_es = ['EliminarUnico', 'eliminadoc', '=', 'nueva', 'EliminarUnico', '(', '“']

        # Comprueba si los valores de los tokens en el comando coinciden con la secuencia esperada
        for i, (token, valor_esper) in enumerate(zip(command, sec_es)):
            if valor_esper is not None and token.valor != valor_esper:
                # Si el valor esperado no es None y no coincide con el valor del token, añade un error a self.Errorsin
                error = Error(token.valor, "SINTACTICO", token.linea, token.columna)
                self.Errorsin.append(error)
                print(f"Error de sintaxis en el comando EliminarUnico en la posición {i+1}")
                return

        # Busca el token '”'
        try:
            start_quote_index = next(i for i, token in enumerate(command) if token.valor == '“')
            end_quote_index = next(i for i, token in enumerate(command) if token.valor == '”')
        except StopIteration:
            error = Error("SINTACTICO", command[-1].linea, command[-1].columna, "Falta el token '”'")
            self.Errorsin.append(error)
            print("Error de sintaxis en el comando EliminarUnico: falta el token '”'")
            return

        # Recoge todos los tokens entre '“' y '”'
        tokens_between_quotes = command[start_quote_index+1:end_quote_index]

        # Busca el token '{'
        try:
            start_brace_index = next(i for i, token in enumerate(command) if token.valor == '{')
            end_brace_index = next(i for i, token in enumerate(command) if token.valor == '}')
        except StopIteration:
            error = Error("SINTACTICO", command[-1].linea, command[-1].columna, "Falta el token '}'")
            self.Errorsin.append(error)
            print("Error de sintaxis en el comando EliminarUnico: falta el token '}'")
            return

        # Recoge todos los tokens entre '{' y '}'
        tokens_between_braces = command[start_brace_index+1:end_brace_index]
        if tokens_between_braces:
            tokens_between_braces.pop(0)  # Elimina el primer elemento

        # Comprueba los tokens después de '}'
        sec_es_after_brace = ['”', ')', ';']
        for i, (token, valor_esper) in enumerate(zip(command[end_brace_index+1:], sec_es_after_brace), start=end_brace_index+1):
            if token.valor != valor_esper:
                error = Error(token.valor, "SINTACTICO", token.linea, token.columna)
                self.Errorsin.append(error)
                print(f"Error de sintaxis en el comando EliminarUnico en la posición {i+1}")
                return

        # Si todos los tokens coinciden con la secuencia esperada, imprime el comando
        print("No hay errores de sintaxis en el comando EliminarUnico")

        # Crea un objeto con la estructura deseada y lo añade a la lista traduccion
        collection_name = ' '.join(token.valor for token in tokens_between_quotes)

        # Procesa los tokens entre las llaves
        document = ''
        remove_next_item = False
        for i, token in enumerate(tokens_between_braces):
            if remove_next_item:
                remove_next_item = False
                continue
            elif token.valor == ',':
                document += ',\n'
                remove_next_item = True
            elif token.valor == ':':
                document = document[:-1] + ':'
            else:
                document += token.valor

        traduccion_object = f"db.{collection_name}.deleteOne({{{document}}});"
        self.traduccion.append(traduccion_object)
        print("Objeto añadido a la lista traduccion: ", traduccion_object)




    def verificar_sintaxis_buscartodo(self, command):
        # Define la secuencia esperada valores de tokens
        sec_es = ['BuscarTodo', 'todo', '=', 'nueva', 'BuscarTodo', '(', '“']

        # Comprueba si los valores de los tokens en el comando coinciden con la secuencia esperada
        for i, (token, valor_esper) in enumerate(zip(command, sec_es)):
            if valor_esper is not None and token.valor != valor_esper:
                # Si el valor esperado no es None y no coincide con el valor del token, añade un error a self.Errorsin
                error = Error(token.valor, "SINTACTICO", token.linea, token.columna)
                self.Errorsin.append(error)
                print(f"Error de sintaxis en el comando BuscarTodo en la posición {i+1}")
                return

        # Busca el token '”'
        try:
            start_quote_index = next(i for i, token in enumerate(command) if token.valor == '“')
            end_quote_index = next(i for i, token in enumerate(command) if token.valor == '”')
        except StopIteration:
            error = Error("SINTACTICO", command[-1].linea, command[-1].columna, "Falta el token '”'")
            self.Errorsin.append(error)
            print("Error de sintaxis en el comando BuscarTodo: falta el token '”'")
            return

        # Recoge todos los tokens entre '“' y '”' que no sean espacios en blanco
        tokens_between_quotes = [token for token in command[start_quote_index+1:end_quote_index] if token.valor.strip()]

        # Comprueba los tokens después de '”'
        sec_es_after_quote = [')', ';']
        for i, (token, valor_esper) in enumerate(zip(command[end_quote_index+1:], sec_es_after_quote), start=end_quote_index+1):
            if token.valor != valor_esper:
                error = Error(token.valor, "SINTACTICO", token.linea, token.columna)
                self.Errorsin.append(error)
                print(f"Error de sintaxis en el comando BuscarTodo en la posición {i+1}")
                return

        # Si todos los tokens coinciden con la secuencia esperada, imprime el comando
        print("No hay errores de sintaxis en el comando BuscarTodo")

        # Crea un objeto con la estructura deseada y lo añade a la lista traduccion
        collection_name = ''.join(token.valor for token in tokens_between_quotes)
        traduccion_object = f"db.{collection_name}.find();"
        self.traduccion.append(traduccion_object)
        print("Objeto añadido a la lista traduccion: ", traduccion_object)



    def verificar_sintaxis_buscarunico(self, command):
        # Define la secuencia esperada de tokens
        sec_es = ['BuscarUnico', 'todo', '=', 'nueva', 'BuscarUnico', '(', '“']

        # Comprueba si los valores de los tokens en el comando coinciden con la secuencia esperada
        for i, (token, valor_esper) in enumerate(zip(command, sec_es)):
            if valor_esper is not None and token.valor != valor_esper:
                # Si el valor esperado no es None y no coincide con el valor del token, añade un error a self.Errorsin
                error = Error(token.valor, "SINTACTICO", token.linea, token.columna)
                self.Errorsin.append(error)
                print(f"Error de sintaxis en el comando BuscarUnico en la posición {i+1}")
                return

        # Busca el token '”'
        try:
            start_quote_index = next(i for i, token in enumerate(command) if token.valor == '“')
            end_quote_index = next(i for i, token in enumerate(command) if token.valor == '”')
        except StopIteration:
            error = Error("SINTACTICO", command[-1].linea, command[-1].columna, "Falta el token '”'")
            self.Errorsin.append(error)
            print("Error de sintaxis en el comando BuscarUnico: falta el token '”'")
            return

        # Recoge todos los tokens entre '“' y '”' que no sean espacios en blanco
        tokens_between_quotes = [token for token in command[start_quote_index+1:end_quote_index] if token.valor.strip()]

        # Comprueba los tokens después de '”'
        sec_es_after_quote = [')', ';']
        for i, (token, valor_esper) in enumerate(zip(command[end_quote_index+1:], sec_es_after_quote), start=end_quote_index+1):
            if token.valor != valor_esper:
                error = Error(token.valor, "SINTACTICO", token.linea, token.columna)
                self.Errorsin.append(error)
                print(f"Error de sintaxis en el comando BuscarUnico en la posición {i+1}")
                return

        # Si todos los tokens coinciden con la secuencia esperada, imprime el comando
        print("No hay errores de sintaxis en el comando BuscarUnico")

        # Crea un objeto con la estructura deseada y lo añade a la lista traduccion
        collection_name = ''.join(token.valor for token in tokens_between_quotes)
        traduccion_object = f"db.{collection_name}.findOne();"
        self.traduccion.append(traduccion_object)
        print("Objeto añadido a la lista traduccion: ", traduccion_object)


    def print_palabras_procesadas(self):
        if not self.palabras_procesadas:
            print("La lista palabras_procesadas está vacía.")
            return

        # Copiar todos los elementos de palabras_procesadas a por_procesar
        self.por_procesar.extend(self.palabras_procesadas)

        # Inicializar una cadena vacía para almacenar los tokens
        cadena = ""

        i = 0
        while i < len(self.por_procesar):
            # Si los próximos tres tokens son '-', reemplazarlos por '//'
            if (i < len(self.por_procesar) - 2 and 
                self.por_procesar[i].valor == '-' and 
                self.por_procesar[i+1].valor == '-' and 
                self.por_procesar[i+2].valor == '-'):
                cadena += '\n//'
                i += 3
                print("Agregado comentario de una línea a la cadena:", cadena)
            # Si los próximos dos tokens son '/*', añadir un salto de línea y luego '/*' a la cadena
            elif (i < len(self.por_procesar) - 1 and 
                self.por_procesar[i].valor == '/' and 
                self.por_procesar[i+1].valor == '*'):
                cadena += '\n/*\n'
                i += 2
                print("Agregado inicio de comentario de bloque a la cadena:", cadena)
            # Si el token actual es '*' y el próximo es '/', añadir un salto de línea, luego '*/' a la cadena y añadir otro salto de línea
            elif (i < len(self.por_procesar) - 1 and 
                self.por_procesar[i].valor == '*' and 
                self.por_procesar[i+1].valor == '/'):
                cadena = cadena.rstrip() + '\n*/\n'
                i += 2
                print("Agregado fin de comentario de bloque a la cadena:", cadena)
            else:
                # Añadir el valor del token a la cadena, seguido de un espacio si el próximo token no es '/'
                cadena += self.por_procesar[i].valor
                if i < len(self.por_procesar) - 1 and self.por_procesar[i+1].valor != '/':
                    cadena += ' '
                i += 1

        print(cadena)
        cadena_obj = Cadena(cadena)
        #Agregar la cadena a self.traduccion
        
        #self.traduccion.append(cadena_obj)  # Comentado
        print("Agregado cadena a traduccion:", self.traduccion)

        # Vaciar la lista palabras_procesadas
        self.palabras_procesadas.clear()

def generar_traduccion(traduccion, archivo_salida):
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write('')  # Escribe 'use admin' al inicio del archivo
        for elemento in traduccion:
            if isinstance(elemento, Cadena):  # Si el elemento es un objeto Cadena
                f.write(str(elemento) + ': ' + elemento.valor + '\n')  # Escribe la representación del objeto y su valor en el archivo
            else:  # Si el elemento es una cadena
                f.write(elemento + '\n')  # Escribe la cadena en el archivo
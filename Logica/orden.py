from Logica.TokenModels import MiBase, Error

def leer_archivo_bson(nombre_archivo):
    estado_db = []
    estado_colec = []
    eliminar_db = []
    eliminar_colec = []
    errorestruc = []
    indice_db = 1
    indice_coleccion = 1

    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        for i, linea in enumerate(f, start=1):
            linea = linea.strip()
            if not linea:
                continue

            if linea.startswith("use"):
                db_name = linea.split()[1]
                estado_db.append(MiBase(db_name, True, "DB", indice_db))
                indice_db += 1
            elif linea.startswith("db.createCollection"):
                nombre_coleccion = linea.split("'")[1]
                estado_colec.append(MiBase(nombre_coleccion, True, "Coleccion", indice_coleccion))
                indice_coleccion += 1
            elif linea == "db.dropDatabase();":
                eliminar_db.append(MiBase("DB", True, "DB", indice_db))
                indice_db += 1
            elif "db." in linea and ".drop();" in linea:
                nombre_coleccion = linea.split("db.")[1].split(".")[0]
                eliminar_colec.append(MiBase(nombre_coleccion, True, "Coleccion", indice_coleccion))
                indice_coleccion += 1

    print("estado_db:", [db.nombre_unico for db in estado_db])
    print("eliminar_db:", [db.nombre_unico for db in eliminar_db])
    print("estado_colec:", [colec.nombre_unico for colec in estado_colec])
    print("eliminar_colec:", [colec.nombre_unico for colec in eliminar_colec])

    diferencia_db = len(eliminar_db) - len(estado_db)
    if diferencia_db > 0:
        print("La lista eliminar_db es mayor que la lista estado_db")
        for _ in range(diferencia_db):
            errorestruc.append(Error("Estructura inexistente", "SINTACTICO", i, 0))

    diferencia_colec = len(eliminar_colec) - len(estado_colec)
    if diferencia_colec > 0:
        print("La lista eliminar_colec es mayor que la lista estado_colec")
        for _ in range(diferencia_colec):
            errorestruc.append(Error("Estructura inexistente", "SINTACTICO", i, 0))

    return estado_db, estado_colec, eliminar_db, eliminar_colec, errorestruc

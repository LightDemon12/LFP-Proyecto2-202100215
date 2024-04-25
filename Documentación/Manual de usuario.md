# Laboratorio Lenguajes Formales y de Programacón

## Traductor MongoBD

### Primer Semestre de 2024

```js
Universidad San Carlos de Guatemala
Programador: Angel Guillermo de Jesús Pérez Jiménez 
Carne: 202100215
Correo: 3870961320101@ingenieria.usac.edu.gt
```


## Descripción del Proyecto

La aplicación se enfoca en proporcionar una plataforma intuitiva y eficiente para diseñar y compilar sentencias de bases de datos no relacionales, centrándose especialmente en el ecosistema MongoDB. Con un conjunto de herramientas cuidadosamente diseñadas, los usuarios pueden crear, editar y validar sus sentencias de manera rápida y precisa. Además, la aplicación ofrece funcionalidades avanzadas para analizar léxica y sintácticamente el código, identificar y corregir errores, y transformar las sentencias diseñadas en comandos MongoDB listos para su ejecución. Este enfoque integral permite a los usuarios trabajar de manera efectiva en la creación de bases de datos no relacionales, optimizando el proceso de desarrollo y aumentando la productividad.

## Flujo del programa

* Interfaz de usuario inicial

![Interfaz inicial](https://i.ibb.co/L5Mjdms/imagen-2024-04-24-191836473.png)

* se muestra la el menu de opciones del archivo

![Interfaz Menu](https://i.ibb.co/P6XFZ2s/image.png)

* se muestra la ventana con el archivo cargado
![Archivo Cargado](https://i.ibb.co/T2YhZ89/image.png)

* se muestra la ventana de tokens mostrados en una tabla
![Selección nombre archivo](https://i.ibb.co/6YrpLLv/image.png)

* se muestra la ventana con la traduccion del archivo
![Traduccion del archivo resultante](https://i.ibb.co/kKv81Sx/image.png)

* se muestran las opciones del archivos resultante
![Archivos resultantes](https://i.ibb.co/mXy0vPG/image.png)

* se muestra  el formato de la ventana de error en caso de encontrar alguno
![Ventana error](https://i.ibb.co/6y6PCts/image.png)

* se muestra el contenido de la tabla de errores
![Tabla de errores](https://i.ibb.co/RHxCp70/image.png)

## Formato de instrucciones validas

| Tipo de Función  | Función          | MongoDB                |
|------------------|------------------|------------------------|
| CrearBD          | use              | use('nombreBaseDatos') |
| EliminarBD       | dropDataBase     | db.dropDatabase()      |
| CrearColeccion   | createCollection | db.createCollection('nombreColeccion') |
| EliminarColeccion| dropCollection   | db.nombreColeccion.drop() |
| InsertarUnico    | InsertOne        | db.nombreColeccion.insertOne(ARCHIVOJSON) |
| ActualizarUnico  | updateOne        | db.nombreColeccion.updateOne(ARCHIVOJSON) |
| EliminarUnico    | deleteOne        | db.nombreColeccion.deleteOne(ARCHIVOJSON) |
| BuscarTodo       | find             | db.nombreColeccion.find() |
| BuscarUnico      | findOne          | db.nombreColeccion.findOne() |

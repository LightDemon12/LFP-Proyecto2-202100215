# Laboratorio Lenguajes Formales y de Programacón

## Proyecto de Compilador para MongoDB

### Primer Semestre de 2024


Universidad San Carlos de Guatemala
Programador: Angel Guillermo de Jesús Pérez Jiménez 
Carne: 202100215
Correo: 3870961320101@ingenieria.usac.edu.gt


---

## Descripción del Proyecto

El proyecto tiene como objetivo principal desarrollar un compilador en Python que traduzca un lenguaje específico, diseñado para la creación de sentencias de bases de datos no relacionales, en sentencias compatibles con MongoDB. La herramienta resultante permitirá a los usuarios diseñar y generar fácilmente sentencias para operaciones de creación, modificación y consulta en bases de datos MongoDB.

La aplicación constará de dos áreas principales: un editor de código para la entrada de las sentencias en el lenguaje definido y un área de visualización donde se mostrarán las sentencias finales en sintaxis de MongoDB. La interfaz también incluirá funcionalidades como la carga y guardado de archivos, así como la detección y visualización de errores léxicos y sintácticos durante el proceso de compilación.

El proceso de compilación se basará en métodos como el árbol y el parser descendente de llamadas recursivas. Se implementará un análisis léxico y sintáctico para reconocer los elementos del lenguaje especificado y validar su estructura y coherencia. Los errores detectados durante el proceso de compilación se mostrarán de manera clara y detallada, proporcionando al usuario la información necesaria para corregirlos.

Además, se permitirá la inserción de comentarios en el código fuente, lo que facilitará la comprensión y documentación de las sentencias creadas. Estos comentarios podrán ser de una o varias líneas y seguirán un formato específico para garantizar su correcta interpretación.

El proyecto también incluirá la definición de funciones que representarán las operaciones típicas en MongoDB, como la creación y eliminación de bases de datos y colecciones, así como la inserción, actualización y eliminación de documentos. Estas funciones se utilizarán para generar las sentencias finales en sintaxis de MongoDB a partir de las sentencias diseñadas por el usuario.

## Objetivos

* **Objetivo General:**

  * Combinar los conocimientos adquiridos en el curso y en otros cursos de sistemas para crear un compilador que traduzca el lenguaje especificado y lo transforme en Sentencias de Bases de Datos No Relacionales.

* **Objetivos Específicos:**

  * Crear una herramienta que permita el diseño de sentencias de base de datos no relacionales de manera sencilla para el usuario.
  * Diseñar y construir un compilador que permita compilar archivos de entrada y visualizar el resultado en un entorno externo.
  * Proporcionar Retroalimentación de Errores: Mostrar de manera clara y detallada los errores léxicos y sintácticos detectados durante la compilación, para facilitar su corrección por parte del usuario.
  * Incorporar Funciones MongoDB Predefinidas: Definir funciones que representen las operaciones típicas en MongoDB, para simplificar la generación de las sentencias finales en sintaxis de MongoDB.

## Partes del arbol utilizado para el AFD

![Partes del arbol](https://i.ibb.co/02kQWPF/arbol.png)

## Formato del AFD

![AFD](https://i.ibb.co/jbzNpMB/AFD-PROYECTO-2-LFP.jpg)

## Partes del Proyecto

![Carpetas y archivos en codigo fuente](hhttps://i.ibb.co/5s3v0J7/Estructura.png)

## Tabla de Tokens

![Tabla de Tokens](https://i.ibb.co/PF0b3hS/imagen-2024-04-24-190534608.png)

## Gramática para Compilador de Sentencias de MongoDB

| **Terminales**        | **No Terminales**  | **Producciones**                                                                                          | **Expresiones Regulares** |
|-----------------------|--------------------|----------------------------------------------------------------------------------------------------------|-----------------------------|
| Tk_CrearBD            | Inicio             | Inicio ::= Operacion \| ε                                                                                 | CrearBD = 'CrearBD'        |
| Tk_Variable           | CrearDB            | Operacion ::= CrearBD \| EliminarBD \| CrearColeccion \| EliminarColeccion \| InsertarUnico \| ActualizarUnico \| EliminarUnico \| BuscarTodo \| BuscarUnico  | Variable = '(?:[a-zA-Z]+\.[0-9]*|[a-zA-Z]*\.[0-9]+|[a-zA-Z]+|[0-9]+)' |
| Tk_nueva              | EliminarBD         | CrearBD ::= Tk_CrearBD Tk_Variable Tk_Igual Tk_nueva Tk_CrearBD Tk_OpenParen Tk_CloseParen Tk_PuntoComa | nueva = 'nueva'            |
| Tk_OpenParen          | CrearColeccion     | EliminarBD ::= Tk_EliminarBD Tk_elimina Tk_Igual Tk_nueva Tk_EliminarBD Tk_OpenParen Tk_CloseParen Tk_PuntoComa | OpenParen = '\('            |
| Tk_CloseParen         | EliminarColeccion  | CrearColeccion ::= Tk_Crearcolec Tk_colec Tk_Igual Tk_nueva Tk_Crearcolec Tk_OpenParen Tk_Comilladoble Tk_Variable Tk_Comilladoble Tk_CloseParen Tk_PuntoComa | CloseParen = '\)'           |
| Tk_PuntoComa          | InsertarUnico      | EliminarColeccion ::= Tk_EliminarColecc Tk_eliminarcolec Tk_Igual Tk_nueva Tk_EliminarColecc Tk_OpenParen Tk_Comilladoble Tk_Variable Tk_Comilladoble Tk_CloseParen Tk_PuntoComa | PuntoComa = ';'             |
| Tk_EliminarBD         | ActualizarUnico    | InsertarUnico ::= TK_InsertarU Tk_insertar Tk_Igual Tk_nueva TK_InsertarU Tk_OpenParen Tk_Comilladoble Tk_Variable Tk_Comilladoble Tk_Comilla Tk_Comilla Tk_Comma Tk_Comilladoble Tk_Variable Tk_Comilladoble Tk_Comilla Tk_Comilla Tk_Comma Tk_Comilladoble Tk_Variable Tk_Comilladoble Tk_CloseParen Tk_PuntoComa | EliminarBD = 'EliminarBD'  |
| Tk_elimina            | EliminarUnico      | ActualizarUnico ::= Tk_Actualizar Tk_Actualizadoc Tk_Igual Tk_nueva Tk_Actualizar Tk_OpenParen Tk_Comilladoble Tk_Variable Tk_Comilladoble Tk_Comma Tk_Comilladoble Tk_Variable Tk_Comilladoble Tk_Comma Tk_Dolar Tk_Set Tk_Comilla Tk_Comilla Tk_Variable Tk_Comilladoble Tk_Comma Tk_Comilladoble Tk_Variable Tk_Comilladoble Tk_CloseParen Tk_PuntoComa | elimina = 'elimina'        |
| Tk_Igual              | BuscarTodo         | EliminarUnico ::= Tk_EliminarU Tk_Eliminardoc Tk_Igual Tk_nueva Tk_EliminarU Tk_OpenParen Tk_Comilladoble Tk_Variable Tk_Comilladoble Tk_CloseParen Tk_PuntoComa | Igual = '='                 |
| Tk_Crearcolec         | BuscarUnico        | BuscarTodo ::= Tk_BuscarT Tk_Todo Tk_Igual Tk_nueva Tk_BuscarT Tk_OpenParen Tk_Comilladoble Tk_Variable Tk_Comilladoble Tk_CloseParen Tk_PuntoComa | Crearcolec = 'CrearColeccion' |
| Tk_colec              |                   | BuscarUnico ::= Tk_BuscarU Tk_Todo Tk_Igual Tk_nueva Tk_BuscarU Tk_OpenParen Tk_Comilladoble Tk_Variable Tk_Comilladoble Tk_CloseParen Tk_PuntoComa | colec = 'colec'             |
| Tk_Comilladoble       |                   |                                                                                                          | Comilladoble = '"'          |
| Tk_OpenLLave          |                   |                                                                                                          | OpenLLave = '{'             |
| Tk_CloseLlave         |                   |                                                                                                          | CloseLlave = '}'            |
| Tk_Dospuntos          |                   |                                                                                                          | Dospuntos = ':'             |
| Tk_Coma               |                   |                                                                                                          | Coma = ','                  |
| Tk_EliminarColecc     |                   |                                                                                                          | EliminarColecc = 'EliminarColeccion' |
| Tk_eliminarcolec      |                   |                                                                                                          | eliminarcolec = 'eliminacolec' |
| TK_InsertarU          |                   |                                                                                                          | InsertarU = 'InsertarUnico' |
| Tk_insertar           |                   |                                                                                                          | insertar = 'insertadoc'    |
| Tk_Actualizar         |                   |                                                                                                          | Actualizar = 'ActualizarUnico' |
| Tk_doc                |                   |                                                                                                          | actualizardoc = 'actualizadoc' |
| Tk_Dolar              |                   |                                                                                                          | Dolar = '\$'                |
| Tk_Set                |                   |                                                                                                          | Set = 'set'                 |
| Tk_EliminarU          |                   |                                                                                                          | EliminarU = 'EliminarUnico'|
| Tk_Eliminardoc        |                   |                                                                                                          | eliminardoc = 'eliminadoc' |
| Tk_BuscarT            |                   |                                                                                                          | BuscarT = 'BuscarTodo'     |
| Tk_Todo               |                   |                                                                                                          | Todo = 'todo'               |
| Tk_BuscarU            |                   |                                                                                                          | BuscarU = 'BuscarUnico'    |

### expresion_regular 

{CrearBD} | {Variable} | {nueva} | {OpenParen} | {CloseParen} | {PuntoComa} | '
{EliminarBD} | {elimina} | {Igual} | {Crearcolec} | {colec} | {Comilladoble} | '
{OpenLLave} | {CloseLlave} | {Dospuntos} | {Coma} | {EliminarColecc} | {eliminarcolec} | '
{Actualizar} | {actualizardoc} | {Dolar} | {Set} | {EliminarU} | {eliminardoc} | '
{BuscarT} | {Todo} | {BuscarU} | {InsertarU} | {insertar}'


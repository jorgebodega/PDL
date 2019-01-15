# Proyecto de PDL

Por el momento, el analizador léxico esta funcionando, detecta todos los tipos de tokens que le he establecido.

__Requiere: PLY (En la carpeta de library), Python 3__

Modo de ejecucion (contando con que siempre nos encontramos en la ruta de la carpeta con la prueba a ejecutar):

    python<3> ../analizador.py
    
El fichero con el codigo debe llamarse __code.js__ (PENDIENTE DE CAMBIO -> Parametro)

El fichero [___lexico.py___](https://github.com/jorgebodega/PDL/blob/master/lexico.py)
 es el que contiene toda la funcionalidad de obtencion de tokens, con todas las definiciones de tokens de esta practica.

El fichero [___sintactico.py___](https://github.com/jorgebodega/PDL/blob/master/sintactico.py)
contiene los procedures de nuestro analizador. Existe un método que se encarga de lanzar peticiones al lexico cada vez
que se queda sin tokens, en vez de solicitarlos todos de golpe y ya trabajar. De igual manera, se encarga de crear e insertar
datos en las tablas de simbolos correspondientes.

El fichero [___tabla.py___](https://github.com/jorgebodega/PDL/blob/master/tabla.py)
contiene la funcionalidad de las tablas, para introducir nuevos datos y crear nuevas tablas, asi como la forma de imprimirlas.

El fichero [___gramatica_parse.txt___](https://github.com/jorgebodega/PDL/blob/master/gramatica_parse.txt)
contiene la gramática formateada para poder usarla dentro de la herramienta VAst.

El fichero [___first___](https://github.com/jorgebodega/PDL/blob/master/first)
contiene los first de todos los No Terminales.

El fichero [___follow___](https://github.com/jorgebodega/PDL/blob/master/follow)
contiene los follow de todos los No Terminales.

El fichero [___tabla.py___](https://github.com/jorgebodega/PDL/blob/master/tabla.py)
contiene la funcionalidad de las tablas, para introducir nuevos datos y crear nuevas tablas, asi como la forma de imprimirlas.

Como se puede ver en la salida, va imprimiendo (___POR DEFECTO___) las reglas segun las va usando.

Los ficheros de parse que estan en las carpetas son los que deben usarse en VAst

http://docutils.sourceforge.net/docs/user/rst/quickref.html
### TODO LIST

- __LEXICO__

- [X] Modificar libreria para cambiar el formato de retorno de los tokens.
- [X] Comprobar que todos los tokens estan correctos.
- [X] Poder trasladar la informacion de la TS fuera de [___lexico.py___](https://github.com/jorgebodega/PDL/blob/master/lexico.py).
- [X] Crear varios casos de prueba con y sin errores.
- [ ] Pasar el archivo de codigo como parametro.
- [ ] Pasar el flag para imprimir informacion como parametro.
- [ ] Pasar a limpio los first y follows
- [ ] Pasar a limpio la comprobacion de la condicion LL(1)
- [ ] Calcular el arbol para los tres casos correctos con VAst

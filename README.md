# Proyecto de PDL

__Requiere: PLY (En la carpeta de library), Python 3. Si se tiene descargado desde PIP, puede cambiarse la funcionalidad__
__para que obtenga la librería desde el entorno y no desde la carpeta.__

Modo de ejecución (contando con que siempre nos encontramos en la ruta de la carpeta con la prueba a ejecutar):

    python<3> ../analizador.py [flag_imprimir = False]
    
El fichero con el código debe llamarse __code.js__.

El fichero [___lexico.py___](https://github.com/jorgebodega/PDL/blob/master/lexico.py) es el que contiene toda la 
funcionalidad de obtención de tokens, utilizando la librería PLY que nos permite simplificar la detección de tokens
mediante el uso de expresiones regulares, siguiendo los criterios que están definidos en la memoria.

El fichero [___sintactico.py___](https://github.com/jorgebodega/PDL/blob/master/sintactico.py) contiene los Procedures 
de nuestro analizador. El propio analizador, cuando se queda sin tokens que seguir comprobando, se encarga de llamar al
léxico para analizar una nueva línea del fichero de código. Internamente a cada procedure está implementado el analizador
semántico, de forma que se hacen de forma simultánea el sintáctico y el semántico. De igual manera, tiene implementado el
sistema de tablas, de forma que llamará a la funcionalidad según se va necesitando.

El fichero [___tabla.py___](https://github.com/jorgebodega/PDL/blob/master/tabla.py) contiene la funcionalidad de las tablas,
tanto para controlar los identificadores, como para moverse entre diferentes tablas, o crearlas según se necesiten.
Esta clase ha sido creada para no complicar el funcionamiento de las tablas en el analizador semántico, de forma que el
usuario pueda abstraerse de manejar las tablas, los punteros y demás operaciones.

Podemos ver la definición de la gramática tal y como está planteada en la memoria en los siguientes archivos:

- El fichero [___gramatica_parse.txt___](https://github.com/jorgebodega/PDL/blob/master/gramatica_parse.txt)
contiene la gramática formateada para poder usarla dentro de la herramienta VAst.
- El fichero [___gramatica_simplificada___](https://github.com/jorgebodega/PDL/blob/master/gramatica_simplificada)
contiene la gramática simplificada de forma que pueden verse todas las producciones de una misma regla en una sola línea.
-  El fichero [___gramatica_desglosada___](https://github.com/jorgebodega/PDL/blob/master/gramatica_desglosada)
contiene la gramática desglosada de forma que podemos manejar en cada línea una sola producción.

Para comprobar que la gramática del analizador sintáctico es correcta, disponemos de los siguientes archivos:

- El fichero [___first___](https://github.com/jorgebodega/PDL/blob/master/first)
contiene los First de todos los No Terminales.
- El fichero [___follow___](https://github.com/jorgebodega/PDL/blob/master/follow)
contiene los Follow de todos los No Terminales.
- El fichero [___ll1___](https://github.com/jorgebodega/PDL/blob/master/ll1)
contiene la comprobación de la condición LL(1) para todas las reglas con más de una producción.

El fichero [___tabla.py___](https://github.com/jorgebodega/PDL/blob/master/tabla.py)
contiene la funcionalidad de las tablas, para introducir nuevos datos y crear nuevas tablas, así como la forma de imprimirlas.

Como se puede ver en la salida si el flag está activo, va imprimiendo las reglas y los tokens según se van usando.

Los ficheros de parse que están en las carpetas son los que deben usarse en la herramienta VAst

#### TODO LIST
- [ ] Pasar el archivo de código como parámetro.
- [X] Pasar el flag para imprimir información como parámetro.

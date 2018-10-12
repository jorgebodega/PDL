# Proyecto de PDL

Por el momento, el analizador léxico esta funcionando, detecta todos los tipos de tokens que le he establecido.

__Requiere: PLY (En la carpeta de library), Python 3__

Modo de ejecucion:

    python<3> analizador.py

Existe un fichero de entrada, llamado [___prueba.js___](https://github.com/jorgebodega/PDL/blob/master/prueba.js)
con algunos ejemplos.

El fichero [___analizador.py___](https://github.com/jorgebodega/PDL/blob/master/prueba.js)
se encargará de recorrer este fichero de entrada linea por linea y hacer la peticion al
analizador para que genere los tokens correspodientes, y en el futuro, de manejar esos tokens que recibimos con las fases mas avanzadas
del analizar sintático.

Como se puede ver en la salida, detecta los tokens y los guarda en una array por linea.

El fichero [___lexico.py___](https://github.com/jorgebodega/PDL/blob/master/prueba.js)
 es el que contiene toda la logica, con todas las definiciones de tokens de esta practica.

### TODO LIST

- [ ] Modificar libreria para cambiar el formato de retorno de los tokens.
- [ ] Comprobar que todos los tokens estan correctos.
- [ ] Poder trasladar la informacion de la TS fuera de [___lexico.py___](https://github.com/jorgebodega/PDL/blob/master/prueba.js).
- [ ] Crear varios casos de prueba con y sin errores.
- [ ] Separar casos de prueba en carpetas y cambiar el modo de ejecucion para adaptarse.
- [ ] Definir el formato de la tabla de simbolos.

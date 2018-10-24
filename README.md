# Proyecto de PDL

Por el momento, el analizador léxico esta funcionando, detecta todos los tipos de tokens que le he establecido.

__Requiere: PLY (En la carpeta de library), Python 3__

Modo de ejecucion (contando con que siempre nos encontramos en la ruta de la carpeta con la prueba a ejecutar):

    python<3> ../analizador.py
    
El fichero con el codigo debe llamarse __code.js__ (PENDIENTE DE CAMBIO -> Parametro)

Existe un fichero de entrada, llamado [___prueba.js___](https://github.com/jorgebodega/PDL/blob/master/prueba.js)
con algunos ejemplos.

El fichero [___analizador.py___](https://github.com/jorgebodega/PDL/blob/master/analizador.py)
se encargará de recorrer este fichero de entrada linea por linea y hacer la peticion al
analizador para que genere los tokens correspodientes, y en el futuro, de manejar esos tokens que recibimos con las fases mas avanzadas
del analizar sintático.

Como se puede ver en la salida, detecta los tokens y los guarda en una array por linea.

El fichero [___lexico.py___](https://github.com/jorgebodega/PDL/blob/master/lexico.py)
 es el que contiene toda la logica, con todas las definiciones de tokens de esta practica.

### TODO LIST

- __LEXICO__

- [X] Modificar libreria para cambiar el formato de retorno de los tokens.
- [ ] Comprobar que todos los tokens estan correctos.
- [X] Poder trasladar la informacion de la TS fuera de [___lexico.py___](https://github.com/jorgebodega/PDL/blob/master/lexico.py).
- [X] Crear varios casos de prueba con y sin errores.
- [X] Separar casos de prueba en carpetas y 
- [ ] Cambiar el modo de ejecucion y pasar el archivo de codigo como parametro.
- [ ] Borrar Token de __'- (MENOS)'__ y pasar el valor del entero directamente con signo

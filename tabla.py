"""
Archivo que manejara la funcionalidad de la tabla de simbolos.

TODO: Hay que añadir funcionalidad posteriormente, con el sintáctico y el semántico.
"""

class TablaSimbolos:

    def __init__(self):
        self.__dictInterno = [] # Tecnicamente es una lista, pero no le cambie el nombre de la variable
        self.ptrTabla = None

    def __str__(self):
        contenido = ''
        for tabla in self.__dictInterno:
            contenido += str(tabla)
            contenido += 30 * '=' + '\n\n'
        return contenido

    def init_ts(self):
        """Inicializamos las tablas de simbolos con la tabla general."""
        self.__dictInterno.append(Tabla('TSGeneral'))
        self.ptrTabla = self.__dictInterno[0]

    def removeTabla(self):
        """Movemos el puntero de la tabla actual a la tabla general."""
        if self.ptrTabla != self.__dictInterno[0]:
            self.ptrTabla = self.__dictInterno[0]

    def comprobar_lexema(self, lexema):
        return self.ptrTabla.comprobar_lexema(lexema)

    def is_tablageneral(self):
        return self.ptrTabla == self.__dictInterno[0]

    def insertarFuncion(self, lexema):
        self.ptrTabla.insertarFuncion(lexema)  # Insertamos la funcion en la tabla de simbolos apuntada.
        self.__dictInterno.append(Tabla('TS_' + lexema))  # Insertamos una nueva tabla.
        self.ptrTabla = self.__dictInterno[-1]  # Cambiamos el puntero a la nueva tabla.

    def insertarLexema(self, lexema, size):
        self.ptrTabla.insertarLexema(lexema, size)  # Insertamos el nuevo lexemana en la tabla de simbolos apuntada.


class Tabla:

    def __init__(self, nombre_tabla):
        self.nombre = nombre_tabla
        self.lexemas = []
        self.contenido = []
        self.desplazamiento = 0

    def __str__(self):
        texto = 'CONTENIDO DE LA TABLA # %s\n\n' % self.nombre
        tabla = self.contenido
        for item in tabla:
            texto += '*\tLEXEMA: \'%s\'\n' % str(item['lexema'])
            texto += ' \tATRIBUTOS:\n'
            for key in item['atributos'].keys():
                texto += '\t\t%s : %s\n' % (str(key), str(item['atributos'][key]))
            texto += 20 * '-' + '\n'
        return texto

    def comprobar_lexema(self, lexema):
        return lexema in self.lexemas

    def insertarLexema(self, lexema, size):
        if lexema not in self.lexemas:
            self.lexemas.append(lexema)
            self.contenido.append({
                'lexema': lexema,
                'atributos': {
                    'Prueba': 'Prueba',
                    'Desplazamiento': self.desplazamiento
                }
            })
            self.desplazamiento += size

    def insertarFuncion(self, lexema):
        if lexema not in self.lexemas:
            self.lexemas.append(lexema)
            self.contenido.append({
                'lexema': lexema,
                'atributos': {
                    'Prueba': 'Prueba',
                    'Desplazamiento': self.desplazamiento
                }
            })
            self.desplazamiento += 4 # Vamos a dar por hecho que los punteros son de 4 bytes

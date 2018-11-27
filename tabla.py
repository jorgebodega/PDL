"""
Archivo que manejara la funcionalidad de la tabla de simbolos.

TODO: Hay que añadir funcionalidad posteriormente, con el sintáctico y el semántico.
"""

class TablaSimbolos:

    def __init__(self):
        self.__dictInterno = [Tabla('TSGeneral')]
        self.ptrTabla = self.__dictInterno[0]

    def __str__(self):
        contenido = ''
        for tabla in self.__dictInterno:
            contenido += str(tabla)
            contenido += '\n' + 30 * '=' + '\n'
        return contenido

    def removeTabla(self):
        if self.ptrTabla != self.__dictInterno[0]:
            self.__dictInterno.remove(self.ptrTabla)
            self.ptrTabla = self.__dictInterno[0]

    def insertarFuncion(self, lexema):
        self.ptrTabla.insertarFuncion(lexema)
        self.__dictInterno.append(Tabla(lexema))
        self.ptrTabla = self.__dictInterno[-1]
        self.ptrTabla.insertarLexema(lexema)

    def insertarLexema(self, lexema):
        self.ptrTabla.insertarLexema(lexema)

class Tabla:

    def __init__(self, nombreTabla):
        self.nombre = nombreTabla
        self.lexemas = []
        self.contenido = []

    def __str__(self):
        texto = 'CONTENIDO DE LA TABLA # %s\n\n' % self.nombre
        tabla = self.contenido
        for item in tabla:
            texto += '*\tLEXEMA: \'%s\'\n' % str(item['lexema'])
            texto += ' \tATRIBUTOS:'
            for key in item['atributos'].keys():
                texto += '\t\t%s : %s' % (str(key), str(item['atributos'][key]))
            texto += 20 * '-' + '\n'
        texto += 30 * '=' + '\n'
        return texto

    def insertarLexema(self, lexema):
        self.lexemas.append(lexema)
        self.contenido.append({
            'lexema': lexema,
            'atributos': [{
                'Prueba': 'Prueba'
            }]
        })

    def insertarFuncion(self, lexema):
        self.lexemas.append(lexema)
        self.contenido.append({
            'lexema': lexema,
            'atributos': [{
                'Prueba': 'Prueba'
            }]
        })

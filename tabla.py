"""
Archivo que manejara la funcionalidad de la tabla de simbolos.

TODO: Hay que añadir funcionalidad posteriormente, con el sintáctico y el semántico.
"""


class TablaSimbolos:

    def __init__(self):
        self.__dictInterno = {
            'TSGeneral': []
        }

    def __str__(self):
        contenido = ''
        for key in self.__dictInterno:
            contenido += 'CONTENIDO DE LA TABLA # %s\n\n' % key
            tabla = self.__dictInterno[key]
            for item in tabla:
                contenido += '* LEXEMA: \'%s\'\n' % item['LEXEMA']
                contenido += 20*'-' + '\n'
            contenido += 30*'=' + '\n'
        return contenido

    def insertarFuncion(self, lexema):
        nombreTabla = 'TS_' + lexema
        self.__dictInterno[nombreTabla] = []

    def insertarLexema(self, lexema, tabla='TSGeneral'):
        self.__dictInterno[tabla].append({
            'LEXEMA': lexema
        })

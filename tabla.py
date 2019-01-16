class TablaSimbolos:
    """
    Clase que sirve para abstraer al usuario del funcionamiento de las tablas, permitiendole hacer uso de estas
    sin preocuparse de mantener el puntero ni el array interno.
    Solo se encarga de redirigir las funciones en caso necesario o de manejar su propio array interno con el puntero.
    """

    def __init__(self):
        self.__tablas = {}
        self.__puntero_tabla = None

    def __str__(self):
        contenido = ''
        for nombre, tabla in self.__tablas:
            contenido += 'CONTENIDO DE LA TABLA # %s\n\n' % nombre
            contenido += str(tabla)
            contenido += 30 * '=' + '\n\n'
        return contenido

    def iniciar_tabla_simbolos(self):
        """
        Inicializamos las tablas de simbolos con la tabla general.
        Solo puede llamarse una vez, al inicio del problema.
        """
        if len(self.__tablas) == 0:
            self.__tablas['TSGeneral'] = Tabla()
            self.__puntero_tabla = self.__tablas[0]

    def remove_tabla(self):
        """
        Si el puntero no esta apuntando a la Tabla General, lo apunta.
        Solo se permite este comportamiento porque el lenguaje no permite anidar funciones,
        con lo que no se crean subtablas de subtablas, nivel máximo de profundidad 1.
        """
        if self.__puntero_tabla != self.__tablas['TSGeneral']:
            self.__puntero_tabla = self.__tablas['TSGeneral']

    def comprobar_lexema(self, lexema):
        """
        Invoca al metodo comprobar_lexema de la tabla correspondiente.
        :param lexema: Lexema que el usuario quiere comprobar.
        :return: True | False
        """
        return self.__puntero_tabla.comprobar_lexema(lexema)

    def tipo_lexema(self, lexema):
        """
        Invoca al metodo tipo_lexema de la tabla correspondiente.
        :param lexema: Lexema que el usuario quiere comprobar.
        :return: Tipo lexema | None
        """
        return self.__puntero_tabla.tipo_lexema(lexema)

    def insertar_funcion(self, lexema):
        """
        Inserta el lexema nuevo en la tabla actualmente apuntada, marcando que es una funcion.
        :param lexema: Lexema a ser añadido.
        """
        self.__puntero_tabla.insertar_funcion(lexema)
        self.__tablas[lexema] = Tabla()  # Creamos la nueva Tabla.
        self.__puntero_tabla = self.__tablas[lexema]  # Cambiamos el puntero a la nueva tabla.

    def insertar_lexema(self, lexema, tipo_dato, size):
        """
        Inserta el lexema nuevo en la tabla actualmente apuntada.
        :param lexema: Lexema a ser añadido.
        :param size: Tamaño del lexema.
        """
        self.__puntero_tabla.insertar_lexema(lexema, tipo_dato, size)


class Tabla:
    """
    Clase que contiene la funcionalidad de la tabla, como insertar nuevos elementos,
    buscar elementos, comprobar el tipo de estos o imprimir la informacion de la tabla.
    """

    def __init__(self):
        self.tabla = {}
        self.desplazamiento = 0

    def __str__(self):
        texto = ''
        for lexema, entrada in self.tabla:
            texto += '*\tLEXEMA: \'%s\'\n' % str(lexema)
            texto += ' \tATRIBUTOS:\n'
            for atributo in entrada.keys():
                texto += '\t\t%s : %s\n' % (str(atributo), str(entrada[atributo]))
            texto += 20 * '-' + '\n'
        return texto

    def comprobar_lexema(self, lexema):
        """
        Comprueba que existe el lexema en la tabla.
        :param lexema: Lexema que el usuario quiere comprobar.
        :return: True | False
        """
        return lexema in self.tabla

    def tipo_lexema(self, lexema):
        """
        Devuelve el tipo del lexema parametro.
        :param lexema: Lexema que el usuario quiere comprobar.
        :return: Tipo lexema | None
        """
        return self.tabla[lexema]['Tipo']

    def insertar_lexema(self, lexema, tipo_dato, size):
        """
        Inserta un nuevo lexema en la tabla de contenido.
        PRE: El lexema no existe en la tabla previamente. Usar el metodo comprobar_lexema

        :param lexema: Nuevo lexema que incluir en la tabla.
        :param tipo_dato: Tipo del lexema que queremos introducir. Cualquiera menos funciones.
        :param size: Tamaño del lexema. Viene determinado previamente por el tipo de dato.
        :return:
        """
        self.tabla[lexema] = {
            'Tipo': tipo_dato,
            'Desplazamiento': self.desplazamiento
        }
        self.desplazamiento += size

    def insertar_funcion(self, lexema):
        """
        Inserta un nuevo lexema en la tabla de contenido.
        PRE: El lexema no existe en la tabla previamente. Usar el metodo comprobar_lexema

        :param lexema: Nuevo lexema que incluir en la tabla.
        :return:
        """
        self.tabla[lexema] = {
            'Tipo': 'funcion',
            'Desplazamiento': self.desplazamiento
        }
        # Vamos a dar por hecho que los punteros son de 4 bytes
        self.desplazamiento += 4

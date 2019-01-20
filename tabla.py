class TablaSimbolos:
    """
    Clase que abstrae al usuario del funcionamiento de las tablas, permitiendole hacer uso de estas
    sin preocuparse de mantener el puntero ni el array interno.
    Solo se encarga de redirigir las funciones en caso necesario o de manejar su propio array interno con el puntero.
    """

    def __init__(self):
        self.__tablas = {}
        self.__puntero_tabla = None

    def __str__(self):
        contenido = ''
        for nombre, tabla in self.__tablas.items():
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
            self.__puntero_tabla = self.__tablas['TSGeneral']

    def remove_tabla(self):
        """
        Si el puntero no esta apuntando a la Tabla General, lo apunta.
        Solo se permite este comportamiento porque el lenguaje no permite anidar funciones,
        con lo que no se crean subtablas de subtablas, nivel máximo de profundidad 1.
        """
        if self.__puntero_tabla != self.__tablas['TSGeneral']:
            self.__puntero_tabla = self.__tablas['TSGeneral']

    def is_defined(self, lexema):
        """
        Comprueba si el id esta definido en la tabla apuntada o en la general
        :param lexema: Id que el usuario quiere comprobar.
        :return: True | False
        """
        definido = self.__puntero_tabla.is_defined(lexema)
        if not definido and self.__puntero_tabla != self.__tablas['TSGeneral']:
            definido = self.__tablas['TSGeneral'].is_defined(lexema)
        return definido

    def is_defined_only_in_pointer(self, lexema):
        """
        Comprueba si el id esta definido en la tabla apuntada o en la general
        :param lexema: Id que el usuario quiere comprobar.
        :return: True | False
        """
        definido = self.__puntero_tabla.is_defined(lexema)
        return definido

    def tipo_lexema(self, lexema):
        """
        Devuelve el tipo del id si esta esta definido.
        :param lexema: Id que se quiere comprobar.
        :return: Tipo lexema | None
        """
        valor = self.__puntero_tabla.tipo_lexema(lexema)
        if valor is None and self.__puntero_tabla != self.__tablas['TSGeneral']:
            valor = self.__tablas['TSGeneral'].tipo_lexema(lexema)
        return valor

    def tipo_retorno(self, lexema):
        """
        Devuelve el tipo del id si esta esta definido.
        :param lexema: Id que se quiere comprobar.
        :return: Tipo lexema | None
        """
        valor = self.__tablas['TSGeneral'].tipo_retorno(lexema)
        return valor

    def insertar_funcion(self, lexema, size, parametros, tipo_retorno):
        """
        Inserta el lexema nuevo en la tabla actualmente apuntada, marcando que es una funcion.
        Borra los parametros de la tabla global
        :param lexema: Lexema a ser añadido.
        """
        self.__puntero_tabla.insertar_funcion(lexema, size, parametros, tipo_retorno)
        self.__tablas['TS_' + lexema] = Tabla()  # Creamos la nueva Tabla.
        self.__puntero_tabla = self.__tablas['TS_' + lexema]  # Cambiamos el puntero a la nueva tabla.
        for param in parametros:
            tipo, size_lexema, param_lexema = param
            if not self.__tablas['TSGeneral'].is_defined(param_lexema):
                self.__tablas['TSGeneral'].remove_attr(param_lexema)
            self.__puntero_tabla.insertar_lexema(param_lexema, tipo, size_lexema)

    def insertar_id_base(self, lexema):
        """
        Inserta el id nuevo en la tabla actualmente apuntada desde el lexico.
        :param lexema: id a ser añadido.
        """
        self.__puntero_tabla.insertar_id_base(lexema)

    def insertar_lexema(self, lexema, tipo_dato, size):
        """
        Inserta el lexema nuevo en la tabla actualmente apuntada.
        :param lexema: Lexema a ser añadido.
        :param tipo_dato: Tipo del dato que vamos a añadir.
        :param size: Tamaño del lexema.
        """
        self.__puntero_tabla.insertar_lexema(lexema, tipo_dato, size)

    def insertar_lexema_global(self, lexema, tipo_dato, size):
        """
        Inserta el lexema nuevo en la tabla general.
        :param lexema: Lexema a ser añadido.
        :param tipo_dato: Tipo del dato que vamos a añadir.
        :param size: Tamaño del lexema.
        """
        if self.__puntero_tabla != self.__tablas['TSGeneral']:
            self.__puntero_tabla.remove_attr(lexema)
        self.__tablas['TSGeneral'].insertar_lexema(lexema, tipo_dato, size)


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
        for lexema, entrada in self.tabla.items():
            texto += '*\tLEXEMA: \'%s\'\n' % str(lexema)
            texto += ' \tATRIBUTOS:\n'
            for atributo in entrada.keys():
                texto += '\t+\t%s : %s\n' % (str(atributo), str(entrada[atributo]))
            texto += 20 * '-' + '\n'
        return texto

    def tipo_lexema(self, lexema):
        """
        Devuelve el tipo del id parametro.
        :param lexema: Id que el usuario quiere comprobar.
        :return: Tipo lexema | None
        """
        valor = None
        if lexema in self.tabla and 'Tipo' in self.tabla[lexema].keys():
            valor = self.tabla[lexema]['Tipo']
        return valor

    def tipo_retorno(self, lexema):
        """
        Devuelve el tipo del id parametro.
        :param lexema: Id que el usuario quiere comprobar.
        :return: Tipo lexema | None
        """
        valor = self.tabla[lexema]['TipoRetorno']
        return valor

    def is_defined(self, lexema):
        """
        Devuelve si el lexema ha sido inicializado en la tabla.
        Si solo ha sido insertado por el lexico, se considera que no ha sido inicializado.
        :param lexema: Id a comprobar.
        :return: True | False
        """
        return lexema in self.tabla and len(self.tabla[lexema].keys()) != 0

    def insertar_id_base(self, lexema):
        """
        Inserta un nuevo lexema en la tabla de contenido, desde el lexico.
        PRE: El lexema no existe en la tabla previamente. Usar el metodo comprobar_lexema

        :param lexema: Nuevo lexema que incluir en la tabla.
        :return:
        """
        if lexema not in self.tabla:
            self.tabla[lexema] = {}

    def insertar_lexema(self, lexema, tipo_dato, size):
        """
        Cambia el id por un lexema en la tabla de contenido.

        :param lexema: id que modificar en la tabla.
        :param tipo_dato: Tipo del lexema que queremos introducir. Cualquiera menos funciones.
        :param size: Tamaño del lexema. Viene determinado previamente por el tipo de dato.
        :return:
        """
        self.tabla[lexema] = {
            'Tipo': tipo_dato,
            'Despl': self.desplazamiento
        }
        self.desplazamiento += size

    def insertar_funcion(self, lexema, size, parametros, tipo_retorno):
        """
        Cambia el id por una funcion en la tabla de contenido.

        :param lexema: id que modificar en la tabla.
        :return:
        """
        self.tabla[lexema] = {
            'Tipo': 'funcion',
            'Despl': self.desplazamiento,
            'numParam': len(parametros),
            'TipoRetorno': tipo_retorno
        }
        for index, param in enumerate(parametros, start=1):
            self.tabla[lexema]['TipoParam%d' % index] = param[0]
        # Vamos a dar por hecho que los punteros son de 4 bytes
        self.desplazamiento += size

    def remove_attr(self, lexema):
        del self.tabla[lexema]

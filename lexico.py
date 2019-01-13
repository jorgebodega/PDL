"""
Archivo que manejara la funcionalidad del analizador lexico.

Recibe una linea de codigo, genera los tokens correspondientes,
los devuelve en un array y escribe en un archivo.
"""

import library.lex as lex


class Token(object):
    """
    Esta clase es una clase auxiliar para manejar los tokens.
    Hace lo mismo que la de la libreria, pero esta nos permite no estar
    entrando a modificar la libreria.
    """

    def __init__(self, tipo, valor, linea, columna):
        self.tipo = str(tipo)
        self.valor = valor
        self.linea = linea
        self.columna = columna

    def __str__(self):
        return '<%s, %s>' % (str(self.tipo), str(self.valor))

    def __repr__(self):
        return str(self)


class AnLex(object):
    """
    Clase que contiene la libreria y hace uso de ella para crear y transmitir los tokens.
    """

    # Lista con los tipos de tokens de nuestro analizador
    tokens = (
        # Operadores (+, ++, -, ==, !=, &&, ,, =, ;, {, }, (, ))
        'op_suma', 'op_posinc', 'op_resta', 'op_igual', 'op_noigual',
        'op_and', 'op_coma', 'op_asignacion', 'op_ptocoma', 'op_llaveab',
        'op_llavecer', 'op_parenab', 'op_parencer',

        # Otros (identificador, palabra reservada, cadena de texto, entero)
        'ID', 'PR', 'cadena', 'entero'
    )

    palabras_reservadas = (
        # Palabras reservadas de nuestro lenguaje
        'True', 'False', 'var', 'function', 'int', 'bool', 'String',
        'print', 'prompt', 'return', 'for', 'if'
    )

    id = []

    # Expresiones regulares para los operadores
    def t_op_suma(self, t):
        r'\+{1}'
        t.value = '-'
        return t
    def t_op_posinc(self, t):
        r'\+{2}'
        t.value = '-'
        return t
    def t_op_resta(self, t):
        r'-'
        t.value = '-'
        return t
    def t_op_igual(self, t):
        r'=='
        t.value = '-'
        return t
    def t_op_noigual(self, t):
        r'!='
        t.value = '-'
        return t
    def t_op_and(self, t):
        r'&&'
        t.value = '-'
        return t
    def t_op_coma(self, t):
        r','
        t.value = '-'
        return t
    def t_op_asignacion(self, t):
        r'='
        t.value = '-'
        return t
    def t_op_ptocoma(self, t):
        r';'
        t.value = '-'
        return t
    def t_op_llaveab(self, t):
        r'{'
        t.value = '-'
        return t
    def t_op_llavecer(self, t):
        r'}'
        t.value = '-'
        return t
    def t_op_parenab(self, t):
        r'\('
        t.value = '-'
        return t
    def t_op_parencer(self, t):
        r'\)'
        t.value = '-'
        return t

    # Reglas que ignoran espacios, tabulados y comentarios del tipo //
    t_ignore = ' \t\n'
    t_ignore_COMMENT = r'/{2}[ |\w|\W]+'

    def __init__(self, fs, fe):
        self.fichero_salida = fs
        self.fichero_error = fe
        self.__errorCheck = False
        self.lexer = None

    def getPalRes(self):
        return self.palabras_reservadas

    def getErrorCheck(self):
        return self.__errorCheck

    def t_entero(self, t):
        r'\d+'
        valor_entero = int(t.value)
        if valor_entero <= 32767:
            t.value = int(t.value)
            return t
        # Si el numero no se encuentra en el rango permitido, marcamos el error
        # t.lexer.skip(1)
        mensaje_error = "Error Lexico (Linea %d): Numero no permitido '%i': Fuera de los limites\n" % (t.lineno, valor_entero)
        self.fichero_error.write(mensaje_error)
        self.__errorCheck = True
        exit()

    def t_PR(self, t):
        r'([a-z]|[A-Z])(\w|\_)*'
        try:
            t.value = self.palabras_reservadas.index(t.value) + 1
            return t
        except ValueError:
            # No problem, si salta la excepcion es que no lo ha encontrado en las palabras reservadas.
            # Python es asi, en vez de notificar que no lo encuentra, pues te salta una excepcion en la cara.
            return self.t_ID(t)

    def t_ID(self, t):
        r'([a-z]|[A-Z])(\w|\_)*'
        try:
            id_position = self.id.index(t.value)
            t.value = id_position + 1
            t.type = 'ID'
            return t
        except ValueError:
            self.id.append(t.value)
            t.value = len(self.id)
            t.type = 'ID'
            return t

    def t_cadena(self, t):
        r'"[\w|\W]*"'
        t.value = str(t.value).replace('"', '')
        return t

    # Manejo de errores (No debería aparecer ninguno)
    def t_error(self, t):
        mensaje_error = 'Error Lexico (Linea %d): Caracter no permitido "%s"' % ( t.lineno, t.value[0])
        self.fichero_error.write(mensaje_error)
        self.__errorCheck = True
        exit()

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        self.lexer.lineno = 1

    # Test it output
    def tokenizeLine(self, data):
        self.lexer.input(data)
        tokens = []
        while not self.__errorCheck:
            try:
                tok = self.lexer.token()
            except lex.LexError:
                break
            if not tok:
                break
            tokenFormatted = Token(tok.type, tok.value, tok.lineno, tok.lexpos)
            # Lineas que muestran la informacion en el formato de la libreria
            # self.fichero_salida.write(str(tok) + '\n')
            # tokens.append(tok)
            self.fichero_salida.write(str(tokenFormatted) + '\n')
            tokens.append(tokenFormatted)
        self.lexer.lineno += 1
        return tokens

    def lineaActual(self):
        return self.lexer.lineno

    def getLexema(self, index):
        return self.id[index]

"""
Archivo que manejara la funcionalidad del analizador lexico.

Recibe una linea de codigo, genera los tokens correspondientes,
los devuelve en un array y escribe en un archivo.
"""

import library.lex as lex

class AnLex(object):

    # Lista con los tipos de tokens de nuestro analizador
    tokens = (
        # Operadores (+, ++, -, ==, !=, &&, ,, =, ;, {, }, (, ))
        'op_suma', 'op_posinc', 'op_resta', 'op_igual', 'op_noigual',
        'op_and', 'op_coma', 'op_asignacion', 'op_ptocoma', 'op_corchab',
        'op_corchcer', 'op_parenab', 'op_parencer',

        # Otros (identificador, palabra reservada, cadena de texto, entero)
        'ID', 'PR', 'cadena', 'entero'
    )

    palabras_reservadas = (
        # Palabras reservadas de nuesto lenguaje
        'true', 'false', 'var', 'function', 'int', 'bool', 'chars',
        'print', 'prompt', 'return', 'for', 'break', 'if'
    )

    id = []

    # Expresiones regulares para los operadores
    t_op_suma       = r'\+{1}'
    t_op_posinc     = r'\+{2}'
    t_op_resta      = r'-'
    t_op_igual      = r'=='
    t_op_noigual    = r'!='
    t_op_and        = r'&&'
    t_op_coma       = r','
    t_op_asignacion = r'='
    t_op_ptocoma    = r';'
    t_op_corchab    = r'{'
    t_op_corchcer   = r'}'
    t_op_parenab    = r'\('
    t_op_parencer   = r'\)'

    # Reglas que ignoran espacios, tabulados y comentarios del tipo //
    t_ignore = ' \t\n'
    t_ignore_COMMENT = r'/{2}[ |\w|\W]+'

    def __init__(self, fd):
        self.fichero_salida = fd
        self.lexer = None

    def t_entero(self, t):
        r'\d+|\-{1}\d+'
        valor_entero = int(t.value)
        if -32767 <= valor_entero <= 32767:
            t.value = int(t.value)
            return t
        # Si el numero no se encuentra en el rango permitido, marcamos el error
        # t.lexer.skip(1)
        self.fichero_salida.write("Illegal number '%i': Out of Bounds\n" % valor_entero)

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
        print('Illegal character "%s"' % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test it output
    def test(self, data):
        self.lexer.input(data)
        tokens = []
        while True:
             tok = self.lexer.token()
             if not tok:
                 break
             self.fichero_salida.write(str(tok) + '\n')
             tokens.append(tok)
        return tokens

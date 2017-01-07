import library.ply.lex as lex
import library.ply.yacc as yacc

# Listas
reserved = ('true','false','var','function','int','bool','chars','write','prompt','return','switch','case','break','if')
operators = ('*','>','!','=','++','(',')','{','}',':','-',',',';')
tokens = ('NUM','CAD','OP','ID','PalRes','EOF')

# Lista con los identificadores que iremos añadiendo
ids = []

# Lista de tokens que va sacando el analizador
toks = []

##########################################################################
######################### Analizador Léxico ##############################
##########################################################################

# Expresión regular que nos permite identificar cadenas de números, empiecen o no por un -
def t_NUM(t):
    r'\d+|\-{1}\d+'
    if (int(t.value) <= 32767):
        t.value = int(t.value)
        return t
    else:   archivo.write("Illegal number '%i': Out of Bounds\n" % int(t.value))

# Expresión regular que nos permite identificar operadores. Cambiamos el valor a devolver para ordenar la lista
# desde 1 en vez de 0
def t_OP(t):
    r'\*|\>|\!|\=|\+{2}|\(|\)|\{|\}|\:|\-|\,|\;'
    t.value = int(operators.index(t.value)) + 1
    return t

# Expresión regular que nos permite identificar cadenas de caracteres incluidas entre ' y '
def t_CAD(t):
    r'\'{1}\w+\'{1}'
    t.value = str(t.value)
    return t

# Expresión regular que nos permite identificar palabras reservadas del lenguaje.
# En caso de no ser una palabra reservada, comprobamos t_ID(t)
def t_PalRes(t):
    r'([a-z]|[A-Z]){1}(\w|\_)+'
    try:
        t.value = int(reserved.index(t.value)) + 1
        return t
    except Exception as e:
        return t_ID(t)
        pass

# Expresión regular que nos permite encontrar identificadores del lenguaje.
# Si la expresión que encontramos no esta incluida como identificador, la añadimos
def t_ID(t):
    r'([a-z]|[A-Z]){1}(\w|\_)+'
    try:
        t.value = int(ids.index(t.value)) + 1
        t.type = tokens[3]
        return t
    except Exception as e:
        ids.append(t.value)
        t.value = int(ids.index(t.value)) + 1
        t.type = tokens[3]
        return t
        pass

# Reglas que ignoran espacios, tabulados y comentarios del tipo //
t_ignore  = ' \t'
t_ignore_COMMENT = r'\/{2}.+|\W{1}'

# Manejo de errores (No debería aparecer ninguno)
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Calcula la linea en la que estamos
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Construye el analizador
lexer = lex.lex()

# Abre el archivo que contiene nuestro programa y el archivo de destino
texto = open("programa.js","r")
archivo = open("tokens.txt", "w")

# Nos recorremos el archivo linea a linea
for text in texto:
    lex.input(text) #Añadimos la linea al analizador
    for tok in lexer: #Va recorriendo los caracteres para ir haciendo los tokens
        toks.append(tok) # Añadimos el token al final de la lista
        token = "<" + str(tok.type) + ", " + str(tok.value) + ">"
        archivo.write(token + "\n") # Sacamos el token al archivo para su lectura

# Manejo del token EOF, que añadiremos al final del archivo
tokenEOF = lex.LexToken() # Creamos el token
tokenEOF.type = tokens[5] # Asignamos el valor EOF
tokenEOF.value = "" # Le asignamos un valor vacío
toks.append(tokenEOF) # Lo añadimos al final de la lista

#Imprimimos tambien el token EOF
token = "<" + str(tokenEOF.type) + ", " + str(tokenEOF.value) + ">"
archivo.write(token) # Sacamos el token al archivo para su lectura

##########################################################################
####################### Analizador Sintáctico ############################
##########################################################################

parser = yacc.yacc()
start = 'p'

def p_P(p):
    '''P: BZP | FZP | ZP | EOF'''

def p_B(p):
    '''B: EOF | empty'''

def p_T(p):
    '''T: EOF | empty'''

def p_S(p):
    '''S: EOF | empty'''

def p_X(p):
    '''X: EOF | empty'''

def p_L(p):
    '''L: EOF | empty'''

def p_Q(p):
    '''Q: EOF | empty'''

def p_E(p):
    '''E: EOF | empty'''

def p_R(p):
    '''R: EOF | empty'''

def p_U(p):
    '''U: EOF | empty'''

def p_V(p):
    '''V: EOF | empty'''

def p_F(p):
    '''F: EOF | empty'''

def p_H(p):
    '''H: EOF | empty'''

def p_A(p):
    '''A: EOF | empty'''

def p_K(p):
    '''K: EOF | empty'''

def p_Z(p):
    '''Z: EOF | empty'''

def p_C(p):
    '''C: EOF | empty'''

def p_W(p):
    '''W: EOF | empty'''

def p_Y(p):
    '''Y: EOF | empty'''

def p_M(p):
    '''M: EOF | empty'''

def p_N(p):
    '''N: EOF | empty'''

def p_EOF(p):
    '''EOF: '''
    pass

def p_empty(p):
    'empty :'
    pass

while True:
   try:
       for text in texto:
           s = raw_input(text)
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)

#Cerramos el puntero
texto.close()
archivo.close()

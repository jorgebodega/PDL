import library.ply.lex as lex

# Lista de palabras reservadas.
reserved = ('true','false','var','function','int','bool','chars','write','prompt','return','switch','case','break','if')

# Lista de operadores
operators = ('*','>','!','=','++','(',')','{','}',':','-')

# Lista con los identificadores que iremos añadiendo
ids = []

# Lista con los diferentes tipos de tokens
tokens = ('NUM','CAD','OP','ID','PalRes','EOF') #El token EOF lo meto al final a lo bruto

# Lista de tokens que va sacando el analizador
toks = []

# Expresión regular que nos permite identificar cadenas de números, empiecen o no por un -
def t_NUM(t):
    r'\d+|\-{1}\d+'
    t.value = int(t.value)    
    return t

# Expresión regular que nos permite identificar operadores. Cambiamos el valor a devolver para ordenar la lista
# desde 1 en vez de 0
def t_OP(t):
    r'\*|\>|\!|\=|\+{2}|\(|\)|\{|\}|\:'
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

# Abre el archivo que contiene nuestro programa
texto = open("programa.js","r")

# Nos recorremos el archivo linea a linea
for text in texto:
	lex.input(text) #Añadimos la linea al analizador
	for tok in lexer: #Va recorriendo los caracteres para ir haciendo los tokens
		toks.append(tok)
		print("<" + str(tok.type) + ", " + str(tok.value) + ">") #Imprime el token con el formato <A, B>

print("<" + str(tokens[5]) + ", >") #Imprime el token EOF con el formato <EOF, >
# Nota: no he encontrado la forma de hacerlo, lo dejo así.

#Cerramos el puntero
texto.close()
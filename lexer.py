import library.ply.lex as lex

# Lista de palabras reservadas.
reserved = (
	'true',
	'false',
	'var',
	'function',
	'int',
	'bool',
	'chars',
	'write',
	'prompt',
	'return',
	'switch',
	'case',
	'break',
	'if'
)

operators = (
	'*',
	'>',
	'!',
	'=',
	'++',
	'(',
	')',
	'{',
	'}',
	':',
	'-',
)

ids = []

tokens = (
   'NUM',
   'CAD',
   'OP',
   'ID',
   'PalRes',
   'EOF',
)

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
    r'\'{1}.+\'{1}'
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

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
t_ignore_COMMENT = r'\/{1}\*{1}.+\*{1}\/{1}'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out
texto = open("programa.js","r")

for text in texto:
	print(text)
	lex.input(text)
	# Tokenize
	for tok in lexer:
		print("<" + str(tok.type) + ", " + str(tok.value) + ">")

print(ids)

texto.close()
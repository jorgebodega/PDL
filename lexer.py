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

# A regular expression rule with some action code
def t_NUM(t):
    r'\d+|\-{1}\d+'
    t.value = int(t.value)    
    return t

# A regular expression rule with some action code
def t_OP(t):
    r'\*|\>|\!|\=|\+{2}|\(|\)|\{|\}|\:'
    t.value = int(operators.index(t.value)) + 1  
    return t

# A regular expression rule with some action code
def t_CAD(t):
    r'\'{1}([a-z]|[A-Z])+\'{1}'
    t.value = str(t.value) 
    return t

# A regular expression rule with some action code
def t_PalRes(t):
	r'([a-z]|[A-Z]){1}.+([a-z]|[A-Z]){1}'
	try:
		t.value = int(reserved.index(t.value)) + 1
		return t
	except Exception as e:
		return t_ID(t)
		pass


def t_ID(t):
	r'([a-z]|[A-Z]){1}.+([a-z]|[A-Z]){1}'
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

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out
data = '''
3
4
++
}
-20
20
(
'Hola'
'Adios'
break
40
bool
jjiji
hjnfb66gfjw
hjnfb66gfjw
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
for tok in lexer:
  print(tok)
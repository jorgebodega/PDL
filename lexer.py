import library.ply.lex as lex

# Lista de palabras reservadas.
reserved = {
	'true' : 'TRUE',
	'false' : 'FALSE',
	'var' : 'VAR',
	'function' : 'FUNC',
	'int' : 'INT', 
	'bool' : 'BOOL',
	'chars' : 'CHARS',
	'write' : 'WRITE',
	'prompt' : 'PROMPT',
	'return' : 'RETURN',
	'switch' : 'SWITCH',
	'case' : 'CASE',
	'break' : 'BREAK',
	'if' : 'IF',
}

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

id = []

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
    r'\d+'
    t.value = int(t.value)    
    return t

# A regular expression rule with some action code
def t_OP(t):
    r'\*|\>|\!|\=|\+{2}|\(|\)|\{|\}|\:|\-'
    t.value = int(operators.index(t.value)) + 1  
    return t

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
3 ++ 4 * 10
  ++ -20 *2
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
for tok in lexer:
  print(tok)
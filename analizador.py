import os
import lexico
import sintactico

# Puntero a los ficheros que iremos creando o usando
fichero_codigo = open('code.js', 'r')
fichero_salida = open('tokens.txt', 'w')
fichero_ts = open('tabla_simbolos.txt', 'w')
fichero_parse = open('parse.txt', 'w')
fichero_error = open('error.txt', 'w')

# Inicializamos el Analizador Lexico
lexer = lexico.AnLex(fs=fichero_salida, fe=fichero_error)
yacc = sintactico.AnSit(lexer, fichero_codigo, fichero_ts, fichero_parse, fichero_error, True)

yacc.analize()

# Cerramos descriptores de ficheros
fichero_codigo.close()
fichero_error.close()
fichero_ts.close()
fichero_salida.close()
fichero_parse.close()

if os.stat('error.txt').st_size == 0:
    os.remove('error.txt')
if os.stat('parse.txt').st_size == 0:
    os.remove('parse.txt')
if os.stat('tabla_simbolos.txt').st_size == 0:
    os.remove('tabla_simbolos.txt')

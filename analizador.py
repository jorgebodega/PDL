import sys
import sintactico

# Puntero a los ficheros que iremos creando o usando
fichero_codigo = open('code.js', 'r')
fichero_salida = open('tokens.txt', 'w')
fichero_ts = open('tabla_simbolos.txt', 'w')
fichero_parse = open('parse.txt', 'w')
fichero_error = open('error.txt', 'w')

# Inicializamos el Analizador
flag_imprimir = False
if len(sys.argv) > 1:
    flag_imprimir = sys.argv[1]

yacc = sintactico.AnSit(fichero_codigo, fichero_salida, fichero_ts,
                        fichero_parse, fichero_error, flag_imprimir)

yacc.analize()

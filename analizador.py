import lexico, os

fichero_codigo = open('code.js', 'r')
fichero_salida = open('tokens.txt', 'w')
fichero_error = open('error.txt', 'w')

lexer = lexico.AnLex(fs=fichero_salida, fe=fichero_error)
lexer.build()

tokensTotales = []

for linea in fichero_codigo:
    tokens = lexer.tokenizeLine(linea)
    tokensTotales.append(tokens)

# Cerramos descriptores de ficheros
fichero_codigo.close()
fichero_error.close()

# Si no hemos tenido errores
if not lexer.getErrorCheck():
    # Insertamos el token de fin de fichero
    tokenEOF = lexico.Token('fin_fich', 'eof', None, None)
    fichero_salida.write(str(tokenEOF))
    tokensTotales.append([tokenEOF])

# Cerramos descriptor de fichero
fichero_salida.close()

if os.stat('error.txt').st_size == 0:
    os.remove('error.txt')

# for token in tokensTotales:
#    print(str(token))

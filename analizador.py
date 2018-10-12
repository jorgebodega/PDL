import lexico

fichero_prueba = open('prueba.js', 'r')
fichero_salida = open('tokens_salida.txt', 'w')

lexer = lexico.AnLex(fd=fichero_salida)
lexer.build()

tokensTotales = []

for linea in fichero_prueba:
    tokens = lexer.tokenizeLine(linea)
    tokensTotales.append(tokens)

# Insertamos el token de fin de fichero
tokenEOF = lexico.Token('fin_fich', 'eof', None, None)
fichero_salida.write(str(tokenEOF))
tokensTotales.append([tokenEOF])

for token in tokensTotales:
    print(str(token))
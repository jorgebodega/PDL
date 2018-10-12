import lexico

fichero_prueba = open('prueba.js', 'r')
fichero_salida = open('tokens_salida.txt', 'w')

lexer = lexico.AnLex(fd=fichero_salida)
lexer.build()

tokensTotales = []

for linea in fichero_prueba:
    tokens = lexer.tokenizeLine(linea)
    tokensTotales.append(tokens)
# Insertamos aqui uno a mano con el final de fichero
for token in tokensTotales:
    print(str(token))
print('\n' + str(lexer.id))
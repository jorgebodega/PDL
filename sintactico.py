import os
import lexico
import tabla

class AnSit:

    def __init__(self, analizador, f_c, f_t, f_p, f_e):
        self.analizador = analizador
        self.fichero_codigo = f_c
        self.fichero_tablas = f_t
        self.fichero_parse = f_p
        self.fichero_error = f_e
        self.tokens = []
        self.ptrTokens = 0
        self.parse = 'Des '
        self.palRes = analizador.getPalRes()
        self.tablaSimbolos = tabla.TablaSimbolos()
        self.analizador.build()
        self.getNewTokens()

    def S0(self):
        '''S0 -> S'''
        self.parse += '1 '
        self.S()
    def S(self):
        '''S -> A ; S | D ; S | C S | F S | ε'''
        # Comprobamos si el siguiente token esta en el first del no terminal
        if self.tokens[self.ptrTokens].tipo == 'PR':
            if self.palRes[self.tokens[self.ptrTokens].valor] in ['id']:
                self.parse += '2 '
                self.A()
                self.checkToken('op_ptocoma')
                self.S()
            if self.palRes[self.tokens[self.ptrTokens].valor] in ['var']:
                self.parse += '3 '
                self.D()
                self.checkToken('op_ptocoma')
                self.S()
            if self.palRes[self.tokens[self.ptrTokens].valor] in ['if', 'for', 'print', 'prompt', 'return']:
                self.parse += '4 '
                self.C()
                self.S()
            if self.palRes[self.tokens[self.ptrTokens].valor] in ['function']:
                self.parse += '5 '
                self.F()
                self.S()
        else:
            pass
    def A(self):
        '''A -> id E2'''
        self.parse += '7 '
        self.checkToken('ID')
        self.E2()
    def A1(self):
        '''A1 -> A | ε'''
    def A2(self):
        '''A2 -> id A3 | ε'''
    def A3(self):
        '''A3 -> = E | ++'''
    def A4(self):
        '''A4 -> C A4 | D ; A4 | A ; A4 | ε'''
    def D(self):
        '''D -> var D1 id'''
    def D1(self):
        '''D1 -> int | bool | String'''
    def D2(self):
        '''D2 -> D1 | ε'''
    def C(self):
        '''C -> if ( E ) S1 ; | for ( A1 ; E ; A2 ) { A4 } | S1 ;'''
    def F(self):
        '''F -> function D2 id ( F1 ) { C }'''
    def F1(self):
        '''F1 -> F2 F3'''
    def F2(self):
        '''F2 -> D | id | ε'''
    def F3(self):
        '''F3 -> , F1 | ε'''
    def S1(self):
        '''S1 -> print ( E ) | prompt ( id ) | return E1'''
    def E(self):
        '''E -> G E2'''
    def E1(self):
        '''E1 -> E | ε'''
    def E2(self):
        '''E2 -> && E | ε'''
    def G(self):
        '''G -> H G1'''
    def G1(self):
        '''G1 -> == G | != G | ε'''
    def H(self):
        '''H -> I H1'''
    def H1(self):
        '''H1 -> + H | - H | ε'''
    def I(self):
        '''I -> id J | ( E ) | entero | cadena | True | False'''
    def J(self):
        '''J -> ++ | ( Z ) | ε'''
    def Z(self):
        '''Z -> id Z1 | ε'''
    def Z1(self):
        '''Z1 -> , id Z1 | ε'''

    def getNewTokens(self):
        newLine = self.fichero_codigo.readline()
        if newLine is None:
            tokenEOF = lexico.Token('fin_fich', 'eof', lexer.lineaActual(), 0)
            fichero_salida.write(str(tokenEOF))
            self.tokens.append(tokenEOF)
        else:
            newTokens = lexer.tokenizeLine(newLine)
            for token in newTokens:
                self.tokens.append(token)

    def checkToken(self, tipo):
        if self.tokens[self.ptrTokens].tipo == tipo:
            self.ptrTokens += 1
            if self.ptrTokens == len(self.tokens):
                self.getNewTokens()
        else:
            pass
            # Lanzar error
            # Error_Sin()

# Puntero a los ficheros que iremos creando o usando
fichero_codigo = open('code.js', 'r')
fichero_salida = open('tokens.txt', 'w')
fichero_ts = open('tabla_simbolos.txt', 'w')
fichero_parse = open('parse.txt', 'w')
fichero_error = open('error.txt', 'w')

# Inicializamos el Analizador Lexico
lexer = lexico.AnLex(fs=fichero_salida, fe=fichero_error)
yacc = AnSit(lexer, fichero_codigo, fichero_ts, fichero_parse, fichero_error)

# Cerramos descriptores de ficheros
fichero_codigo.close()
fichero_error.close()

fichero_ts.write(str(yacc.tablaSimbolos))
fichero_parse.write(yacc.parse)

# Cerramos descriptor de fichero
fichero_ts.close()
fichero_salida.close()
fichero_parse.close()

if os.stat('error.txt').st_size == 0:
    os.remove('error.txt')


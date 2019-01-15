import tabla


class AnSit:

    def __init__(self, analizador, fichero_codigo, fichero_tablas,
                 fichero_parse, fichero_error, flag_imprimir=False):
        self.flag = flag_imprimir
        self.analizador = analizador
        self.fichero_codigo = fichero_codigo
        self.fichero_tablas = fichero_tablas
        self.fichero_parse = fichero_parse
        self.fichero_error = fichero_error
        self.tokens = []
        self.ptrTokens = 0
        self.parse = 'Des '  # Analizador descendente recursivo
        self.palRes = analizador.palabras_reservadas
        self.tabla_simbolos = tabla.TablaSimbolos()
        self.analizador.build()

    def s0(self):
        print('S0 -> S' if self.flag else '')
        self.parse += '1 '

        # Semantico
        self.tabla_simbolos.iniciar_tabla_simbolos()
        # Semantico

        self.s()
        # No hace falta destruir la tabla de simbolos, el programa para la ejecucion aqui

    def s(self):
        print('S -> A ; S | D ; S | C S | F S | λ' if self.flag else '')
        if self.ptrTokens == len(self.tokens):
            self.parse += '6 '
        elif self.tokens[self.ptrTokens].tipo == 'ID':
            self.parse += '2 '
            self.a()
            self.checkToken('op_ptocoma')
            self.s()
        elif self.tokens[self.ptrTokens].tipo == 'PR':
            if self.palRes[self.tokens[self.ptrTokens].valor - 1] == 'var':
                self.parse += '3 '
                self.d()
                self.checkToken('op_ptocoma')
                self.s()
            elif self.palRes[self.tokens[self.ptrTokens].valor - 1] in ['if', 'for', 'print', 'prompt', 'return']:
                self.parse += '4 '
                self.c()
                self.s()
            elif self.palRes[self.tokens[self.ptrTokens].valor - 1] == 'function':
                self.parse += '5 '
                self.f()
                self.s()

    def a(self):
        print('A -> id = E' if self.flag else '')
        self.parse += '7 '
        self.checkToken('ID')

        # Semantico
        lexema = self.analizador.getLexema(self.tokens[self.ptrTokens - 1].valor - 1)
        print(lexema)
        if not self.tabla_simbolos.comprobar_lexema(lexema):
            self.error_semantico()
        tipo_lexema = self.tabla_simbolos.tipo_lexema(lexema)
        # Semantico

        self.checkToken('op_asignacion')

        # Semantico
        retorno_e = self.e()
        tipo_dato, size = retorno_e  # TODO: Posiblemente podemos adaptar el retorno y que no traiga el tamaño.
        if tipo_lexema != tipo_dato:
            self.error_semantico()
        # Semantico
    
    def a1(self):
        print('A1 -> A | λ' if self.flag else '')
        if self.tokens[self.ptrTokens].tipo == 'ID':
            self.parse += '8 '
            self.a()
        else:
            self.parse += '9 '

    def a2(self):
        print('A2 -> id A3 | λ' if self.flag else '')
        if self.tokens[self.ptrTokens].tipo == 'ID':
            self.parse += '10 '
            self.checkToken('ID')
            self.a3()
        else:
            self.parse += '11 '

    def a3(self):
        print('A3 -> = E | ++' if self.flag else '')
        if self.tokens[self.ptrTokens].tipo == 'op_asignacion':
            self.parse += '12 '
            self.checkToken('op_asignacion')
            self.e()
        elif self.tokens[self.ptrTokens].tipo == 'op_posinc':
            self.parse += '13 '
            self.checkToken('op_posinc')

    def a4(self):
        print('A4 -> C A4 | D ; A4 | A ; A4 | λ' if self.flag else '')
        if self.tokens[self.ptrTokens].tipo == 'PR':
            if self.palRes[self.tokens[self.ptrTokens].valor - 1] in ['if', 'for', 'print', 'prompt', 'return']:
                self.parse += '14 '
                self.c()
                self.a4()
            elif self.palRes[self.tokens[self.ptrTokens].valor - 1] == 'var':
                self.parse += '15 '
                self.d()
                self.checkToken('op_ptocoma')
                self.a4()
        elif self.tokens[self.ptrTokens].tipo == 'ID':
            self.parse += '16 '
            self.a()
            self.checkToken('op_ptocoma')
            self.a4()
        else:
            self.parse += '17 '

    def d(self):
        print('D -> var D1 id' if self.flag else '')
        self.parse += '18 '
        self.checkToken('PR', 'var')

        # Semantico
        retorno_d1 = self.d1()

        if retorno_d1 is None:
            self.error_semantico()
        # Semantico

        self.checkToken('ID')

        # Semantico
        lexema = self.analizador.getLexema(self.tokens[self.ptrTokens - 1].valor - 1)
        if self.tabla_simbolos.comprobar_lexema(lexema):
            self.error_semantico()
        tipo_dato, size = retorno_d1
        self.tabla_simbolos.insertar_lexema(lexema, tipo_dato, size)
        # Semantico

    def d1(self):
        print('D1 -> int | bool | String' if self.flag else '')

        # Semantico
        valor_retorno = None  # Valor por defecto a None
        # Semantico

        if self.tokens[self.ptrTokens].tipo == 'PR':
            if self.palRes[self.tokens[self.ptrTokens].valor - 1] == 'int':
                self.parse += '19 '
                self.checkToken('PR', 'int')

                # Semantico
                valor_retorno = ['entero', 4]  # Enteros de 4 bytes
                # Semantico

            elif self.palRes[self.tokens[self.ptrTokens].valor - 1] == 'bool':
                self.parse += '20 '
                self.checkToken('PR', 'bool')

                # Semantico
                valor_retorno = ['logico', 1]  # Booleanos de 1 byte
                # Semantico

            elif self.palRes[self.tokens[self.ptrTokens].valor - 1] == 'String':
                self.parse += '21 '
                self.checkToken('PR', 'String')

                # Semantico
                valor_retorno = ['cadena', 4]  # Cadenas de 4 bytes (Provisionalmente)
                # Semantico

        # Semantico
        return valor_retorno
        # Semantico

    def d2(self):
        print('D2 -> D1 | λ' if self.flag else '')

        # Semantico
        valor_retorno = ['vacio', 0]  # Valor por defecto a vacio -> void
        # Semantico

        first_d1 = (self.tokens[self.ptrTokens].tipo == 'PR' and
                    self.palRes[self.tokens[self.ptrTokens].valor - 1] in ['int', 'bool', 'String'])
        if first_d1:
            self.parse += '22 '

            # Semantico
            valor_retorno = self.d1()
            # Semantico

        else:
            self.parse += '23 '

        # Semantico
        return valor_retorno
        # Semantico

    def c(self):
        print('C -> if ( E ) S1 ; | for ( A1 ; E ; A2 ) { A4 } | S1 ;' if self.flag else '')
        if self.tokens[self.ptrTokens].tipo == 'PR':
            if self.palRes[self.tokens[self.ptrTokens].valor - 1] == 'if':
                self.parse += '24 '
                self.checkToken('PR', 'if')
                self.checkToken('op_parenab')
                self.e()
                self.checkToken('op_parencer')
                self.s1()
                self.checkToken('op_ptocoma')
            elif self.palRes[self.tokens[self.ptrTokens].valor - 1] == 'for':
                self.parse += '25 '
                self.checkToken('PR', 'for')
                self.checkToken('op_parenab')
                self.a1()
                self.checkToken('op_ptocoma')
                self.e()
                self.checkToken('op_ptocoma')
                self.a2()
                self.checkToken('op_parencer')
                self.checkToken('op_llaveab')
                self.a4()
                self.checkToken('op_llavecer')
            elif self.palRes[self.tokens[self.ptrTokens].valor - 1] in ['print', 'prompt', 'return']:
                self.parse += '26 '
                self.s1()
                self.checkToken('op_ptocoma')

    def f(self):
        print('F -> function D2 id ( F1 ) { A4 }' if self.flag else '')
        self.parse += '27 '
        self.checkToken('PR', 'function')

        # Semantico
        tipo_retorno_funcion = self.d2()
        # Semantico

        self.checkToken('ID')

        # Semantico
        lexema = self.analizador.getLexema(self.tokens[self.ptrTokens - 1].valor - 1)
        if not self.tabla_simbolos.comprobar_lexema(lexema):
            self.error_semantico()
        # No deberia llegar nunca a este error, no puede darse el caso
        # elif not self.tabla_simbolos.is_tablageneral():
        #     self.error_sintactico()
        else:
            self.tabla_simbolos.insertarFuncion(lexema)
        # Semantico

        self.checkToken('op_parenab')
        self.f1()
        self.checkToken('op_parencer')
        self.checkToken('op_llaveab')
        self.a4()
        self.checkToken('op_llavecer')

        # Semantico
        self.tabla_simbolos.removeTabla()
        # Semantico

    def f1(self):
        print('F1 -> F2 F3' if self.flag else '')
        self.parse += '28 '
        self.f2()
        self.f3()

    def f2(self):
        print('F2 -> D1 id | λ' if self.flag else '')
        firstD1 = self.tokens[self.ptrTokens].tipo == 'PR' and self.palRes[self.tokens[self.ptrTokens].valor - 1] in ['int', 'bool', 'String']
        if firstD1:
            self.parse += '29 '
            self.d1()
            self.checkToken('ID')
        else:
            self.parse += '30 '

    def f3(self):
        print('F3 -> , F1 | λ' if self.flag else '')
        if self.tokens[self.ptrTokens].tipo == 'op_coma':
            self.parse += '31 '
            self.checkToken('op_coma')
            self.f1()
        else:
            self.parse += '32 '

    def s1(self):
        print('S1 -> print ( E ) | prompt ( id ) | return E1' if self.flag else '')
        if self.tokens[self.ptrTokens].tipo == 'PR':
            if self.palRes[self.tokens[self.ptrTokens].valor - 1] == 'print':
                self.parse += '33 '
                self.checkToken('PR', 'print')
                self.checkToken('op_parenab')
                self.e()
                self.checkToken('op_parencer')
            elif self.palRes[self.tokens[self.ptrTokens].valor - 1] == 'prompt':
                self.parse += '34 '
                self.checkToken('PR', 'prompt')
                self.checkToken('op_parenab')
                self.checkToken('ID')
                self.checkToken('op_parencer')
            elif self.palRes[self.tokens[self.ptrTokens].valor - 1] == 'return':
                self.parse += '35 '
                self.checkToken('PR', 'return')
                self.e1()

    def e(self):
        print('E -> G E2' if self.flag else '')
        self.parse += '36 '
        self.g()
        self.e2()

    def e1(self):
        print('E1 -> E | λ' if self.flag else '')
        firstE = ((self.tokens[self.ptrTokens].tipo == 'PR' and
                   self.palRes[self.tokens[self.ptrTokens].valor - 1] in ['True', 'False']) or
                  self.tokens[self.ptrTokens].tipo in ['op_parenab', 'entero', 'cadena'] or
                  self.tokens[self.ptrTokens].tipo == 'ID')
        if firstE:
            self.parse += '37 '
            self.e()
        else:
            self.parse += '38 '

    def e2(self):
        print('E2 -> && E | λ' if self.flag else '')
        if self.tokens[self.ptrTokens].tipo == 'op_and':
            self.parse += '39 '
            self.checkToken('op_and')
            self.e()
        else:
            self.parse += '40 '

    def g(self):
        print('G -> H G1' if self.flag else '')
        self.parse += '41 '
        self.h()
        self.g1()

    def g1(self):
        print('G1 -> == G | != G | λ' if self.flag else '')
        if self.tokens[self.ptrTokens].tipo == 'op_igual':
            self.parse += '42 '
            self.checkToken('op_igual')
            self.g()
        elif self.tokens[self.ptrTokens].tipo == 'op_noigual':
            self.parse += '43 '
            self.checkToken('op_noigual')
            self.g()
        else:
            self.parse += '44 '

    def h(self):
        print('H -> I H1' if self.flag else '')
        self.parse += '45 '
        self.i()
        self.h1()

    def h1(self):
        print('H1 -> + H | - H | λ' if self.flag else '')
        if self.tokens[self.ptrTokens].tipo == 'op_suma':
            self.parse += '46 '
            self.checkToken('op_suma')
            self.h()
        elif self.tokens[self.ptrTokens].tipo == 'op_resta':
            self.parse += '47 '
            self.checkToken('op_resta')
            self.h()
        else:
            self.parse += '48 '

    def i(self):
        print('I -> id J | ( E ) | entero | cadena | True | False' if self.flag else '')
        if self.tokens[self.ptrTokens].tipo == 'ID':
            self.parse += '49 '
            self.checkToken('ID')
            self.j()
        elif self.tokens[self.ptrTokens].tipo == 'op_parenab':
            self.parse += '50 '
            self.checkToken('op_parenab')
            self.e()
            self.checkToken('op_parencer')
        elif self.tokens[self.ptrTokens].tipo == 'entero':
            self.parse += '51 '
            self.checkToken('entero')
        elif self.tokens[self.ptrTokens].tipo == 'cadena':
            self.parse += '52 '
            self.checkToken('cadena')
        elif self.tokens[self.ptrTokens].tipo == 'PR':
            if self.palRes[self.tokens[self.ptrTokens].valor - 1] == 'True':
                self.parse += '53 '
                self.checkToken('PR', 'True')
            elif self.palRes[self.tokens[self.ptrTokens].valor - 1] == 'False':
                self.parse += '54 '
                self.checkToken('PR', 'False')

    def j(self):
        print('J -> ++ | ( Z ) | λ' if self.flag else '')
        if self.tokens[self.ptrTokens].tipo == 'op_posinc':
            self.parse += '55 '
            self.checkToken('op_posinc')
        elif self.tokens[self.ptrTokens].tipo == 'op_parenab':
            self.parse += '56 '
            self.checkToken('op_parenab')
            self.z()
            self.checkToken('op_parencer')
        else:
            self.parse += '57 '

    def z(self):
        print('Z -> id Z1 | λ' if self.flag else '')
        if self.tokens[self.ptrTokens].tipo == 'ID':
            self.parse += '58 '
            self.checkToken('ID')
            self.z1()
        else:
            self.parse += '59 '

    def z1(self):
        print('Z1 -> , id Z1 | λ' if self.flag else '')
        if self.tokens[self.ptrTokens].tipo == 'op_coma':
            self.parse += '60 '
            self.checkToken('op_coma')
            self.checkToken('ID')
            self.z1()
        else:
            self.parse += '61 '

    def analize(self):
        self.getNewTokens()
        self.s0()
        self.fichero_parse.write(self.parse)
        self.fichero_tablas.write(str(self.tabla_simbolos))

    def getNewTokens(self):
        newLine = self.fichero_codigo.readline()
        if len(newLine) != 0:
            newTokens = self.analizador.tokenizeLine(newLine)
            if (len(newTokens) != 0):
                for token in newTokens:
                    self.tokens.append(token)
            else: self.getNewTokens()

    def checkToken(self, tipo, possibleValue = None):
        if self.tokens[self.ptrTokens].tipo == tipo:
            if self.tokens[self.ptrTokens].tipo == 'ID':
                self.tabla_simbolos.insertarLexema(self.analizador.getLexema(self.tokens[self.ptrTokens].valor - 1))
            if possibleValue is None or self.palRes[self.tokens[self.ptrTokens].valor - 1] == possibleValue:
                self.ptrTokens += 1  # TODO: Posiblemente toca pasarla a cada vez que se accede al lexema
                if self.ptrTokens == len(self.tokens):
                    self.getNewTokens()
            else:
                self.error_sintactico()
        else:
            self.error_sintactico()

    def error_sintactico(self):
        error = 'Error Sintáctico (Linea %d): Token %s erroneo' % (self.analizador.lineaActual() - 1,
                                                                   str(self.tokens[self.ptrTokens]))
        self.fichero_error.write(error)
        exit()

    def error_semantico(self):
        error = 'Error Semántico (Linea %d): %s <definir errores>' % (self.analizador.lineaActual() - 1,
                                                                      str(self.tokens[self.ptrTokens]))
        self.fichero_error.write(error)
        exit()

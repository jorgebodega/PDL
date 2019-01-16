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
        self.puntero_tokens = 0
        self.parse = 'Des '  # Analizador descendente recursivo
        self.palabras_reservadas = analizador.palabras_reservadas
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
        tipo_token = self.get_tipo()
        if self.puntero_tokens == len(self.tokens):
            self.parse += '6 '
        elif tipo_token == 'ID':
            self.parse += '2 '
            self.a()
            self.check_token('op_ptocoma')
            self.s()
        elif tipo_token == 'PR':
            palabra = self.get_palabra_reservada()
            if palabra == 'var':
                self.parse += '3 '
                self.d()
                self.check_token('op_ptocoma')
                self.s()
            elif palabra in ['if', 'for', 'print', 'prompt', 'return']:
                self.parse += '4 '
                self.c()
                self.s()
            elif palabra == 'function':
                self.parse += '5 '
                self.f()
                self.s()

    def a(self):
        print('A -> id = E' if self.flag else '')
        self.parse += '7 '
        self.check_token('ID')

        # Semantico
        lexema = self.get_lexema()
        # print(lexema)
        if not self.tabla_simbolos.comprobar_lexema(lexema):
            self.error_semantico()
        tipo_lexema = self.tabla_simbolos.tipo_lexema(lexema)
        # Semantico

        self.check_token('op_asignacion')

        # Semantico
        retorno_e = self.e()
        tipo_dato, size = retorno_e  # TODO: Posiblemente podemos adaptar el retorno y que no traiga el tamaño.
        if tipo_lexema != tipo_dato:
            self.error_semantico()
        # Semantico
    
    def a1(self):
        print('A1 -> A | λ' if self.flag else '')
        tipo_token = self.get_tipo()
        if tipo_token == 'ID':
            self.parse += '8 '
            self.a()
        else:
            self.parse += '9 '

    def a2(self):
        print('A2 -> id A3 | λ' if self.flag else '')
        tipo_token = self.get_tipo()
        if tipo_token == 'ID':
            self.parse += '10 '
            self.check_token('ID')
            self.a3()
        else:
            self.parse += '11 '

    def a3(self):
        print('A3 -> = E | ++' if self.flag else '')
        tipo_token = self.get_tipo()
        if tipo_token == 'op_asignacion':
            self.parse += '12 '
            self.check_token('op_asignacion')
            self.e()
        elif tipo_token == 'op_posinc':
            self.parse += '13 '
            self.check_token('op_posinc')

    def a4(self):
        print('A4 -> C A4 | D ; A4 | A ; A4 | λ' if self.flag else '')
        tipo_token = self.get_tipo()
        if tipo_token == 'PR':
            palabra = self.get_palabra_reservada()
            if palabra in ['if', 'for', 'print', 'prompt', 'return']:
                self.parse += '14 '
                self.c()
                self.a4()
            elif palabra == 'var':
                self.parse += '15 '
                self.d()
                self.check_token('op_ptocoma')
                self.a4()
        elif tipo_token == 'ID':
            self.parse += '16 '
            self.a()
            self.check_token('op_ptocoma')
            self.a4()
        else:
            self.parse += '17 '

    def d(self):
        print('D -> var D1 id' if self.flag else '')
        self.parse += '18 '
        self.check_token('PR', 'var')

        # Semantico
        retorno_d1 = self.d1()

        if retorno_d1 is None:
            self.error_semantico()
        # Semantico

        self.check_token('ID')

        # Semantico
        lexema = self.analizador.getLexema(self.tokens[self.puntero_tokens - 1].valor - 1)
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

        if self.get_tipo() == 'PR':
            palabra = self.get_palabra_reservada()
            if palabra == 'int':
                self.parse += '19 '
                self.check_token('PR', 'int')

                # Semantico
                valor_retorno = ['entero', 4]  # Enteros de 4 bytes
                # Semantico

            elif palabra == 'bool':
                self.parse += '20 '
                self.check_token('PR', 'bool')

                # Semantico
                valor_retorno = ['logico', 1]  # Booleanos de 1 byte
                # Semantico

            elif palabra == 'String':
                self.parse += '21 '
                self.check_token('PR', 'String')

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

        tipo_token = self.get_tipo()
        if tipo_token == 'PR':
            palabra = self.get_palabra_reservada()
            if palabra in ['int', 'bool', 'String']:
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

        tipo_token = self.get_tipo()
        if tipo_token == 'PR':
            palabra = self.get_palabra_reservada()
            if palabra == 'if':
                self.parse += '24 '
                self.check_token('PR', 'if')
                self.check_token('op_parenab')
                self.e()
                self.check_token('op_parencer')
                self.s1()
                self.check_token('op_ptocoma')
            elif palabra == 'for':
                self.parse += '25 '
                self.check_token('PR', 'for')
                self.check_token('op_parenab')
                self.a1()
                self.check_token('op_ptocoma')
                self.e()
                self.check_token('op_ptocoma')
                self.a2()
                self.check_token('op_parencer')
                self.check_token('op_llaveab')
                self.a4()
                self.check_token('op_llavecer')
            elif palabra in ['print', 'prompt', 'return']:
                self.parse += '26 '
                self.s1()
                self.check_token('op_ptocoma')

    def f(self):
        print('F -> function D2 id ( F1 ) { A4 }' if self.flag else '')
        self.parse += '27 '
        self.check_token('PR', 'function')

        # Semantico
        tipo_retorno_funcion = self.d2()
        # Semantico

        self.check_token('ID')

        # Semantico
        lexema = self.get_lexema()
        if not self.tabla_simbolos.comprobar_lexema(lexema):
            self.error_semantico()
        # No deberia llegar nunca a este error, no puede darse el caso
        # elif not self.tabla_simbolos.is_tablageneral():
        #     self.error_sintactico()
        else:
            self.tabla_simbolos.insertar_funcion(lexema)
        # Semantico

        self.check_token('op_parenab')
        self.f1()
        self.check_token('op_parencer')
        self.check_token('op_llaveab')
        self.a4()
        self.check_token('op_llavecer')

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

        tipo_token = self.get_tipo()
        if tipo_token == 'PR':
            palabra = self.get_palabra_reservada()
            if palabra in ['int', 'bool', 'String']:
                self.parse += '29 '
                self.d1()
                self.check_token('ID')
        else:
            self.parse += '30 '

    def f3(self):
        print('F3 -> , F1 | λ' if self.flag else '')

        tipo_token = self.get_tipo()
        if tipo_token == 'op_coma':
            self.parse += '31 '
            self.check_token('op_coma')
            self.f1()
        else:
            self.parse += '32 '

    def s1(self):
        print('S1 -> print ( E ) | prompt ( id ) | return E1' if self.flag else '')

        tipo_tokens = self.get_tipo()
        if tipo_tokens == 'PR':

            palabra = self.get_palabra_reservada()
            if palabra == 'print':
                self.parse += '33 '
                self.check_token('PR', 'print')
                self.check_token('op_parenab')
                self.e()
                self.check_token('op_parencer')
            elif palabra == 'prompt':
                self.parse += '34 '
                self.check_token('PR', 'prompt')
                self.check_token('op_parenab')
                self.check_token('ID')
                self.check_token('op_parencer')
            elif palabra == 'return':
                self.parse += '35 '
                self.check_token('PR', 'return')
                self.e1()

    def e(self):
        print('E -> G E2' if self.flag else '')
        self.parse += '36 '
        self.g()
        self.e2()

    def e1(self):
        print('E1 -> E | λ' if self.flag else '')

        tipo_token = self.get_tipo()
        if tipo_token in ['op_parenab', 'entero', 'cadena'] or tipo_token == 'ID':
            self.parse += '37 '
            self.e()
        elif tipo_token == 'PR':
            palabra = self.get_palabra_reservada()
            if palabra in ['True', 'False']:
                self.parse += '37 '
                self.e()
        else:
            self.parse += '38 '

    def e2(self):
        print('E2 -> && E | λ' if self.flag else '')

        tipo_token = self.get_tipo()
        if tipo_token == 'op_and':
            self.parse += '39 '
            self.check_token('op_and')
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

        tipo_token = self.get_tipo()
        if tipo_token == 'op_igual':
            self.parse += '42 '
            self.check_token('op_igual')
            self.g()
        elif tipo_token == 'op_noigual':
            self.parse += '43 '
            self.check_token('op_noigual')
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

        tipo_token = self.get_tipo()
        if tipo_token == 'op_suma':
            self.parse += '46 '
            self.check_token('op_suma')
            self.h()
        elif tipo_token == 'op_resta':
            self.parse += '47 '
            self.check_token('op_resta')
            self.h()
        else:
            self.parse += '48 '

    def i(self):
        print('I -> id J | ( E ) | entero | cadena | True | False' if self.flag else '')

        tipo_token = self.get_tipo()
        if tipo_token == 'ID':
            self.parse += '49 '
            self.check_token('ID')
            self.j()
        elif tipo_token == 'op_parenab':
            self.parse += '50 '
            self.check_token('op_parenab')
            self.e()
            self.check_token('op_parencer')
        elif tipo_token == 'entero':
            self.parse += '51 '
            self.check_token('entero')
        elif tipo_token == 'cadena':
            self.parse += '52 '
            self.check_token('cadena')
        elif tipo_token == 'PR':
            palabra = self.get_palabra_reservada()
            if palabra == 'True':
                self.parse += '53 '
                self.check_token('PR', 'True')
            elif palabra == 'False':
                self.parse += '54 '
                self.check_token('PR', 'False')

    def j(self):
        print('J -> ++ | ( Z ) | λ' if self.flag else '')

        tipo_token = self.get_tipo()
        if tipo_token == 'op_posinc':
            self.parse += '55 '
            self.check_token('op_posinc')
        elif tipo_token == 'op_parenab':
            self.parse += '56 '
            self.check_token('op_parenab')
            self.z()
            self.check_token('op_parencer')
        else:
            self.parse += '57 '

    def z(self):
        print('Z -> id Z1 | λ' if self.flag else '')

        tipo_token = self.get_tipo()
        if tipo_token == 'ID':
            self.parse += '58 '
            self.check_token('ID')
            self.z1()
        else:
            self.parse += '59 '

    def z1(self):
        print('Z1 -> , id Z1 | λ' if self.flag else '')

        tipo_token = self.get_tipo()
        if tipo_token == 'op_coma':
            self.parse += '60 '
            self.check_token('op_coma')
            self.check_token('ID')
            self.z1()
        else:
            self.parse += '61 '

    def analize(self):
        """Ejecuta el programa e inserta los resultados en los fichero correspondientes."""
        self.get_newtokens()  # Obtiene los primeros tokens del fichero de codigo.
        self.s0()  # Inicia la ejecucion.
        self.fichero_parse.write(self.parse)
        self.fichero_tablas.write(str(self.tabla_simbolos))

    def get_newtokens(self):
        """Obtiene los tokens correspodientes a la siguiente linea de codigo, hasta que se acaba el fichero."""
        new_line = self.fichero_codigo.readline()
        if len(new_line) != 0:
            new_tokens = self.analizador.tokenize_line(new_line)
            self.tokens += new_tokens
            if len(new_tokens) == 0:
                self.get_newtokens()

    def get_palabra_reservada(self):
        """
        Obtiene la palabra reservada correspodiente al token actualmente apuntado.
        :return: Palabra reservada | None
        """
        return self.analizador.get_palabra_reservada(self.tokens[self.puntero_tokens].valor - 1)

    def get_tipo(self):
        """Devuelve el tipo del token apuntado actualmente."""
        return self.tokens[self.puntero_tokens].tipo

    def check_token(self, tipo, possible_value = None):
        """
        Comprueba que el token apuntado actualmente es del tipo indicado.
        Si lo es, avanza el puntero, si no lanza error sintactico.
        :param tipo: Tipo esperado para el token.
        :param possible_value: Posible valor que puede esperar en caso de ser una palabra reservada.
        """
        if self.tokens[self.puntero_tokens].tipo == tipo:
            palabra = self.get_palabra_reservada()
            if possible_value is None or palabra == possible_value:
                self.puntero_tokens += 1
                if self.puntero_tokens == len(self.tokens):  # En caso de llegar el final del array, rellenamos.
                    self.get_newtokens()
            else:
                self.error_sintactico()
        else:
            self.error_sintactico()

    def get_lexema(self):
        """
        Devuelve el lexema actualmente apuntado.
        :return: Valor del lexema | None
        """
        return self.analizador.get_lexema(self.tokens[self.puntero_tokens].valor - 1)

    def error_sintactico(self):
        """Inserta el error en el fichero correspondiente y paramos la ejecucion del programa."""
        error = 'Error Sintáctico (Linea %d): Token %s erroneo' % (self.analizador.lineaActual() - 1,
                                                                   str(self.tokens[self.puntero_tokens]))
        self.fichero_error.write(error)
        print(error if self.flag else '')
        exit()

    def error_semantico(self, mensaje='<Mensaje no definido>'):
        """Inserta el error en el fichero correspondiente y paramos la ejecucion del programa."""
        error = 'Error Semántico (Linea %d): ' % self.analizador.lineaActual() - 1
        error += mensaje
        self.fichero_error.write(error)
        print(error if self.flag else '')
        exit()

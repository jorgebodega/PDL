import tabla
import lexico
# TODO REVISAR TODOS LOS NUMEROS DEL PARSE.
# TODO Cambiar el self.flag por self.flar_imprimir.
# TODO Revisar mensajes de error.

sizes = {
    'entero': 2,
    'logico': 1,
    'cadena': 256,
    'funcion': 2  # Puntero
}


class AnSit:

    def __init__(self, fichero_codigo, fichero_salida, fichero_tablas,
                 fichero_parse, fichero_error, flag_imprimir=False):
        self.flag = flag_imprimir
        self.fichero_codigo = fichero_codigo
        self.fichero_tablas = fichero_tablas
        self.fichero_parse = fichero_parse
        self.fichero_error = fichero_error
        self.tokens = []
        self.puntero_tokens = 0
        self.parse = 'Descendente '  # Analizador descendente recursivo
        self.tabla_simbolos = tabla.TablaSimbolos()
        self.analizador = lexico.AnLex(fichero_salida, fichero_error, self.tabla_simbolos)
        self.analizador.build()
        self.palabras_reservadas = self.analizador.palabras_reservadas

    def s0(self):
        print('S0 -> S' if self.flag else '')
        self.parse += '1 '

        # Semantico
        self.tabla_simbolos.iniciar_tabla_simbolos()
        self.get_newtokens()
        # Semantico

        self.s()
        # No hace falta destruir la tabla de simbolos, el programa para la ejecucion aqui

    def s(self):
        print('S -> A ; S | D ; S | C S | F S | λ' if self.flag else '')
        tipo_token = self.get_tipo_token()
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

                # Semantico
                retorno_c = self.c()
                if retorno_c is not None:
                    self.error_semantico('No puede usarse un return fuera del ambito de una funcion.')
                # Semantico

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
        if not self.tabla_simbolos.is_defined(lexema):
            self.tabla_simbolos.insertar_lexema_global(lexema, 'entero', sizes['entero'])
            tipo_lexema = 'entero'
        else:
            tipo_lexema = self.tabla_simbolos.tipo_lexema(lexema)
        # Semantico

        self.check_token('op_asignacion')

        # Semantico
        tipo_dato = self.e()
        if tipo_lexema != tipo_dato:
            self.error_semantico('El tipo de dato es diferente al tipo del identificador.')
        # Semantico
    
    def a1(self):
        print('A1 -> A | λ' if self.flag else '')
        tipo_token = self.get_tipo_token()
        if tipo_token == 'ID':
            self.parse += '8 '
            self.a()
        else:
            self.parse += '9 '

    def a2(self):
        print('A2 -> id A3 | λ' if self.flag else '')
        tipo_token = self.get_tipo_token()
        if tipo_token == 'ID':
            self.parse += '10 '
            self.check_token('ID')

            # Semantico
            lexema = self.get_lexema()
            if not self.tabla_simbolos.is_defined(lexema):
                self.tabla_simbolos.insertar_lexema_global(lexema, 'entero', sizes['entero'])
                tipo_lexema = 'entero'
            else:
                tipo_lexema = self.tabla_simbolos.tipo_lexema(lexema)
            tipo_retorno = self.a3()
            if tipo_retorno != tipo_lexema:
                self.error_semantico('La operacion no puede realizarse sobre tipos diferentes de datos.')
            # Semantico
        else:
            self.parse += '11 '

    def a3(self):
        print('A3 -> = E | ++' if self.flag else '')
        tipo_token = self.get_tipo_token()
        if tipo_token == 'op_asignacion':
            self.parse += '12 '
            self.check_token('op_asignacion')

            # Semantico
            return self.e()
            # Semantico
        elif tipo_token == 'op_posinc':
            self.parse += '13 '
            self.check_token('op_posinc')

            # Semantico
            return 'entero'
            # Semantico

    def a4(self):
        print('A4 -> C A4 | D ; A4 | A ; A4 | λ' if self.flag else '')
        tipo_token = self.get_tipo_token()
        if tipo_token == 'PR':
            palabra = self.get_palabra_reservada()
            if palabra in ['if', 'for', 'print', 'prompt', 'return']:
                self.parse += '14 '

                # Semantico
                valor_return = self.c()
                retorno_a4 = self.a4()
                return retorno_a4 if valor_return is None else valor_return
                # Semantico
            elif palabra == 'var':
                self.parse += '15 '
                self.d()
                self.check_token('op_ptocoma')

                # Semantico
                return self.a4()
                # Semantico
        elif tipo_token == 'ID':
            self.parse += '16 '
            self.a()
            self.check_token('op_ptocoma')

            # Semantico
            return self.a4()
            # Semantico
        else:
            self.parse += '17 '

            # Semantico
            return
            # Semantico

    def d(self):
        print('D -> var D1 id' if self.flag else '')
        self.parse += '18 '
        self.check_token('PR', 'var')

        # Semantico
        retorno_d1 = self.d1()
        # Semantico

        self.check_token('ID')

        # Semantico
        lexema = self.get_lexema()
        if self.tabla_simbolos.is_defined_only_in_pointer(lexema):
            self.error_semantico("Identificador ya definido.")
        tipo_dato = retorno_d1
        self.tabla_simbolos.insertar_lexema(lexema, tipo_dato, sizes[tipo_dato])
        # Semantico

    def d1(self):
        print('D1 -> int | bool | String' if self.flag else '')

        # Semantico
        valor_retorno = None  # Valor por defecto a None
        # Semantico

        if self.get_tipo_token() == 'PR':
            palabra = self.get_palabra_reservada()
            if palabra == 'int':
                self.parse += '19 '
                self.check_token('PR', 'int')

                # Semantico
                valor_retorno = 'entero'
                # Semantico

            elif palabra == 'bool':
                self.parse += '20 '
                self.check_token('PR', 'bool')

                # Semantico
                valor_retorno = 'logico'
                # Semantico

            elif palabra == 'String':
                self.parse += '21 '
                self.check_token('PR', 'String')

                # Semantico
                valor_retorno = 'cadena'
                # Semantico

        # Semantico
        return valor_retorno
        # Semantico

    def d2(self):
        print('D2 -> D1 | λ' if self.flag else '')

        # Semantico
        valor_retorno = 'vacio'  # Valor por defecto a vacio -> void
        # Semantico

        tipo_token = self.get_tipo_token()
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
        print('C -> if ( E ) S1 ; | for ( A1 ; E ; A2 ) { A4 } | S2 ;' if self.flag else '')

        tipo_token = self.get_tipo_token()
        if tipo_token == 'PR':
            palabra = self.get_palabra_reservada()
            if palabra == 'if':
                self.parse += '24 '
                self.check_token('PR', 'if')
                self.check_token('op_parenab')

                # Semantico
                retorno_e = self.e()
                if retorno_e != 'logico':
                    self.error_semantico('La evaluacion de un if debe ser un valor logico')
                # Semantico

                self.check_token('op_parencer')

                # Semantico
                retorno_s1 = self.s1()
                # Semantico

                self.check_token('op_ptocoma')

                # Semantico
                return retorno_s1
                # Semantico
            elif palabra == 'for':
                self.parse += '25 '
                self.check_token('PR', 'for')
                self.check_token('op_parenab')
                self.a1()
                self.check_token('op_ptocoma')

                # Semantico
                retorno_e = self.e()
                if retorno_e != 'logico':
                    self.error_semantico('La evaluacion de un if debe ser un valor logico')
                # Semantico

                self.check_token('op_ptocoma')
                self.a2()
                self.check_token('op_parencer')
                self.check_token('op_llaveab')

                # Semantico
                retorno_a4 = self.a4()
                # Semantico

                self.check_token('op_llavecer')

                # Semantico
                return retorno_a4
                # Semantico
            elif palabra in ['print', 'prompt', 'return']:
                self.parse += '26 '

                # Semantico
                retorno_s2 = self.s2()
                # Semantico

                self.check_token('op_ptocoma')

                # Semantico
                return retorno_s2
                # Semantico

    def f(self):
        print('F -> function D2 id ( F1 ) { A4 }' if self.flag else '')
        self.parse += '27 '
        self.check_token('PR', 'function')

        # Semantico
        tipo_funcion = self.d2()
        # Semantico

        self.check_token('ID')

        # Semantico
        lexema = self.get_lexema()
        if self.tabla_simbolos.is_defined(lexema):
            self.error_semantico("Identificador ya definido.")
        # Semantico

        self.check_token('op_parenab')

        # Semantico
        parametros = self.f1()
        self.tabla_simbolos.insertar_funcion(lexema, sizes['funcion'], parametros, tipo_funcion)
        # Semantico

        self.check_token('op_parencer')
        self.check_token('op_llaveab')

        # Semantico
        tipo_retorno = self.a4()
        if (tipo_funcion != 'vacio' and tipo_retorno != tipo_funcion) or \
           (tipo_funcion == 'vacio' and tipo_retorno is not None):
            self.error_semantico("El tipo de retorno no coincide con el especificado en la declaración.")
        self.tabla_simbolos.remove_tabla()
        # Semantico

        self.check_token('op_llavecer')

    def f1(self):
        print('F1 -> F2 | λ' if self.flag else '')
        tipo_token = self.get_tipo_token()
        if tipo_token == 'PR':
            palabra = self.get_palabra_reservada()
            if palabra in ['int', 'bool', 'String']:
                self.parse += '28 '

                # Semantico
                return self.f2()
                # Semantico
        else:
            self.parse += '29 '

            # Semantico
            return []
            # Semantico

    def f2(self):
        print('F2 -> D1 id F3' if self.flag else '')
        self.parse += '30 '

        # Semantico
        retorno_d1 = self.d1()
        self.check_token('ID')

        lexema = self.get_lexema()
        tipos = [[retorno_d1, sizes[retorno_d1], lexema]]
        tipos += self.f3()
        return tipos
        # Semantico

    def f3(self):
        print('F3 -> , F2 | λ' if self.flag else '')

        tipo_token = self.get_tipo_token()
        if tipo_token == 'op_coma':
            self.parse += '31 '
            self.check_token('op_coma')

            # Semantico
            return self.f2()
            # Semantico
        else:
            self.parse += '32 '

            # Semantico
            return []
            # Semantico

    def s1(self):
        print('S1 -> S2 | A' if self.flag else '')

        tipo_tokens = self.get_tipo_token()
        if tipo_tokens == 'PR':
            palabra = self.get_palabra_reservada()
            if palabra in ['print', 'prompt', 'return']:
                self.parse += '33 '

                # Semantico
                return self.s2()
                # Semantico
        else:
            self.parse += '34 '
            self.a()

            # Semantico
            return
            # Semantico

    def s2(self):
        print('S2 -> print ( E ) | prompt ( id ) | return E1' if self.flag else '')

        tipo_tokens = self.get_tipo_token()
        if tipo_tokens == 'PR':
            palabra = self.get_palabra_reservada()
            if palabra == 'print':
                self.parse += '35 '
                self.check_token('PR', 'print')
                self.check_token('op_parenab')
                self.e()
                self.check_token('op_parencer')

                # Semantico
                return
                # Semantico
            elif palabra == 'prompt':
                self.parse += '36 '
                self.check_token('PR', 'prompt')
                self.check_token('op_parenab')
                self.check_token('ID')

                # Semantico
                lexema = self.get_lexema()
                tipo_lexema = self.tabla_simbolos.tipo_lexema(lexema)
                if not self.tabla_simbolos.is_defined(lexema) or tipo_lexema not in ['entero', 'cadena']:
                    self.error_semantico('La operación debe realizarse sobre identificadores enteros o cadenas')
                # Semantico

                self.check_token('op_parencer')

                # Semantico
                return
                # Semantico
            elif palabra == 'return':
                self.parse += '37 '
                self.check_token('PR', 'return')

                # Semantico
                return self.e1()
                # Semantico

    def e(self):
        print('E -> G E2' if self.flag else '')
        self.parse += '38 '

        # Semantico
        retorno_g = self.g()
        retorno_e2 = self.e2()

        if retorno_e2 is None:
            return retorno_g
        else:
            if retorno_g != 'logico':
                self.error_semantico("Se esperaba un valor de tipo lógico")
            return 'logico'
        # Semantico

    def e1(self):
        print('E1 -> E | λ' if self.flag else '')

        tipo_token = self.get_tipo_token()
        if tipo_token in ['op_parenab', 'entero', 'cadena'] or tipo_token == 'ID':
            self.parse += '39 '

            # Semantico
            return self.e()
            # Semantico
        elif tipo_token == 'PR':
            palabra = self.get_palabra_reservada()
            if palabra in ['True', 'False']:
                self.parse += '39 '

                # Semantico
                return self.e()
                # Semantico
        else:
            self.parse += '40 '

            # Semantico
            return 'vacio'
            # Semantico

    def e2(self):
        print('E2 -> && E | λ' if self.flag else '')

        tipo_token = self.get_tipo_token()
        if tipo_token == 'op_and':
            self.parse += '41 '
            self.check_token('op_and')

            # Semantico
            retorno_e = self.e()
            if retorno_e != 'logico':
                self.error_semantico("Se esperaba un valor de tipo lógico")
            return 'logico'
            # Semantico
        else:
            self.parse += '42 '

            # Semantico
            return
            # Semantico

    def g(self):
        print('G -> H G1' if self.flag else '')
        self.parse += '43 '

        # Semantico
        retorno_h = self.h()
        retorno_g1 = self.g1()

        if retorno_g1 is None:
            return retorno_h
        else:
            if retorno_h != 'entero':
                self.error_semantico("Se esperaba un valor de tipo entero")
            return 'logico'
        # Semantico

    def g1(self):
        print('G1 -> == G | != G | λ' if self.flag else '')

        tipo_token = self.get_tipo_token()
        if tipo_token == 'op_igual':
            self.parse += '44 '
            self.check_token('op_igual')

            # Semantico
            retorno_g = self.g()
            if retorno_g != 'entero':
                self.error_semantico("Se esperaba un valor de tipo entero")
            return 'logico'
            # Semantico
        elif tipo_token == 'op_noigual':
            self.parse += '45 '
            self.check_token('op_noigual')

            # Semantico
            retorno_g = self.g()
            if retorno_g != 'entero':
                self.error_semantico("Se esperaba un valor de tipo entero")
            return 'logico'
            # Semantico
        else:
            self.parse += '46 '

            # Semantico
            return
            # Semantico

    def h(self):
        print('H -> I H1' if self.flag else '')
        self.parse += '47 '

        # Semantico
        retorno_i = self.i()
        retorno_h1 = self.h1()

        if retorno_h1 is None:
            return retorno_i
        else:
            if retorno_i != 'entero':
                self.error_semantico("Se esperaba un valor de tipo entero")
            return 'entero'
        # Semantico

    def h1(self):
        print('H1 -> + H | - H | λ' if self.flag else '')

        tipo_token = self.get_tipo_token()
        if tipo_token == 'op_suma':
            self.parse += '48 '
            self.check_token('op_suma')

            # Semantico
            retorno_h = self.h()
            if retorno_h != 'entero':
                self.error_semantico("Se esperaba un valor de tipo entero")
            return 'entero'
            # Semantico
        elif tipo_token == 'op_resta':
            self.parse += '49 '
            self.check_token('op_resta')

            # Semantico
            retorno_h = self.h()
            if retorno_h != 'entero':
                self.error_semantico("Se esperaba un valor de tipo entero")
            return 'entero'
            # Semantico
        else:
            self.parse += '50 '

            # Semantico
            return
            # Semantico

    def i(self):
        print('I -> id J | ( E ) | entero | cadena | True | False' if self.flag else '')

        tipo_token = self.get_tipo_token()
        if tipo_token == 'ID':
            self.parse += '51 '
            self.check_token('ID')

            # Semantico
            lexema = self.get_lexema()
            if not self.tabla_simbolos.is_defined(lexema):
                self.error_semantico("Identificador no definido")

            tipo_lexema = self.get_tipo_id(lexema)
            retorno_j = self.j()

            if retorno_j == 'entero':
                if tipo_lexema != 'entero':
                    self.error_semantico("Se esperaba un tipo de dato entero para autoincrementar")
                return 'entero'
            elif retorno_j == 'funcion':
                if tipo_lexema != 'funcion':
                    self.error_semantico("Se esperaba identificador de tipo función")
                return self.tabla_simbolos.tipo_retorno(lexema)
            else:
                return tipo_lexema
            # Semantico
        elif tipo_token == 'op_parenab':
            self.parse += '52 '
            self.check_token('op_parenab')

            # Semantico
            retorno_e = self.e()
            # Semantico

            self.check_token('op_parencer')

            # Semantico
            return retorno_e
            # Semantico
        elif tipo_token == 'entero':
            self.parse += '53 '
            self.check_token('entero')

            # Semantico
            return 'entero'
            # Semantico
        elif tipo_token == 'cadena':
            self.parse += '54 '
            self.check_token('cadena')

            # Semantico
            return 'cadena'
            # Semantico
        elif tipo_token == 'PR':
            palabra = self.get_palabra_reservada()
            if palabra == 'True':
                self.parse += '55 '
                self.check_token('PR', 'True')

                # Semantico
                return 'logico'
                # Semantico
            elif palabra == 'False':
                self.parse += '56 '
                self.check_token('PR', 'False')

                # Semantico
                return 'logico'
                # Semantico

    def j(self):
        print('J -> ++ | ( Z ) | λ' if self.flag else '')

        tipo_token = self.get_tipo_token()
        if tipo_token == 'op_posinc':
            self.parse += '57 '
            self.check_token('op_posinc')

            # Semantico
            return 'entero'
            # Semantico
        elif tipo_token == 'op_parenab':
            self.parse += '58 '
            self.check_token('op_parenab')
            self.z()
            self.check_token('op_parencer')

            # Semantico
            return 'funcion'
            # Semantico
        else:
            self.parse += '59 '

            # Semantico
            return
            # Semantico

    def z(self):
        print('Z -> id Z1 | λ' if self.flag else '')

        tipo_token = self.get_tipo_token()
        if tipo_token == 'ID':
            self.parse += '60 '
            self.check_token('ID')

            # Semantico
            lexema = self.get_lexema()
            if not self.tabla_simbolos.is_defined(lexema):
                self.error_semantico("Identificador no definido")
            # Semantico

            self.z1()
        else:
            self.parse += '61 '

    def z1(self):
        print('Z1 -> , id Z1 | λ' if self.flag else '')

        tipo_token = self.get_tipo_token()
        if tipo_token == 'op_coma':
            self.parse += '62 '
            self.check_token('op_coma')
            self.check_token('ID')

            # Semantico
            lexema = self.get_lexema()
            if not self.tabla_simbolos.is_defined(lexema):
                self.error_semantico("Identificador no definido")
            # Semantico

            self.z1()
        else:
            self.parse += '63 '

    def analize(self):
        """Ejecuta el programa e inserta los resultados en los fichero correspondientes."""
        self.s0()  # Inicia la ejecucion.
        self.fichero_parse.write(self.parse)
        self.fichero_tablas.write(str(self.tabla_simbolos))

    def get_newtokens(self):
        """Obtiene los tokens correspodientes a la siguiente linea de codigo, hasta que se acaba el fichero."""
        new_line = self.fichero_codigo.readline()
        if len(new_line) != 0:
            new_tokens = self.analizador.tokenizeLine(new_line)
            if len(new_tokens) != 0:
                print(new_tokens if self.flag else '')
                self.tokens += new_tokens
            else:
                self.get_newtokens()

    def get_palabra_reservada(self):
        """
        Obtiene la palabra reservada correspodiente al token actualmente apuntado.
        :return: Palabra reservada | None
        """
        return self.analizador.get_palabra_reservada(self.tokens[self.puntero_tokens].valor - 1)

    def get_tipo_token(self):
        """Devuelve el tipo del token apuntado actualmente."""
        tipo = None
        if self.puntero_tokens < len(self.tokens):
            tipo = self.tokens[self.puntero_tokens].tipo
        return tipo

    def get_tipo_id(self, lexema):
        """Devuelve el tipo del id parametro."""
        return self.tabla_simbolos.tipo_lexema(lexema)

    def retorno_funcion(self):
        """Devuelve el tipo del token apuntado actualmente."""
        return self.tokens[self.puntero_tokens].tipo

    def check_token(self, tipo, possible_value=None):
        """
        Comprueba que el token apuntado actualmente es del tipo indicado.
        Si lo es, avanza el puntero, si no lanza error sintactico.
        :param tipo: Tipo esperado para el token.
        :param possible_value: Posible valor que puede esperar en caso de ser una palabra reservada.
        """
        if self.tokens[self.puntero_tokens].tipo == tipo:
            if possible_value is None or self.get_palabra_reservada() == possible_value:
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
        return self.analizador.get_lexema(self.tokens[self.puntero_tokens - 1].valor - 1)

    def error_sintactico(self):
        """Inserta el error en el fichero correspondiente y paramos la ejecucion del programa."""
        error = 'Error Sintáctico (Linea %d): Token %s erroneo' % (self.analizador.lineaActual() - 1,
                                                                   str(self.tokens[self.puntero_tokens]))
        self.fichero_error.write(error)
        print(error if self.flag else '')
        exit()

    def error_semantico(self, mensaje='<Mensaje no definido>'):
        """Inserta el error en el fichero correspondiente y paramos la ejecucion del programa."""
        error = 'Error Semántico (Linea %d): ' % (self.analizador.lineaActual() - 1)
        error += mensaje
        self.fichero_error.write(error + '\n')
        print(error if self.flag else '')
        exit()

# -*- coding: utf-8 -*-
import os
import sys
import yaml

#Cargamos el fichero de configuracion
PATH = os.path.dirname(os.path.abspath(__file__))
with open(PATH + '/config.yml', 'r') as f:
    config = yaml.load(f)

if len(sys.argv) != 2:
    print "Error, solo pasar el archivo"
    exit()

# En primer lugar debemos de abrir el fichero que vamos a leer.
# Usa 'r' para tener acceso de lectura.
FILE = open(sys.argv[1], 'r')
FICHERO_ERROR = open("fichero_error.txt", "w")

# Volacamos el contenido del fichero en 'FICHERO', vara tratarlo como una cadena.
FICHERO = FILE.read()
FILE.close()

#Variables Lexico
#--------------------------------------
TOKENS = []
LISTA_TOKENS = []
NTOKENS = 0
TSaux = [] # TSaux[POS] = LEX --> [ POS | LEX ]

#Variables Sintactico
#--------------------------------------
SAL_ACCIONES = 0 #Acciones
SAL_TERMINALES = 1 #Terminales leidos
Tab = 1
contCr = 0

#Variables Semantico y TS
#--------------------------------------
DicTS = {} # DicTS[ident] = [TS, Desp, ptrTS_padre]
#TS = [ POS | LEXEMA | TIPO | DESPLAZAMIENTO | TAMANO_PARAMETROS | TIPO_PARAMETROS | TIPO_RETURN | PTRTS_ HIJO ]
ptrTS_actual = "null"    # ptrTS_actual     => identificador (ident) TS actual en DicTS
N_IDS = 0            # TSaux[N_IDS] =>  id.ent por orden de aparicion
PARSE_ORDEN = ""

#Funciones TS
#--------------------------------------
# buscarTS             => busca si existe TS en DicTS
# buscarId             => busca si exixte el id en la TS actual, en caso contrario devuelve null
# buscarTipoId         => busca si existe el id en la TS actual y devuelve su tipo, si no existe devuelve null
# buscarTipoFuncion => busca si existe el id en la TS actual y es de tipo "function" y devuelve el tipo de parametros que se le pasa, si no existe, o no es funcion, devuelve null
# insertarTS         => inserta un id en la TS actual
# insertarFunTs     => inserta los parametros de una funcion dado un ptrTS valido
# crearTS             => crea una TS nueva


# buscarTS             => busca si existe TS en DicTS, si no devuelve null
def buscarTS(ident):
    global DicTS
    try:
        return DicTS[str(ident)]
    except:
        return "null"
# buscarId             => busca si exixte el id en la TS actual, en caso contrario devuelve null
def buscarId(ident, ptrTS_actual):
    global DicTS
    ptrTS_busqueda = ptrTS_actual
    if str(ident) in [ DicTS[str(ptrTS_busqueda)][0][n][1] for n in range(len(DicTS[str(ptrTS_busqueda)][0])) ]:
        return  str(ident)
    elif DicTS[str(ptrTS_busqueda)][2] != "null":
        return buscarId(ident, DicTS[str(ptrTS_busqueda)][2])
    else: # sino miramos en la TS_padre
        return "null"
# buscarTipoId         => busca si existe el id en la TS actual y devuelve su tipo, si no existe devuelve null
def buscarTipoId(ident, ptrTS_actual):
    global DicTS
    ptrTS_busqueda = ptrTS_actual
    if str(ident) in [ DicTS[str(ptrTS_busqueda)][0][n][1] for n in range(len(DicTS[str(ptrTS_busqueda)][0])) ]:
        return  [ DicTS[str(ptrTS_busqueda)][0][n][2] for n in range(len(DicTS[str(ptrTS_busqueda)][0])) ][ [ DicTS[str(ptrTS_busqueda)][0][n][1] for n in range(len(DicTS[str(ptrTS_busqueda)][0])) ].index(str(ident))]
    elif DicTS[str(ptrTS_busqueda)][2] != "null":
        return buscarTipoId(ident, DicTS[str(ptrTS_busqueda)][2])
    else:
        return "null"

# buscarTipoFuncion => busca si existe el id en la TS actual y es de tipo "function" y devuelve la salida de la funcion, si no existe, o no es funcion, devuelve null
def buscarTipoFuncion(ident, ptrTS_actual):
    global DicTS
    ptrTS_busqueda = ptrTS_actual
    if str(ident) in [ DicTS[str(ptrTS_busqueda)][0][n][1] for n in range(len(DicTS[str(ptrTS_busqueda)][0])) ] and [ DicTS[str(ptrTS_busqueda)][0][n][2] for n in range(len(DicTS[str(ptrTS_busqueda)][0])) ][ [ DicTS[str(ptrTS_busqueda)][0][n][1] for n in range(len(DicTS[str(ptrTS_busqueda)][0])) ].index(str(ident))] == "function":
        return  [ DicTS[str(ptrTS_busqueda)][0][n][6] for n in range(len(DicTS[str(ptrTS_busqueda)][0])) ][ [ DicTS[str(ptrTS_busqueda)][0][n][1] for n in range(len(DicTS[str(ptrTS_busqueda)][0])) ].index(str(ident))]
    elif DicTS[str(ptrTS_busqueda)][2] != "null" :
        return buscarTipoFuncion(ident, DicTS[str(ptrTS_busqueda)][2])
    else :
        return "null"

# buscarTipoParametrosFuncion => busca si existe el id en la TS actual y es de tipo "function" y devuelve el tipo de parametros que se le pasa, si no existe, o no es funcion, devuelve null
def buscarTipoParametrosFuncion(ident, ptrTS_actual) :
    global DicTS
    ptrTS_busqueda = ptrTS_actual
    if str(ident) in [ DicTS[str(ptrTS_busqueda)][0][n][1] for n in range(len(DicTS[str(ptrTS_busqueda)][0])) ] and [ DicTS[str(ptrTS_busqueda)][0][n][2] for n in range(len(DicTS[str(ptrTS_busqueda)][0])) ][ [ DicTS[str(ptrTS_busqueda)][0][n][1] for n in range(len(DicTS[str(ptrTS_busqueda)][0])) ].index(str(ident))] == "function" :
        return  [ DicTS[str(ptrTS_busqueda)][0][n][5] for n in range(len(DicTS[str(ptrTS_busqueda)][0])) ][ [ DicTS[str(ptrTS_busqueda)][0][n][1] for n in range(len(DicTS[str(ptrTS_busqueda)][0])) ].index(str(ident))]
    elif DicTS[str(ptrTS_busqueda)][2] != "null" :
        return buscarTipoParametrosFuncion(ident, DicTS[str(ptrTS_busqueda)][2])
    else :
        return "null"

# insertarTS         => inserta un id en la TS actual
def insertarTS(LEXEMA , TIPO , DESPLAZAMIENTO, ptrTST_actual) :
    global DicTS
    if str(LEXEMA) not in [ DicTS[str(ptrTS_actual)][0][n][1] for n in range(len(DicTS[str(ptrTS_actual)][0])) ] :
        DicTS[ptrTS_actual][0].append([len(DicTS[ptrTS_actual][0]), str(LEXEMA) , str(TIPO) , str(DESPLAZAMIENTO) , 'null' , 'null' , 'null' , 'null' , 'null' ])
        return "insertado"
    else :
        return "null"

# insertarFunTs     => inserta los parametros de una funcion dado un ptrTS valido
def    insertarFunTS(ptrTS_anterior, ident, tamano_parametros , tipo_parametros, tipo_return, ptrTS_hijo) :
    global DicTS
    if str(ident) in [ DicTS[str(ptrTS_anterior)][0][n][1] for n in range(len(DicTS[str(ptrTS_anterior)][0])) ] and [ DicTS[str(ptrTS_anterior)][0][n][2] for n in range(len(DicTS[str(ptrTS_anterior)][0])) ][ [ DicTS[str(ptrTS_anterior)][0][n][1] for n in range(len(DicTS[str(ptrTS_anterior)][0])) ].index(str(ident))] == "function" :
        DicTS[str(ptrTS_anterior)][0][[ DicTS[str(ptrTS_anterior)][0][n][1] for n in range(len(DicTS[str(ptrTS_anterior)][0])) ].index(str(ident))][4:] = [str(tamano_parametros) , str(tipo_parametros), str(tipo_return), str(ptrTS_hijo)]
        return "insertado"
    else :
        return "null"

######################        INICIO ANALIZADOR LEXICO        ######################
def analizadorLexico():
    elemt  = ""
    coment = ""
    salida = 1
    entra = 0

    for caracter in FICHERO :
        if caracter != " " and caracter != "\t" and caracter != "\n" and coment == "":
            #concatenamos el caracter a elemt
            elemt += caracter
            if salida == 1 : print elemt

        #Comporbamos si estamos en un comentario o cadena
        if coment != "":
            elemt += caracter

            if elemt[-2:] == "*/" or elemt[-1:] == "\n":
                if coment == "\n" and elemt[-1:] == "\n":
                    TOKENS.append("< %s , %s >"%("cr", "-"))
                    LISTA_TOKENS.append("cr")
                    if salida == 1 : print "< %s , %s >\n"%("cr","-")

                if salida == 1 : print ">>> FIN Comentario\n"
                coment = ""
                elemt = ""
                continue

            elif elemt[-1:] == "\"" and coment == "\"":
                TOKENS.append("< %s , %s >"%("cadena", str(elemt)))
                LISTA_TOKENS.append("cadena")
                if salida == 1 : print "< %s , %s >\n"%("cadena", str(elemt))
                coment = ""
                elemt = ""
                continue

            else:
                continue

        #En caso de que sea Token
        else:
            #Inicio de comentario acotado
            if len(elemt) > 1 and elemt[-2:] == "/*":
                if entra == 1 : print "entra1"
                if len (elemt) > 2:
                    if elemt[:-2] in config :
                        TOKENS.append("< %s , %s >"%(str(config[elemt[:-2]]), str(elemt[:-2])))
                        LISTA_TOKENS.append(str(elemt[:-2]))
                        if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-2]]), str(elemt[:-2]))
                    else:
                        try:
                            int(elemt[-2:])
                            if int(elemt[-2:]) > 32767:
                                TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- numero superior a 32767"))
                                LISTA_TOKENS.append("ERROR")
                                print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1))
                                FICHERO_ERROR.write("ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1)))
                                break
                            else:
                                TOKENS.append("< %s , %s >"%("entero",str(elemt[:-2])))
                                LISTA_TOKENS.append("entero")
                                if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-2]))
                        except:
                            if str(elemt[:-2]).isalnum() and str(elemt[:-2][:1]).isalpha() :
                                TOKENS.append("< %s , %s >"%("id",str(elemt[:-2]))) # tendria que ser  pos en TS
                                LISTA_TOKENS.append("id")
                                TSaux.append(str(elemt[:-2]))
                                if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-2]))
                            else:
                                TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- identificador mal formado"))
                                LISTA_TOKENS.append("ERROR")
                                print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1))
                                FICHERO_ERROR.write("ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1)))
                                break

                coment= "*/"
                elemt = ""
                if salida == 1 : print ">>> NUEVO Comentario /*\n"

            #Elemento propio del lenguaje
            elif elemt in config :
                if elemt == "=":
                    continue
                if entra == 1 : print "entra2"
                TOKENS.append("< %s , %s >"%(str(config[elemt]), str(elemt)))
                LISTA_TOKENS.append(str(elemt))
                if salida == 1 : print "< %s , %s >\n"%(str(config[elemt]), str(elemt))
                elemt = ""

            #Si acaba en salto de linea con elementos
            elif caracter == "\n" and elemt != "":
                if entra == 1 : print "entra3"
                if elemt in config :
                    TOKENS.append("< %s , %s >"%(str(config[elemt[:-1]]), str(elemt[:-1])))
                    TOKENS.append("< %s , %s >"%("cr", "-"))
                    LISTA_TOKENS.append(str(elemt[:-1]))
                    LISTA_TOKENS.append("cr")
                    if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
                    if salida == 1 : print "< %s , %s >\n"%("cr","-")
                else:
                    try:
                        int(elemt)
                        if int(elemt) > 32767:
                            TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- numero superior a 32767"))
                            LISTA_TOKENS.append("ERROR")
                            print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1))
                            FICHERO_ERROR.write("ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1)))
                            break
                        else:
                            TOKENS.append("< %s , %s >"%("entero",str(elemt)))
                            LISTA_TOKENS.append("entero")
                            if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt))
                    except:
                        if str(elemt[:-(len(elemt)-1)]) == "_":
                            TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- identificador mal formado"))
                            LISTA_TOKENS.append("ERROR")
                            print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1))
                            FICHERO_ERROR.write("ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1)))
                            break
                        flag_lex_ok = 0
                        for char in elemt:
                            if not str(char).isalnum() and not str(char) == "_" :
                                TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- identificador mal formado"))
                                LISTA_TOKENS.append("ERROR")
                                print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1))
                                FICHERO_ERROR.write("ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1)))
                                flag_lex_ok = 1
                                break
                        if flag_lex_ok == 1: break
                        TOKENS.append("< %s , %s >"%("id",str(elemt))) # deberia ser  pos en  TS
                        LISTA_TOKENS.append("id")
                        TSaux.append(str(elemt))
                        if salida == 1 : print "< %s , %s >\n"%("id",str(elemt))
                    TOKENS.append("< %s , %s >"%("cr", "-"))
                    LISTA_TOKENS.append("cr")
                    if salida == 1 : print "< %s , %s >\n"%("cr","-")
                elemt = ""

            #Si acaba en salto de linea sin elementos
            elif caracter == "\n" and elemt == "":
                if entra == 1 : print "entra4"
                TOKENS.append("< %s , %s >"%("cr", "-"))
                LISTA_TOKENS.append("cr")
                if salida == 1 : print "< %s , %s >\n"%("cr","-")

            #Comentariom de linea
            elif len(elemt) > 1 and elemt[-2:] == "//":
                if entra == 1 : print "entra5"
                if len (elemt) > 2:
                    if elemt[:-2] in config :
                        TOKENS.append("< %s , %s >"%(str(config[elemt[:-2]]), str(elemt[:-2])))
                        LISTA_TOKENS.append(elemt[:-2])
                        if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-2]]), str(elemt[:-2]))
                    else:
                        try:
                            int(elemt[:-2])
                            if int(elemt[:-2]) > 32767:
                                TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- numero superior a 32767"))
                                LISTA_TOKENS.append("ERROR")
                                print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1))
                                FICHERO_ERROR.write("ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1)))
                                break
                            else:
                                TOKENS.append("< %s , %s >"%("entero",str(elemt[:-2])))
                                LISTA_TOKENS.append("entero")
                                if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-2]))
                        except:
                            if str(elemt[:-2]).isalnum() and str(elemt[:-2][:1]).isalpha() :
                                TOKENS.append("< %s , %s >"%("id",str(elemt[:-2]))) # deberia ser  pos en  TS
                                LISTA_TOKENS.append("id")
                                TSaux.append(str(elemt[:-2]))
                                if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-2]))
                            else:
                                TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- identificador mal formado"))
                                LISTA_TOKENS.append("ERROR")
                                print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1))
                                FICHERO_ERROR.write("ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1)))
                                break

                    elemt = ""
                    if salida == 1 : print ">>> NUEVO Comentario //\n"

                coment= "\n"
                elemt = ""

            #Acaba en fin de parentesis
            elif elemt[-1:] == ")":
                if entra == 1 : print "entra6"
                if len (elemt) > 1:
                    if elemt[:-1] in config :
                        TOKENS.append("< %s , %s >"%(str(config[elemt[:-1]]), str(elemt[:-1])))
                        TOKENS.append("< %s , %s >"%(str(config[")"]), ")"))
                        LISTA_TOKENS.append(str(elemt[:-1]))
                        LISTA_TOKENS.append(")")
                        if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
                        if salida == 1 : print "< %s , %s >\n"%(str(config[")"]),")")
                    else:
                        try:
                            int(elemt[:-1])
                            if int(elemt[:-1]) > 32767:
                                TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- numero superior a 32767"))
                                LISTA_TOKENS.append("ERROR")
                                print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1))
                                FICHERO_ERROR.write("ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1)))
                                break
                            else:
                                TOKENS.append("< %s , %s >"%("entero",str(elemt[:-1])))
                                LISTA_TOKENS.append("entero")
                                if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
                        except:
                            if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
                                TOKENS.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
                                LISTA_TOKENS.append("id")
                                TSaux.append(str(elemt[:-1]))
                                if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
                            else:
                                TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- identificador mal formado"))
                                LISTA_TOKENS.append("ERROR")
                                print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1))
                                FICHERO_ERROR.write("ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1)))
                                break

                        TOKENS.append("< %s , %s >"%(str(config[")"]), ")"))
                        LISTA_TOKENS.append(")")
                        if salida == 1 : print "< %s , %s >\n"%(str(config[")"]),")")

                    elemt = ""
                elemt = ""

            #Empieza en igual
            elif elemt[:1] == "=" and len (elemt) > 1:
                TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                LISTA_TOKENS.append(str(elemt[:1]))
                if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:1]]), str(elemt[:1]))
                elemt = elemt[1:]
                if entra == 1 : print "entra7"
                if elemt[:1] == "\"":
                    coment= "\""
                    continue

            #Acaba en igual
            elif elemt[-1:] == "=" and len (elemt) > 1:
                if entra == 1 : print "entra8"
                if elemt[:-1] in config :
                    TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                    LISTA_TOKENS.append(str(elemt[:1]))
                    if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
                else:
                    try:
                        int(elemt[:-1])
                        if int(elemt[:-1]) > 32767:
                            TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- numero superior a 32767"))
                            LISTA_TOKENS.append("ERROR")
                            print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1))
                            FICHERO_ERROR.write("ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1)))
                            break
                        else:
                            TOKENS.append("< %s , %s >"%("entero",str(elemt[:-1])))
                            LISTA_TOKENS.append("entero")
                            if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
                    except:
                            if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
                                TOKENS.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
                                LISTA_TOKENS.append("id")
                                TSaux.append(str(elemt[:-1]))
                                if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
                            else:
                                TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- identificador mal formado"))
                                LISTA_TOKENS.append("ERROR")
                                print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1))
                                FICHERO_ERROR.write("ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1)))
                                break

                elemt = elemt[-1:]
                continue

            #Empieza en mas
            elif elemt[:1] == "+" and len (elemt) > 1:
                TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                LISTA_TOKENS.append(str(elemt[:1]))
                if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:1]]), str(elemt[:1]))
                elemt = elemt[1:]
                if entra == 1 : print "entra7"
                if elemt[:1] == "\"":
                    coment= "\""
                    continue

            #Acaba en mas
            elif elemt[-1:] == "+" and len (elemt) > 1:
                if entra == 1 : print "entra8"
                if elemt[:-1] in config :
                    TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                    LISTA_TOKENS.append(str(elemt[:1]))
                    if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
                else:
                    try:
                        int(elemt[:-1])
                        if int(elemt[:-1]) > 32767:
                            TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- numero superior a 32767"))
                            LISTA_TOKENS.append("ERROR")
                            print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1))
                            FICHERO_ERROR.write("ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1)))
                            break
                        else:
                            TOKENS.append("< %s , %s >"%("entero",str(elemt[:-1])))
                            LISTA_TOKENS.append("entero")
                            if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
                    except:
                            if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
                                TOKENS.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
                                LISTA_TOKENS.append("id")
                                TSaux.append(str(elemt[:-1]))
                                if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
                            else:
                                TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- identificador mal formado"))
                                LISTA_TOKENS.append("ERROR")
                                print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1))
                                FICHERO_ERROR.write("ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1)))
                                break

                elemt = elemt[-1:]
                continue

            #Empieza en mayor
            elif elemt[:1] == ">" and len (elemt) > 1:
                TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                LISTA_TOKENS.append(str(elemt[:1]))
                if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:1]]), str(elemt[:1]))
                elemt = elemt[1:]
                if entra == 1 : print "entra7"
                if elemt[:1] == "\"":
                    coment= "\""
                    continue

            #Acaba en mayor
            elif elemt[-1:] == ">" and len (elemt) > 1:
                if entra == 1 : print "entra8"
                if elemt[:-1] in config :
                    TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                    LISTA_TOKENS.append(str(elemt[:1]))
                    if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
                else:
                    try:
                        int(elemt[:-1])
                        if int(elemt[:-1]) > 32767:
                            TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- numero superior a 32767"))
                            LISTA_TOKENS.append("ERROR")
                            print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1))
                            FICHERO_ERROR.write("ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1)))
                            break
                        else:
                            TOKENS.append("< %s , %s >"%("entero",str(elemt[:-1])))
                            LISTA_TOKENS.append("entero")
                            if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
                    except:
                            if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
                                TOKENS.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
                                LISTA_TOKENS.append("id")
                                TSaux.append(str(elemt[:-1]))
                                if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
                            else:
                                TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- identificador mal formado"))
                                LISTA_TOKENS.append("ERROR")
                                print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1))
                                FICHERO_ERROR.write("ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1)))
                                break

                elemt = elemt[-1:]
                continue

            #Empieza en mayor
            elif elemt[:1] == ":" and len (elemt) > 1:
                TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                LISTA_TOKENS.append(str(elemt[:1]))
                if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:1]]), str(elemt[:1]))
                elemt = elemt[1:]
                if entra == 1 : print "entra7"
                if elemt[:1] == "\"":
                    coment= "\""
                    continue

            #Acaba en mayor
            elif elemt[-1:] == ":" and len (elemt) > 1:
                if entra == 1 : print "entra8"
                if elemt[:-1] in config :
                    TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                    LISTA_TOKENS.append(str(elemt[:1]))
                    if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
                else:
                    try:
                        int(elemt[:-1])
                        if int(elemt[:-1]) > 32767:
                            TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- numero superior a 32767"))
                            LISTA_TOKENS.append("ERROR")
                            print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1))
                            FICHERO_ERROR.write("ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1)))
                            break
                        else:
                            TOKENS.append("< %s , %s >"%("entero",str(elemt[:-1])))
                            LISTA_TOKENS.append("entero")
                            if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
                    except:
                            if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
                                TOKENS.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
                                LISTA_TOKENS.append("id")
                                TSaux.append(str(elemt[:-1]))
                                if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
                            else:
                                TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- identificador mal formado"))
                                LISTA_TOKENS.append("ERROR")
                                print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1))
                                FICHERO_ERROR.write("ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1)))
                                break

                elemt = elemt[-1:]
                continue

            #Empieza en mayor
            elif elemt[:1] == ";" and len (elemt) > 1:
                TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                LISTA_TOKENS.append(str(elemt[:1]))
                if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:1]]), str(elemt[:1]))
                elemt = elemt[1:]
                if entra == 1 : print "entra7"
                if elemt[:1] == "\"":
                    coment= "\""
                    continue

            #Acaba en mayor
            elif elemt[-1:] == ";" and len (elemt) > 1:
                if entra == 1 : print "entra8"
                if elemt[:-1] in config :
                    TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                    LISTA_TOKENS.append(str(elemt[:1]))
                    if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
                else:
                    try:
                        int(elemt[:-1])
                        if int(elemt[:-1]) > 32767:
                            TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- numero superior a 32767"))
                            LISTA_TOKENS.append("ERROR")
                            print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1))
                            FICHERO_ERROR.write("ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1)))
                            break
                        else:
                            TOKENS.append("< %s , %s >"%("entero",str(elemt[:-1])))
                            LISTA_TOKENS.append("entero")
                            if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
                    except:
                            if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
                                TOKENS.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
                                LISTA_TOKENS.append("id")
                                TSaux.append(str(elemt[:-1]))
                                if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
                            else:
                                TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- identificador mal formado"))
                                LISTA_TOKENS.append("ERROR")
                                print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1))
                                FICHERO_ERROR.write("ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1)))
                                break

                elemt = elemt[-1:]
                continue

            #Empieza por coma
            elif elemt[:1] == "," and len (elemt) > 1:
                TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                LISTA_TOKENS.append(str(elemt[:1]))
                if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:1]]), str(elemt[:1]))
                elemt = elemt[1:]
                if entra == 1 : print "entra7"
                if elemt[:1] == "\"":
                    coment= "\""
                    continue

            #Acaba en coma
            elif elemt[-1:] == "," and len (elemt) > 1:
                if entra == 1 : print "entra8"
                if elemt[:-1] in config :
                    TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                    LISTA_TOKENS.append(str(elemt[:1]))
                    if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
                else:
                    try:
                        int(elemt[:-1])
                        if int(elemt[:-1]) > 32767:
                            TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- numero superior a 32767"))
                            LISTA_TOKENS.append("ERROR")
                            print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1))
                            FICHERO_ERROR.write("ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1)))
                            break
                        else:
                            TOKENS.append("< %s , %s >"%("entero",str(elemt[:-1])))
                            LISTA_TOKENS.append("entero")
                            if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
                    except:
                            if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
                                TOKENS.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
                                LISTA_TOKENS.append("id")
                                TSaux.append(str(elemt[:-1]))
                                if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
                            else:
                                TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- identificador mal formado"))
                                LISTA_TOKENS.append("ERROR")
                                print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1))
                                FICHERO_ERROR.write("ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1)))
                                break

                elemt = elemt[-1:]
                continue

            #Empieza {
            elif elemt[:1] == "{" and len (elemt) > 1:
                TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                LISTA_TOKENS.append(str(elemt[:1]))
                if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:1]]), str(elemt[:1]))
                elemt = elemt[1:]
                if entra == 1 : print "entra7"
                if elemt[:1] == "\"":
                    coment= "\""
                    continue

            #Acaba  {
            elif elemt[-1:] == "{" and len (elemt) > 1:
                if entra == 1 : print "entra8"
                if elemt[:-1] in config :
                    TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                    LISTA_TOKENS.append(str(elemt[:1]))
                    if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
                else:
                    try:
                        int(elemt[:-1])
                        if int(elemt[:-1]) > 32767:
                            TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- numero superior a 32767"))
                            LISTA_TOKENS.append("ERROR")
                            print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1))
                            FICHERO_ERROR.write("ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1)))
                            break
                        else:
                            TOKENS.append("< %s , %s >"%("entero",str(elemt[:-1])))
                            LISTA_TOKENS.append("entero")
                            if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
                    except:
                            if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
                                TOKENS.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
                                LISTA_TOKENS.append("id")
                                TSaux.append(str(elemt[:-1]))
                                if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
                            else:
                                TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- identificador mal formado"))
                                LISTA_TOKENS.append("ERROR")
                                print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1))
                                FICHERO_ERROR.write("ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1)))
                                break

                elemt = elemt[-1:]
                continue

            #Empieza }
            elif elemt[:1] == "}" and len (elemt) > 1:
                TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                LISTA_TOKENS.append(str(elemt[:1]))
                if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:1]]), str(elemt[:1]))
                elemt = elemt[1:]
                if entra == 1 : print "entra7"
                if elemt[:1] == "\"":
                    coment= "\""
                    continue

            #Acaba }
            elif elemt[-1:] == "}" and len (elemt) > 1:
                if entra == 1 : print "entra8"
                if elemt[:-1] in config :
                    TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                    LISTA_TOKENS.append(str(elemt[:1]))
                    if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
                else:
                    try:
                        int(elemt[:-1])
                        if int(elemt[:-1]) > 32767:
                            TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- numero superior a 32767"))
                            LISTA_TOKENS.append("ERROR")
                            print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1))
                            FICHERO_ERROR.write("ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1)))
                            break
                        else:
                            TOKENS.append("< %s , %s >"%("entero",str(elemt[:-1])))
                            LISTA_TOKENS.append("entero")
                            if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
                    except:
                            if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
                                TOKENS.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
                                LISTA_TOKENS.append("id")
                                TSaux.append(str(elemt[:-1]))
                                if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
                            else:
                                TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- identificador mal formado"))
                                LISTA_TOKENS.append("ERROR")
                                print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1))
                                FICHERO_ERROR.write("ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1)))
                                break

                elemt = elemt[-1:]
                continue

            #Empieza (
            elif elemt[:1] == "(" and len (elemt) > 1:
                TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                LISTA_TOKENS.append(str(elemt[:1]))
                if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:1]]), str(elemt[:1]))
                elemt = elemt[1:]
                if entra == 1 : print "entra7"
                if elemt[:1] == "\"":
                    coment= "\""
                    continue

            #Acaba (
            elif elemt[-1:] == "(" and len (elemt) > 1:
                if entra == 1 : print "entra8"
                if elemt[:-1] in config :
                    TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                    LISTA_TOKENS.append(str(elemt[:1]))
                    if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
                else:
                    try:
                        int(elemt[:-1])
                        if int(elemt[:-1]) > 32767:
                            TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- numero superior a 32767"))
                            LISTA_TOKENS.append("ERROR")
                            print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1))
                            FICHERO_ERROR.write("ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1)))
                            break
                        else:
                            TOKENS.append("< %s , %s >"%("entero",str(elemt[:-1])))
                            LISTA_TOKENS.append("entero")
                            if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
                    except:
                            if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
                                TOKENS.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
                                LISTA_TOKENS.append("id")
                                TSaux.append(str(elemt[:-1]))
                                if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
                            else:
                                TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- identificador mal formado"))
                                LISTA_TOKENS.append("ERROR")
                                print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1))
                                FICHERO_ERROR.write("ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1)))
                                break

                elemt = elemt[-1:]
                continue

            #Empieza )
            elif elemt[:1] == ")" and len (elemt) > 1:
                TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                LISTA_TOKENS.append(str(elemt[:1]))
                if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:1]]), str(elemt[:1]))
                elemt = elemt[1:]
                if entra == 1 : print "entra7"
                if elemt[:1] == "\"":
                    coment= "\""
                    continue

            #Acaba )
            elif elemt[-1:] == ")" and len (elemt) > 1:
                if entra == 1 : print "entra8"
                if elemt[:-1] in config :
                    TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                    LISTA_TOKENS.append(str(elemt[:1]))
                    if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
                else:
                    try:
                        int(elemt[:-1])
                        if int(elemt[:-1]) > 32767:
                            TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- numero superior a 32767"))
                            LISTA_TOKENS.append("ERROR")
                            print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1))
                            FICHERO_ERROR.write("ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1)))
                            break
                        else:
                            TOKENS.append("< %s , %s >"%("entero",str(elemt[:-1])))
                            LISTA_TOKENS.append("entero")
                            if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
                    except:
                            if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
                                TOKENS.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
                                LISTA_TOKENS.append("id")
                                TSaux.append(str(elemt[:-1]))
                                if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
                            else:
                                TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- identificador mal formado"))
                                LISTA_TOKENS.append("ERROR")
                                print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1))
                                FICHERO_ERROR.write("ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1)))
                                break

                elemt = elemt[-1:]
                continue

            #Empieza por ,
            elif elemt[:1] == "," and len (elemt) > 1:
                TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                LISTA_TOKENS.append(str(elemt[:1]))
                if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:1]]), str(elemt[:1]))
                elemt = elemt[1:]
                if entra == 1 : print "entra7"
                if elemt[:1] == "\"":
                    coment= "\""
                    continue

            #Acaba en igual
            elif elemt[-1:] == "," and len (elemt) > 1:
                if entra == 1 : print "entra8"
                if elemt[:-1] in config :
                    TOKENS.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
                    LISTA_TOKENS.append(str(elemt[:1]))
                    if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
                else:
                    try:
                        int(elemt[:-1])
                        if int(elemt[:-1]) > 32767:
                            TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- numero superior a 32767"))
                            LISTA_TOKENS.append("ERROR")
                            print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1))
                            FICHERO_ERROR.write("ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1)))
                            break
                        else:
                            TOKENS.append("< %s , %s >"%("entero",str(elemt[:-1])))
                            LISTA_TOKENS.append("entero")
                            if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
                    except:
                            if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
                                TOKENS.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
                                LISTA_TOKENS.append("id")
                                TSaux.append(str(elemt[:-1]))
                                if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
                            else:
                                TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- identificador mal formado"))
                                LISTA_TOKENS.append("ERROR")
                                print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1))
                                FICHERO_ERROR.write("ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1)))
                                break

                elemt = elemt[-1:]
                continue

            #Cadena de caracteres
            elif elemt[-1:] == "\"":
                coment= "\""
                if entra == 1 : print "entra9"
                continue

            #Elemento no propio del lenguaje
            elif caracter == " " and elemt != "":
                if entra == 1 : print "entra10"
                try:
                    int(elemt)
                    if int(elemt) > 32767:
                        TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- numero superior a 32767"))
                        LISTA_TOKENS.append("ERROR")
                        print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1))
                        FICHERO_ERROR.write("ERROR LEXICO, Linea %s- numero superior a 32767"%(str(LISTA_TOKENS.count("cr")+1)))
                        break
                    else:
                        TOKENS.append("< %s , %s >"%("entero",str(elemt)))
                        LISTA_TOKENS.append("entero")
                    if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt))
                except:
                    if elemt in config :
                        TOKENS.append("< %s , %s >"%(str(config[elemt]), str(elemt)))
                        LISTA_TOKENS.append(str(elemt))
                        if salida == 1 : print "< %s , %s >\n"%(str(config[elemt]), str(elemt))
                    else:
                            if str(elemt).isalnum() and str(elemt[:1]).isalpha() :
                                TOKENS.append("< %s , %s >"%("id",str(elemt))) # deberia ser  pos en  TS
                                LISTA_TOKENS.append("id")
                                TSaux.append(str(elemt))
                                if salida == 1 : print "< %s , %s >\n"%("id",str(elemt))
                            else:
                                TOKENS.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(LISTA_TOKENS.count("cr")+1)+"- identificador mal formado"))
                                LISTA_TOKENS.append("ERROR")
                                print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1))
                                FICHERO_ERROR.write("ERROR LEXICO, Linea %s- identificador mal formado"%(str(LISTA_TOKENS.count("cr")+1)))
                                break
                elemt = ""

    contTS = 0
    if LISTA_TOKENS.count("ERROR") == 0 :
        TOKENS.append("< %s , %s >"%( "FinFich", "eof" ))
        LISTA_TOKENS.append("eof")
        if salida == 1 : print "< %s , %s >\n"%("FinFich","eof")

    fichTokens = open('tokens_salida.txt', 'w')
    for token in TOKENS :
        fichTokens.write(str(token)+" \n")
    fichTokens.close()

    if LISTA_TOKENS.count("ERROR") != 0 :
        exit()
######################          FIN ANALIZADOR LEXICO            ######################
######################        INICIO ANALIZADOR SINTACTICO    ######################
def    analizadorSintactico():
    P1()

# P' → P
def P1():
    global SAL_ACCIONES, Tab, DicTS, ptrTS_actual, PARSE_ORDEN
    PARSE_ORDEN+="1 "

    #--Semantico Inicio
    ptrTS_actual = "TS_General"
    DicTS[ptrTS_actual] = [ [], 0, "null"]
    #--Semantico Fin

    #--Sintactico Inicio
    print Tab*"  "+"P’→ P" if SAL_ACCIONES == 0 else ""
    Tab+=1 if SAL_ACCIONES == 0 else 0
    P0()
    Tab-=1 if SAL_ACCIONES == 0 else 0
    #--Sintactico Fin

# P → B Z P | F Z P | Z P | eof
def P0():
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, PARSE_ORDEN

    #--Sintactico Inicio
    if LISTA_TOKENS[NTOKENS] == "eof":
        print Tab*"  "+"P→ eof" if SAL_ACCIONES == 0 else ""
        PARSE_ORDEN+="5 "
        ComprobarToken("eof")

    elif LISTA_TOKENS[NTOKENS] == "function":
        PARSE_ORDEN+="3 "
        print Tab*"  "+"P→ FZP" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        F()
        Z0()
        P0()
        Tab-=1 if SAL_ACCIONES == 0 else 0
    elif LISTA_TOKENS[NTOKENS] == "cr":
        PARSE_ORDEN+="4 "
        print Tab*"  "+"P→ ZP" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        Z0()
        P0()
        Tab-=1 if SAL_ACCIONES == 0 else 0
    else:
        PARSE_ORDEN+="2 "
        print Tab*"  "+"P→ BZP" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        B0()
        Z0()
        P0()
        Tab-=1 if SAL_ACCIONES == 0 else 0
    #--Sintactico Fin

# B → var T id | if (E) S | switch (E) Z {Z W} | S
def B0(): #b=[tipo]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, TSaux, N_IDS, DicTS, ptrTS_actual, PARSE_ORDEN

    #--Sintactico Inicio
    if LISTA_TOKENS[NTOKENS] == "var":
        PARSE_ORDEN+="6 "
        print Tab*"  "+"B → var T id" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        ComprobarToken("var")
        t=T() #t=[tipo,tamano]
        ComprobarToken("id")
        Tab-=1 if SAL_ACCIONES == 0 else 0

        #--Semantico Inicio
        if buscarId(TSaux[N_IDS], ptrTS_actual) != "null" :
            Error_Sem("Identificador ya creado")
        else:
            insertarTS(TSaux[N_IDS], t[0], DicTS[ptrTS_actual][1], ptrTS_actual)
            DicTS[ptrTS_actual][1] += t[1]
            N_IDS+=1
        return ["tipo_ok"]
        #--Semantico Fin

    elif LISTA_TOKENS[NTOKENS] == "if":
        PARSE_ORDEN+="7 "
        print Tab*"  "+"B → if (E) S" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        ComprobarToken("if")
        ComprobarToken("(")
        e=E0() #e=[tipo]
        ComprobarToken(")")

        #--Semantico Inicio
        if e[0] != "logico" :
            Error_Sem("condición \"if\" no logica")
        #--Semantico Fin

        s=S0()
        Tab-=1 if SAL_ACCIONES == 0 else 0

    elif LISTA_TOKENS[NTOKENS] == "switch":
        PARSE_ORDEN+="8 "
        print Tab*"  "+"B → switch (E) Z {Z W}" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        ComprobarToken("switch")
        ComprobarToken("(")
        e=E0() #e=[tipo]
        ComprobarToken(")")

        #--Semantico Inicio
        if e[0] != "entero" :
            Error_Sem("condición \"switch\" no entera")
        #--Semantico Fin

        Z0()
        ComprobarToken("{")
        Z0() #e=[tipo]
        W0()
        ComprobarToken("}")
        Tab-=1 if SAL_ACCIONES == 0 else 0

        #--Semantico Inicio
        return ["tipo_ok"]
        #--Semantico Fin

    else:
        PARSE_ORDEN+="9 "
        print Tab*"  "+"B → S" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        s=S0() #s=[tipo]
        Tab-=1 if SAL_ACCIONES == 0 else 0

        #--Semantico Inicio
        return s
        #--Semantico Fin

# T → int | bool | chars
def T(): #t=[tipo,tamano]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, PARSE_ORDEN

    #--Sintactico Inicio
    if LISTA_TOKENS[NTOKENS] == "int":
        PARSE_ORDEN+="10 "
        print Tab*"  "+"T → int" if SAL_ACCIONES == 0 else ""
        ComprobarToken("int")

        #--Semantico Inicio
        return [ "entero", 2 ]
        #--Semantico Fin

    elif LISTA_TOKENS[NTOKENS] == "bool":
        PARSE_ORDEN+="11 "
        print Tab*"  "+"T → bool" if SAL_ACCIONES == 0 else ""
        ComprobarToken("bool")

        #--Semantico Inicio
        return [ "logico", 1 ]
        #--Semantico Fin

    else:
        PARSE_ORDEN+="12 "
        print Tab*"  "+"T → chars" if SAL_ACCIONES == 0 else ""
        ComprobarToken("chars")

        #--Semantico Inicio
        return [ "cadena", 2 ]
        #--Semantico Fin

    #--Sintactico Fin

# S → id S'| return X | write (E) | prompt (id)
def S0(): #s=[tipo]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, TSaux, N_IDS, ptrTS_actual, PARSE_ORDEN

    #--Sintactico Inicio
    if LISTA_TOKENS[NTOKENS] == "id":
        print Tab*"  "+"S → id S'" if SAL_ACCIONES == 0 else ""
        PARSE_ORDEN+="13 "
        Tab+=1 if SAL_ACCIONES == 0 else 0
        ComprobarToken("id")
        auxID=TSaux[N_IDS]
        N_IDS += 1
        s1=S1() #s=[tipo]
        Tab-=1 if SAL_ACCIONES == 0 else 0

        #--Semantico Inicio
        if buscarTipoId(auxID, ptrTS_actual) != "null" :
            if  buscarTipoFuncion(auxID, ptrTS_actual) != "null" : # CASO: id(L)
                if buscarTipoParametrosFuncion(auxID, ptrTS_actual) == s1[0] :
                        aux = buscarTipoFuncion(auxID, ptrTS_actual)
                        return [ aux ]
                else:
                    Error_Sem("Parametros mal insertados, son : "+ str(s1[0])+ " deberia ser : "+ str(buscarTipoParametrosFuncion(auxID, ptrTS_actual)))
            else: #CASO id = E
                if buscarTipoId(auxID, ptrTS_actual) == s1[0] :
                    return ["tipo_ok"]
                else:
                    Error_Sem("asignacion mal formada")
        else:
            insertarTS( auxID, "entero" , DicTS["TS_General"][1], "TS_General")
            DicTS["TS_General"][1] += 2
            if "entero" == s1[0] :
                return ["tipo_ok"]
            else:
                Error_Sem("asignacion mal formada")
        #--Semantico Fin

    elif LISTA_TOKENS[NTOKENS] == "return":
        PARSE_ORDEN+="14 "
        print Tab*"  "+"S → return X" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        ComprobarToken("return")
        x=X() #x=[tipo]
        Tab-=1 if SAL_ACCIONES == 0 else 0

        #--Semantico Inicio
        return x
        #--Semantico Fin

    elif LISTA_TOKENS[NTOKENS] == "write":
        PARSE_ORDEN+="15 "
        print Tab*"  "+"S → write (E)" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        ComprobarToken("write")
        ComprobarToken("(")
        e=E0() #e=[tipo]
        ComprobarToken(")")
        Tab-=1 if SAL_ACCIONES == 0 else 0

        #--Semantico Inicio
        return e
        #--Semantico Fin

    else:
        PARSE_ORDEN+="16 "
        print Tab*"  "+"S → prompt (id)" if SAL_ACCIONES == 0 else ""
        ComprobarToken("prompt")
        ComprobarToken("(")
        ComprobarToken("id")
        ComprobarToken(")")

        #--Semantico Inicio
        if buscarTipoId(TSaux[N_IDS], ptrTS_actual) != "entero" and buscarTipoId(TSaux[N_IDS],ptrTS_actual) != "cadena" :
            Error_Sem("uso incorrecto de \"prompt\"")
        else :
            aux = buscarTipoId(TSaux[N_IDS], ptrTS_actual)
            N_IDS+=1
            return [ aux ]
        #--Semantico Fin

    #--Sintactico Fin

# S'→ (L) | = E
def S1(): #s1=[tipo]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, PARSE_ORDEN

    #--Sintactico Inicio
    if LISTA_TOKENS[NTOKENS] == "(":
        PARSE_ORDEN+="17 "
        print Tab*"  "+"S'→ (L)" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        ComprobarToken("(")
        l=L() #l=[tipo]
        ComprobarToken(")")
        Tab-=1 if SAL_ACCIONES == 0 else 0

        #--Semantico Inicio
        return l
        #--Semantico Fin

    else:
        PARSE_ORDEN+="18 "
        print Tab*"  "+"S'→ = E" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        ComprobarToken("=")
        e=E0() #e=[tipo]
        Tab-=1 if SAL_ACCIONES == 0 else 0

        #--Semantico Inicio
        return e
        #--Semantico Fin

    #--Sintactico Fin

# X → E | 𝝺
def X(): #x=[tipo]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, PARSE_ORDEN

    #--Sintactico Inicio
    la_E = str(LISTA_TOKENS[NTOKENS])
    if la_E == "id" or la_E == "(" or la_E == "entero" or la_E == "cadena" or la_E == "True" or la_E == "False":
        PARSE_ORDEN+="19 "
        print Tab*"  "+"X → E" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        e=E0() #e=[tipo]
        Tab-=1 if SAL_ACCIONES == 0 else 0

        #--Semantico Inicio
        return e
        #--Semantico Fin

    else:
        PARSE_ORDEN+="20 "
        print Tab*"  "+"X → 𝝺" if SAL_ACCIONES == 0 else ""

        #--Semantico Inicio
        return["tipo_vacio"]
        #--Semantico Fin

    #--Sintactico Fin

# L → E Q | 𝝺
def L(): #l=[tipo]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, PARSE_ORDEN

    #--Sintactico Inicio
    la_E = str(LISTA_TOKENS[NTOKENS])
    if la_E == "id" or la_E == "(" or la_E == "entero" or la_E == "cadena" or la_E == "True" or la_E == "False":
        PARSE_ORDEN+="21 "
        print Tab*"  "+"L → E Q" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        e=E0() #e=[tipo]
        q=Q() #q=[tipo]
        Tab-=1 if SAL_ACCIONES == 0 else 0

        #--Semantico Inicio
        if e[0] != "tipo_error" and q[0] != "tipo_error" :
            if q[0] != "tipo_vacio":
                return [str(e[0])+","+str(q[0])]
            else:
                return [str(e[0])]
        else:
            Error_Sem("contenido parentesis del identificador llamado mal formado")
        #--Semantico Fin

    else:
        PARSE_ORDEN+="22 "
        print Tab*"  "+"L → 𝝺" if SAL_ACCIONES == 0 else ""

        #--Semantico Inicio
        return ["tipo_vacio"]
        #--Semantico Fin

    #--Sintactico Fin

# Q → , E Q | 𝝺
def Q(): #q=[tipo]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, PARSE_ORDEN

    #--Sintactico Inicio
    if LISTA_TOKENS[NTOKENS] == ",":
        PARSE_ORDEN+="23 "
        print Tab*"  "+"Q → , E Q" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        ComprobarToken(",")
        e=E0() #e=[tipo]
        q=Q() #q=[tipo]
        Tab-=1 if SAL_ACCIONES == 0 else 0

        #--Semantico Inicio
        if e[0] != "tipo_error" and q[0] != "tipo_error":
            if q[0] != "tipo_vacio" :
                return [str(e[0])+","+str(q[0])]
            else:
                return [str(e[0])]
        else:
            Error_Sem("contenido parentesis del identificador llamado mal formado")
        #--Semantico Fin

    else:
        PARSE_ORDEN+="24 "
        print Tab*"  "+"Q → 𝝺" if SAL_ACCIONES == 0 else ""

        #--Semantico Inicio
        return ["tipo_vacio"]
        #--Semantico Fin

    #--Sintactico Fin

# # E → R E'
def E0(): #e=[tipo]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, PARSE_ORDEN
    PARSE_ORDEN+="25 "

    #--Sintactico Inicio
    print Tab*"  "+"E → R E'" if SAL_ACCIONES == 0 else ""
    Tab+=1 if SAL_ACCIONES == 0 else 0
    r=R0() #r=[tipo]
    e1=E1() #e1=[tipo]
    Tab-=1 if SAL_ACCIONES == 0 else 0
    #--Sintactico Fin

    #--Semantico Inicio
    if e1[0] != "tipo_vacio" and r[0] != e1[0] :
        Error_Sem("Comparacion de elementos con tipos distintos" )
    else :
        if e1[0] != "tipo_vacio" :
            return ["logico"]
        else :
            return r
    #--Semantico Fin

# E'→ && R E' | 𝝺
def E1(): #e1=[tipo]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, PARSE_ORDEN

    #--Sintactico Inicio
    if LISTA_TOKENS[NTOKENS] == "&&":
        PARSE_ORDEN+="26 "
        print Tab*"  "+"E'→ && R E'" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        ComprobarToken("&&")
        r=R0() #r=[tipo]
        e1=E1() #e1=[tipo]
        Tab-=1 if SAL_ACCIONES == 0 else 0

        #--Semantico Inicio
        if e1[0] != "tipo_vacio" and e1[0] != r[0] != "logico":
            Error_Sem("Comparacion de elementos de tipo no logico")
        else :
            return r
        #--Semantico Fin

    else:
        PARSE_ORDEN+="27 "
        print Tab*"  "+"E' → 𝝺" if SAL_ACCIONES == 0 else ""

        #--Semantico Inicio
        return["tipo_vacio"]
        #--Semantico Fin

    #--Sintactico Fin

# R → U R'
def R0(): #r=[tipo]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, PARSE_ORDEN
    PARSE_ORDEN+="28 "

    #--Sintactico Inicio
    print Tab*"  "+"R → U R'" if SAL_ACCIONES == 0 else ""
    Tab+=1 if SAL_ACCIONES == 0 else 0
    u=U0() #u=[tipo]
    r1=R1()    #r1=[tipo]
    Tab-=1 if SAL_ACCIONES == 0 else 0
    #--Sintactico Fin

    #--Semantico Inicio
    if r1[0] != "tipo_vacio" and u[0] != r1[0] :
        Error_Sem("Comparacion de elementos con tipos distintos")
    else :
        if r1[0] != "tipo_vacio" :
            return ["logico"]
        else :
            return u
    #--Semantico Fin

# R'→ > U R'| 𝝺
def R1(): #r1=[tipo]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, PARSE_ORDEN

    #--Sintactico Inicio
    if LISTA_TOKENS[NTOKENS] == ">":
        PARSE_ORDEN+="29 "
        print Tab*"  "+"R'→ > U R'" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        ComprobarToken(">")
        u=U0() #u=[tipo]
        r1=R1()    #r1=[tipo]
        Tab-=1 if SAL_ACCIONES == 0 else 0

        #--Semantico Inicio
        if r1[0] != "tipo_vacio" and r1[0] != u[0] != "entero" :
            Error_Sem("Comparacion de elementos de tipo no entero")
        else :
            return u
        #--Semantico Fin

    else:
        PARSE_ORDEN+="30 "
        print Tab*"  "+"R' → 𝝺" if SAL_ACCIONES == 0 else ""

        #--Semantico Inicio
        return ["tipo_vacio"]
        #--Semantico Fin

    #--Sintactico Fin

# U → V U'
def U0(): #u=[tipo]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, PARSE_ORDEN
    PARSE_ORDEN+="31 "

    #--Sintactico Inicio
    print Tab*"  "+"U → V U'" if SAL_ACCIONES == 0 else ""
    Tab+=1 if SAL_ACCIONES == 0 else 0
    v=V0() #v=[tipo]
    u1=U1()    #ui=[tipo]
    Tab-=1 if SAL_ACCIONES == 0 else 0
    #--Sintactico Fin

    #--Semantico Inicio
    if u1[0] != "tipo_vacio" and v[0] != u1[0] :
        Error_Sem("Suma de elementos de tipo no entero")
    else :
        if u1[0] != "tipo_vacio" :
            return ["entero"]
        else :
            return v
    #--Semantico Fin

# U'→ + V U' | 𝝺
def U1(): #u1=[tipo]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, PARSE_ORDEN

    #--Sintactico Inicio
    if LISTA_TOKENS[NTOKENS] == "*" :
        PARSE_ORDEN+="32 "
        print Tab*"  "+"U'→ + V U'" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        ComprobarToken("*")
        v=V0() #v=[tipo]
        u1=U1()    #ui=[tipo]
        Tab-=1 if SAL_ACCIONES == 0 else 0

        #--Semantico Inicio
        if v[0] != "entero" :
            Error_Sem("Suma de elementos de tipo no entero")
        else :
            return v
        #--Semantico Fin

    else:
        print Tab*"  "+"U' → 𝝺" if SAL_ACCIONES == 0 else ""
        PARSE_ORDEN+="33 "

        #--Semantico Inicio
        return ["tipo_vacio"]
        #--Semantico Fin

    #--Sintactico Fin

# V → id V' | (E) | entero | cadena | True | False
def V0(): #v=[tipo] or v=[tipo, numParam]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, TSaux, N_IDS, PARSE_ORDEN

    #--Sintactico Inicio
    if LISTA_TOKENS[NTOKENS] == "id" :
        PARSE_ORDEN+="34 "
        print Tab*"  "+"V → id V'" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        ComprobarToken("id")
        auxID=TSaux[N_IDS]
        N_IDS+=1
        v1=V1() #v1=[tipo]
        Tab-=1 if SAL_ACCIONES == 0 else 0

        #--Semantico Inicio
        if buscarTipoId(auxID, ptrTS_actual) != "null" :
            if  buscarTipoFuncion(auxID, ptrTS_actual) != "null" : # CASO: id(L)
                if  buscarTipoParametrosFuncion(auxID, ptrTS_actual) == v1[0] :
                    aux = buscarTipoFuncion(auxID, ptrTS_actual)
                    return [ aux ]
                else:
                    Error_Sem("Parametros mal insertados, son : "+ str(v1[0])+ " deberia ser : "+ str(buscarTipoParametrosFuncion(auxID, ptrTS_actual)))
            else: #CASO id
                aux = buscarTipoId(auxID, ptrTS_actual)
                return [ aux ]
        else:
            insertarTS( auxID, "entero" , DicTS["TS_General"][1], "TS_General")
            DicTS["TS_General"][1] += 2
            return ["entero"]
        #--Semantico Fin

    elif LISTA_TOKENS[NTOKENS] == "(" :
        PARSE_ORDEN+="35 "
        print Tab*"  "+"V → (E)" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        ComprobarToken("(")
        e=E0() #e=[tipo]
        ComprobarToken(")")
        Tab-=1 if SAL_ACCIONES == 0 else 0

        #--Semantico Inicio
        return e
        #--Semantico Fin

    elif LISTA_TOKENS[NTOKENS] == "entero" :
        PARSE_ORDEN+="36 "
        print Tab*"  "+"V → entero" if SAL_ACCIONES == 0 else ""
        ComprobarToken("entero")

        #--Semantico Inicio
        return["entero"]
        #--Semantico Fin

    elif LISTA_TOKENS[NTOKENS] == "cadena" :
        PARSE_ORDEN+="37 "
        print Tab*"  "+"V → cadena" if SAL_ACCIONES == 0 else ""
        ComprobarToken("cadena")

        #--Semantico Inicio
        return["cadena"]
        #--Semantico Fin

    elif LISTA_TOKENS[NTOKENS] == "True" :
        PARSE_ORDEN+="38 "
        print Tab*"  "+"V → True" if SAL_ACCIONES == 0 else ""
        ComprobarToken("True")

        #--Semantico Inicio
        return ["logico"]
        #--Semantico Fin

    else:
        PARSE_ORDEN+="39 "
        print Tab*"  "+"V → False" if SAL_ACCIONES == 0 else ""
        ComprobarToken("False")

        #--Semantico Inicio
        return ["logico"]
        #--Semantico Fin

    #--Sintactico Fin

# V'→ (L) | ++ | 𝝺
def V1(): #v1=[tipo] o v1=[tipo,numParam]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, PARSE_ORDEN

    #--Sintactico Inicio
    if LISTA_TOKENS[NTOKENS] == "(" :
        PARSE_ORDEN+="40 "
        print Tab*"  "+"V'→ (L)" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        ComprobarToken("(")
        l=L() #l=[tipo]
        ComprobarToken(")")
        Tab-=1 if SAL_ACCIONES == 0 else 0

        #--Semantico Inicio
        return l
        #--Semantico Fin

    elif LISTA_TOKENS[NTOKENS] == "++" :
        PARSE_ORDEN+="41 "
        print Tab*"  "+"V'→ ++" if SAL_ACCIONES == 0 else ""
        ComprobarToken("++")

        #--Semantico Inicio
        if buscarTipoId(TSaux[N_IDS-1], ptrTS_actual) != "entero":
            Error_Sem("uso incorrecto de \"++\"")
        #--Semantico Fin

    else:
        PARSE_ORDEN+="42 "
        print Tab*"  "+"V'→ 𝝺" if SAL_ACCIONES == 0 else ""

        #--Semantico Inicio
        return ["tipo_vacio"]
        #--Semantico Fin

    #--Sintactico Fin

# F → function H id (A) Z { Z C }
def F():
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, TSaux, N_IDS, DicTS, ptrTS_actual, PARSE_ORDEN
    PARSE_ORDEN+="43 "

    #--Sintactico Inicio
    print Tab*"  "+"F → function H id (A) Z { Z C }" if SAL_ACCIONES == 0 else ""
    Tab+=1 if SAL_ACCIONES == 0 else 0
    ComprobarToken("function")
    h=H() # h=[tipo,tamano]
    ComprobarToken("id")
    #--Sintactico Fin

    #--Semantico Inicio
    if buscarTS(TSaux[N_IDS]) != "null":
        Error_Sem("Función ya declarada")
    elif ptrTS_actual != "TS_General" :
        Error_Sin()
    else :
        insertarTS(TSaux[N_IDS], "function", DicTS[ptrTS_actual][1], ptrTS_actual)
        DicTS[ptrTS_actual][1]+=4
        ptrTS_anterior = ptrTS_actual
        ptrTS_actual = TSaux[N_IDS]
        DicTS[ptrTS_actual] = [ [], 0, ptrTS_anterior ] # Crea e inicializa la TS_nueva y Desp_nuevo
        N_IDS+=1
    #--Semantico Fin

    #--Sintactico Inicio
    ComprobarToken("(")
    a=A() # a=[tipo,numParam]
    ComprobarToken(")")
    Z0()
    ComprobarToken("{")
    #--Sintactico Fin

    #--Semantico Inicio
    insertarFunTS(ptrTS_anterior, ptrTS_actual, a[1], a[0], h[0], ptrTS_anterior)
    #--Semantico Fin

    #--Sintactico Inicio
    Z0()
    c=C()
    ComprobarToken("}")
    Tab-=1 if SAL_ACCIONES == 0 else 0
    #--Sintactico Fin

    #--Semantico Inicio
    if c[0] != h[0] and c[0] != "tipo_ok":
        Error_Sem("Funcion mal return c: "+str(c)+" h:"+str(h))
    else:
        ptrTS_actual      = ptrTS_anterior
        ptrTS_anterior     = "null"
    #--Semantico Fin

# H → T | 𝝺       // H tipo de retorno de la función
def H(): #h=[tipo,tamano]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, PARSE_ORDEN

    #--Sintactico Inicio
    la_T = str(LISTA_TOKENS[NTOKENS])
    if la_T == "int" or la_T == "bool" or la_T == "char" :
        PARSE_ORDEN+="44 "
        print Tab*"  "+"H → T" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        t=T() #t=[tipo,tamano]
        Tab-=1 if SAL_ACCIONES == 0 else 0
    else:
        PARSE_ORDEN+="45 "
        print Tab*"  "+"H → 𝝺" if SAL_ACCIONES == 0 else ""
        t=[ "tipo_vacio", 0 ] #t=[tipo,tamano]
    #--Sintactico Fin

    #--Semantico Inicio
    return t
    #--Semantico Fin

# A → T id K | 𝝺
def A(): #A=[tipo,numParam]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, TSaux, N_IDS, DicTS, ptrTS_actual, PARSE_ORDEN

    #--Sintactico inicio
    la_T = str(LISTA_TOKENS[NTOKENS])
    if la_T == "int" or la_T == "bool" or la_T == "char" :
        PARSE_ORDEN+="46 "
        print Tab*"  "+"A → T id K" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        t=T() #t=[tipo,tamano]
        ComprobarToken("id")
        #print ("id -->"+TSaux[N_IDS])

        #--Semantico Inicio
        if buscarId(TSaux[N_IDS], ptrTS_actual) != "null":
            Error_Sem("Identificador ya creado")
        else:
            insertarTS(TSaux[N_IDS], t[0], DicTS[ptrTS_actual][1], ptrTS_actual)
            DicTS[ptrTS_actual][1] += t[1]
            N_IDS+=1
        #--Semantico Fin

        k=K() #k=[tipo,numParam]
        Tab-=1 if SAL_ACCIONES == 0 else 0

        #--Semantico Inicio
        if k[0] != "tipo_vacio":
            tipo = str(t[0])+","+str(k[0])
        else:
            tipo = str(t[0])
        numParam = int(k[1]) + 1
        return [ tipo, numParam ]
        #--Semantico Fin

    else:
        PARSE_ORDEN+="47 "
        print Tab*"  "+"A → 𝝺" if SAL_ACCIONES == 0 else ""

        #--Semantico Inicio
        tipo = "tipo_vacio"
        numParam = 0
        return [ tipo, numParam ]
        #--Semantico Fin

    #--Sintactico Fin

# K → , T id K | 𝝺
def K(): #k=[tipo,numParam]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, TSaux, N_IDS, DicTS, ptrTS_actual, PARSE_ORDEN

    #--Sintactico Inicio
    if LISTA_TOKENS[NTOKENS] == ",":
        PARSE_ORDEN+="48 "
        print Tab*"  "+"K → , T id K" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        ComprobarToken(",")
        t=T() #t=[tipo,tamano]
        ComprobarToken("id")

        #--Semantico Inicio
        if buscarId(TSaux[N_IDS], ptrTS_actual) != "null":
            Error_Sem("Identificador ya creado")
        else:
            insertarTS(TSaux[N_IDS], t[0], DicTS[ptrTS_actual][1], ptrTS_actual)
            DicTS[ptrTS_actual][1] += t[1]
            N_IDS+=1
        #--Semantico Fin

        k=K() #k=[tipo,numParam]
        Tab-=1 if SAL_ACCIONES == 0 else 0

        #--Semantico Inicio
        if k[0] != "tipo_vacio":
            tipo = str(t[0])+","+str(k[0])
        else:
            tipo = str(t[0])
        numParam = int(k[1]) + 1
        return [ tipo, numParam ]
        #--Semantico Fin

    else:
        PARSE_ORDEN+="49 "
        print Tab*"  "+"K → 𝝺" if SAL_ACCIONES == 0 else ""

        #--Semantico Inicio
        tipo = "tipo_vacio"
        numParam = 0
        return [ tipo, numParam ]
        #--Semantico Fin

    #--Sintactico Fin

# Z → cr Z'
def Z0():
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, contCr, PARSE_ORDEN
    PARSE_ORDEN+="50 "

    #--Sintactico Inicio
    print Tab*"  "+"Z → cr Z'" if SAL_ACCIONES == 0 else ""
    ComprobarToken("cr")
    Z1()
    contCr+=1
    #--Sintactico Fin

# Z' → cr Z' | 𝝺
def Z1():
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, contCr, PARSE_ORDEN

    #--Sintactico Inicio
    if LISTA_TOKENS[NTOKENS] == "cr":
        print Tab*"  "+"Z' → cr Z'" if SAL_ACCIONES == 0 else ""
        PARSE_ORDEN+="51 "
        ComprobarToken("cr")
        Z1()
        contCr+=1
    else:
        PARSE_ORDEN+="52 "
        print Tab*"  "+"Z' → 𝝺" if SAL_ACCIONES == 0 else ""
        t=[ "tipo_vacio", 0 ] #t=[tipo,tamano]
    #--Sintactico Fin

# C → B Z C | 𝝺       // cuerpo de la función
def C(): #c=[tipo]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, PARSE_ORDEN

    #--Sintactico Inicio
    la_B = str(LISTA_TOKENS[NTOKENS])
    if la_B == "var" or la_B == "if" or la_B == "id" or la_B == "return" or la_B == "write" or la_B == "prompt":
        PARSE_ORDEN+="53 "
        print Tab*"  "+"C → B Z C" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        b=B0() #b=[tipo]
        Z0()
        c=C() #c=[tipo]
        Tab-=1 if SAL_ACCIONES == 0 else 0

        #--Semantico Inicio
        if c[0] != "tipo_error" or b[0] != "tipo_error":
            return ["tipo_ok"]
        else:
            Error_Sem("contenido de corchetes mal formado")
        #--Semantico Fin

    else:
        PARSE_ORDEN+="54 "
        print Tab*"  "+"C → 𝝺" if SAL_ACCIONES == 0 else ""

        #--Semantico Inicio
        return ["tipo_vacio"]
        #--Semantico Fin

    #--Sintactico Fin

# W → case Y : S M Z N
def W0():
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, PARSE_ORDEN

    #--Sintactico Inicio
    PARSE_ORDEN+="55 "
    print Tab*"  "+"W → case Y : S M Z N" if SAL_ACCIONES == 0 else ""
    Tab+=1 if SAL_ACCIONES == 0 else 0
    ComprobarToken("case")
    Y0() #l=[tipo]
    ComprobarToken(":")
    s = S0()
    M0()
    Z0()
    N0()
    Tab-=1 if SAL_ACCIONES == 0 else 0

        #--Semantico Inicio
    return s
        #--Semantico Fin
    #--Sintactico Fin

# Y → entero
def Y0(): #t=[tipo,tamano]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, PARSE_ORDEN

    #--Sintactico Inicio
    PARSE_ORDEN+="56 "
    print Tab*"  "+"Y → entero" if SAL_ACCIONES == 0 else ""
    ComprobarToken("entero")

        #--Semantico Inicio
    return [ "entero", 2 ]
        #--Semantico Fin

# M → ; break | cr break | 𝝺
def M0(): #t=[tipo,tamano]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, PARSE_ORDEN

    #--Sintactico Inicio
    if LISTA_TOKENS[NTOKENS] == ";":
        PARSE_ORDEN+="57 "
        print Tab*"  "+"M → ; break" if SAL_ACCIONES == 0 else ""
        ComprobarToken(";")
        ComprobarToken("break")

    elif LISTA_TOKENS[NTOKENS] == "cr" and LISTA_TOKENS[NTOKENS+1] == "break":
            PARSE_ORDEN+="58 "
            print Tab*"  "+"M → cr break" if SAL_ACCIONES == 0 else ""
            ComprobarToken("cr")
            ComprobarToken("break")

    else:
        PARSE_ORDEN+="59 "
        print Tab*"  "+"M → 𝝺" if SAL_ACCIONES == 0 else ""

        #--Semantico Inicio
        return ["tipo_vacio"]
        #--Semantico Fin

def N0(): #t=[tipo,tamano]
    global NTOKENS, LISTA_TOKENS, SAL_ACCIONES, Tab, PARSE_ORDEN

    #--Sintactico Inicio
    if LISTA_TOKENS[NTOKENS] == "case":
        #--Sintactico Inicio
        PARSE_ORDEN+="60 "
        print Tab*"  "+"N → case Y : S M Z N" if SAL_ACCIONES == 0 else ""
        Tab+=1 if SAL_ACCIONES == 0 else 0
        ComprobarToken("case")
        Y0() #l=[tipo]
        ComprobarToken(":")
        s = S0()
        M0()
        Z0()
        N0()
        Tab-=1 if SAL_ACCIONES == 0 else 0

            #--Semantico Inicio
        return s
            #--Semantico Fin
        #--Sintactico Fin

    else:
        PARSE_ORDEN+="61 "
        print Tab*"  "+"N → 𝝺" if SAL_ACCIONES == 0 else ""

        #--Semantico Inicio
        return ["tipo_vacio"]
        #--Semantico Fin

def Error_Sin():
    global NTOKENS, LISTA_TOKENS, contCr, FICHERO_ERROR
    print "ERROR Sintactico --> Token_Actual : "+ str(LISTA_TOKENS[NTOKENS])+ " en linea :" +str(contCr)
    FICHERO_ERROR.write("ERROR Sintactico --> Token_Actual : "+ str(LISTA_TOKENS[NTOKENS])+ " en linea :" +str(contCr))
    imprimirTS()
    parse()
    exit()

def ComprobarToken(T):
    global NTOKENS, LISTA_TOKENS, SAL_TERMINALES, TSaux, N_IDS
    if LISTA_TOKENS[NTOKENS] == str(T):
        print "TERMINAL --> "+str(LISTA_TOKENS[NTOKENS]) if SAL_TERMINALES == 0 else ""
        if str(T) == "id" :
            print " ID --> "+TSaux[N_IDS] if SAL_TERMINALES == 0 else ""
        NTOKENS += 1
    else:
        Error_Sin()

def Error_Sem(txt):
    global contCr, FICHERO_ERROR
    print str("ERROR Semantico --> "+txt +", en linea: "+ str(contCr))
    FICHERO_ERROR.write("ERROR Semantico --> "+txt +", en linea: "+ str(contCr))
    imprimirTS()
    parse()
    exit()

def imprimirTS():
    global DicTS
    salidaTS = ""
    for i in DicTS:
        salidaTS+="CONTENIDO DE LA TABLA # "+str(i)+" :\n\n"
        for n in DicTS[i][0]:
            salidaTS+= "* LEXEMA : '"+ n[1]+ "'\n"
            salidaTS+= "  ATRIBUTOS :\n"
            salidaTS+= "  + tipo : "+ n[2]+ "\n"
            salidaTS+= "  + desplazamiento : "+ n[3]+ "\n"
            salidaTS+= "  + Tam_parametros : "+ n[4]+ "\n" if n[2] == "function" else ""
            salidaTS+= "  + Tipo_parametro : "+ n[5]+ "\n" if n[2] == "function" else ""
            salidaTS+= "  + Retorno_funcion : "+ n[6]+ "\n" if n[2] == "function" else ""
            salidaTS+= "  + ptrTS_padre : "+ n[7]+ "\n" if n[2] == "function" else ""
            salidaTS+= "--------- ----------\n"
        salidaTS+="================================================\n"
    fichTokens = open('tabla_simbolo.txt', 'w')
    fichTokens.write(str(salidaTS))
    fichTokens.close()

def parse():
    global PARSE_ORDEN
    fichTokens = open('parse_descendente.txt', 'w')
    fichTokens.write("Des "+str(PARSE_ORDEN))
    fichTokens.close()

######################          FIN ANALIZADOR SINTACTICO        ######################

def main():
    global FICHERO_ERROR
    print (50*"-")+"\n"
    analizadorLexico ()
    analizadorSintactico()
    imprimirTS()
    parse()
    FICHERO_ERROR.close()
    if os.stat('fichero_error.txt').st_size == 0: os.remove("fichero_error.txt")
    print (50*"-")+"\n"

if __name__ == "__main__":
    main()

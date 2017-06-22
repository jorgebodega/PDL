# -*- coding: utf-8 -*-
import yaml, os, pprint, sys

#Cargamos el fichero de configuracion
path = os.path.dirname(os.path.abspath(__file__))
with open( path + '/config.yml', 'r') as f:
	config = yaml.load(f)

if len(sys.argv) != 2:
	print "Error, solo pasar el archivo"
	exit()
# Consola
#with open('config.yml', 'r') as f:
#	config = yaml.load(f)

#pprint.pprint(config)

# En primer lugar debemos de abrir el fichero que vamos a leer.
# Usa 'r' para tener acceso de lectura.
infile = open(sys.argv[1], 'r')

# Volacamos el contenido del fichero en 'fich', vara tratarlo como una cadena.
fich = infile.read()
infile.close()

#Variables Lexico
#--------------------------------------
Tokens = []
ListaTokens = []
contadorTokens=0
TSaux = [] # TSaux[POS] = LEX --> [ POS | LEX ]

#Variables Sintactico
#--------------------------------------
sal0=1 #Acciones
sal1=1 #Terminales leidos
Tab=1
contCr=0

#Variables Semantico y TS
#--------------------------------------
DicTS = {} # DicTS[ident] = [TS, Desp, ptrTS_padre]
#Desp = numero
#TS = [ POS | LEXEMA | TIPO | DESPLAZAMIENTO | TAMANO_PARAMETROS | TIPO_PARAMETROS | TIPO_RETURN | PTRTS_ HIJO ]
#		 0		1		2			3				4					5				  6				7
ptrTS_actual = "null"	# ptrTS_actual 	=> identificador (ident) TS actual en DicTS
contadorIds = 0			# TSaux[contadorIds] =>  id.ent por orden de aparicion
parseOrden = ""

#Funciones TS
#--------------------------------------
# buscarTS 			=> busca si existe TS en DicTS
# buscarId 			=> busca si exixte el id en la TS actual, en caso contrario devuelve null
# buscarTipoId 		=> busca si existe el id en la TS actual y devuelve su tipo, si no existe devuelve null
# buscarTipoFuncion => busca si existe el id en la TS actual y es de tipo "function" y devuelve el tipo de parametros que se le pasa, si no existe, o no es funcion, devuelve null
# insertarTS 		=> inserta un id en la TS actual
# insertarFunTs 	=> inserta los parametros de una funcion dado un ptrTS valido
# crearTS 			=> crea una TS nueva

# pprint.pprint(DicTS[ptrTS_actual][0])

# buscarTS 			=> busca si existe TS en DicTS, si no devuelve null
def buscarTS(ident) :
	global DicTS
	try:
		return DicTS[str(ident)]
	except:
		return "null"
# buscarId 			=> busca si exixte el id en la TS actual, en caso contrario devuelve null
def buscarId(ident, ptrTS_actual) :
	global DicTS
	ptrTS_busqueda = ptrTS_actual
	if str(ident) in [ DicTS[str(ptrTS_busqueda)][0][n][1] for n in range(len(DicTS[str(ptrTS_busqueda)][0])) ] :
		return  str(ident)
	elif DicTS[str(ptrTS_busqueda)][2] != "null" :
		return buscarId(ident, DicTS[str(ptrTS_busqueda)][2])
	else : # sino miramos en la TS_padre
		return "null"
# buscarTipoId 		=> busca si existe el id en la TS actual y devuelve su tipo, si no existe devuelve null
def buscarTipoId(ident, ptrTS_actual) :
	global DicTS
	ptrTS_busqueda = ptrTS_actual
	if str(ident) in [ DicTS[str(ptrTS_busqueda)][0][n][1] for n in range(len(DicTS[str(ptrTS_busqueda)][0])) ] :
		return  [ DicTS[str(ptrTS_busqueda)][0][n][2] for n in range(len(DicTS[str(ptrTS_busqueda)][0])) ][ [ DicTS[str(ptrTS_busqueda)][0][n][1] for n in range(len(DicTS[str(ptrTS_busqueda)][0])) ].index(str(ident))]
	elif DicTS[str(ptrTS_busqueda)][2] != "null" :
		return buscarTipoId(ident, DicTS[str(ptrTS_busqueda)][2])
	else :
		return "null"

# buscarTipoFuncion => busca si existe el id en la TS actual y es de tipo "function" y devuelve la salida de la funcion, si no existe, o no es funcion, devuelve null
def buscarTipoFuncion(ident, ptrTS_actual) :
	global DicTS
	ptrTS_busqueda = ptrTS_actual
	if str(ident) in [ DicTS[str(ptrTS_busqueda)][0][n][1] for n in range(len(DicTS[str(ptrTS_busqueda)][0])) ] and [ DicTS[str(ptrTS_busqueda)][0][n][2] for n in range(len(DicTS[str(ptrTS_busqueda)][0])) ][ [ DicTS[str(ptrTS_busqueda)][0][n][1] for n in range(len(DicTS[str(ptrTS_busqueda)][0])) ].index(str(ident))] == "function" :
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

# insertarTS 		=> inserta un id en la TS actual
def insertarTS(LEXEMA , TIPO , DESPLAZAMIENTO, ptrTST_actual) :
	global DicTS
	if str(LEXEMA) not in [ DicTS[str(ptrTS_actual)][0][n][1] for n in range(len(DicTS[str(ptrTS_actual)][0])) ] :
		DicTS[ptrTS_actual][0].append([len(DicTS[ptrTS_actual][0]), str(LEXEMA) , str(TIPO) , str(DESPLAZAMIENTO) , 'null' , 'null' , 'null' , 'null' , 'null' ])
		return "insertado"
	else :
		return "null"

# insertarFunTs 	=> inserta los parametros de una funcion dado un ptrTS valido
def	insertarFunTS(ptrTS_anterior, ident, tamano_parametros , tipo_parametros, tipo_return, ptrTS_hijo) :
	global DicTS
	if str(ident) in [ DicTS[str(ptrTS_anterior)][0][n][1] for n in range(len(DicTS[str(ptrTS_anterior)][0])) ] and [ DicTS[str(ptrTS_anterior)][0][n][2] for n in range(len(DicTS[str(ptrTS_anterior)][0])) ][ [ DicTS[str(ptrTS_anterior)][0][n][1] for n in range(len(DicTS[str(ptrTS_anterior)][0])) ].index(str(ident))] == "function" :
		DicTS[str(ptrTS_anterior)][0][[ DicTS[str(ptrTS_anterior)][0][n][1] for n in range(len(DicTS[str(ptrTS_anterior)][0])) ].index(str(ident))][4:] = [str(tamano_parametros) , str(tipo_parametros), str(tipo_return), str(ptrTS_hijo)]
		return "insertado"
	else :
		return "null"

######################		INICIO ANALIZADOR LEXICO		######################
def analizadorLexico():
	elemt  = ""
	coment = ""
	salida = 1
	entra = 0

	for caracter in fich :
		if caracter != " " and caracter != "\t" and caracter != "\n" and coment == "":
			#concatenamos el caracter a elemt
			elemt += caracter
			if salida == 1 : print elemt

		#Comporbamos si estamos en un comentario o cadena
		if coment != "":
			elemt += caracter
			#if salida == 1 : print "coment -->" +elemt

			if elemt[-2:] == "*/" or elemt[-1:] == "\n":
				if coment == "\n" and elemt[-1:] == "\n":
					Tokens.append("< %s , %s >"%("cr", "-"))
					ListaTokens.append("cr")
					if salida == 1 : print "< %s , %s >\n"%("cr","-")

				if salida == 1 : print ">>> FIN Comentario\n"
				coment = ""
				elemt = ""
				continue

			elif elemt[-1:] == "\"" and coment == "\"":
				Tokens.append("< %s , %s >"%("cadena", str(elemt)))
				ListaTokens.append("cadena")
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
						Tokens.append("< %s , %s >"%(str(config[elemt[:-2]]), str(elemt[:-2])))
						ListaTokens.append(str(elemt[:-2]))
						if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-2]]), str(elemt[:-2]))
					else:
						try:
							int(elemt[-2:])
							if int(elemt[-2:]) > 32767:
								Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- numero superior a 32767"))
								ListaTokens.append("ERROR")
								print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(ListaTokens.count("cr")+1))
							 	break
							else:
								Tokens.append("< %s , %s >"%("entero",str(elemt[:-2])))
								ListaTokens.append("entero")
								if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-2]))
								#if salida == 1 : print ">>> NUEVO ELEMETO [ENTERO]\n"
						except:
							if str(elemt[:-2]).isalnum() and str(elemt[:-2][:1]).isalpha() :
								Tokens.append("< %s , %s >"%("id",str(elemt[:-2]))) # tendria que ser  pos en TS
								ListaTokens.append("id")
								TSaux.append(str(elemt[:-2]))
								if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-2]))
								#if salida == 1 : print ">>> NUEVO ELEMETO [ID]\n"
							else:
								Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- identificador mal formado"))
								ListaTokens.append("ERROR")
								print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(ListaTokens.count("cr")+1))
							 	break

					#if salida == 1 : print ListaTokens
				coment= "*/"
				elemt = ""
				if salida == 1 : print ">>> NUEVO Comentario /*\n"

			#Elemento propio del lenguaje
			elif elemt in config :
				if elemt == "=":
					continue
				if entra == 1 : print "entra2"
				Tokens.append("< %s , %s >"%(str(config[elemt]), str(elemt)))
				ListaTokens.append(str(elemt))
				if salida == 1 : print "< %s , %s >\n"%(str(config[elemt]), str(elemt))
				elemt = ""
				#if salida == 1 : print ">>> NUEVO ELEMETO [CONF]\n"
				#if salida == 1 : print ListaTokens

			#Si acaba en salto de linea con elementos
			elif caracter == "\n" and elemt != "":
				if entra == 1 : print "entra3"
				#print "element -->"+str(elemt)+"\n"
				#print "element[:-1] -->"+str(elemt[:-1])+ "\n\n"
				if elemt in config :
					Tokens.append("< %s , %s >"%(str(config[elemt[:-1]]), str(elemt[:-1])))
					Tokens.append("< %s , %s >"%("cr", "-"))
					ListaTokens.append(str(elemt[:-1]))
					ListaTokens.append("cr")
					if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
					if salida == 1 : print "< %s , %s >\n"%("cr","-")
					#if salida == 1 : print ">>> NUEVO ELEMETO [CONF][CONF] 1\n"
				else:
					try:
						int(elemt)
						if int(elemt) > 32767:
							Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- numero superior a 32767"))
							ListaTokens.append("ERROR")
							print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(ListaTokens.count("cr")+1))
						 	break
						else:
							Tokens.append("< %s , %s >"%("entero",str(elemt)))
							ListaTokens.append("entero")
							if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt))
							#if salida == 1 : print ">>> NUEVO ELEMETO [ENTERO][CONF] 1\n"
					except:
						if str(elemt).isalnum() and str(elemt).isalpha() :
							Tokens.append("< %s , %s >"%("id",str(elemt))) # deberia ser  pos en  TS
							ListaTokens.append("id")
							TSaux.append(str(elemt))
							if salida == 1 : print "< %s , %s >\n"%("id",str(elemt))
							#if salida == 1 : print ">>> NUEVO ELEMETO [ID][CONF] 1\n"
						else:
							Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- identificador mal formado"))
							ListaTokens.append("ERROR")
							print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(ListaTokens.count("cr")+1))
						 	break
					Tokens.append("< %s , %s >"%("cr", "-"))
					ListaTokens.append("cr")
					if salida == 1 : print "< %s , %s >\n"%("cr","-")
				elemt = ""
				#if salida == 1 : print ListaTokens

			#Si acaba en salto de linea sin elementos
			elif caracter == "\n" and elemt == "":
				if entra == 1 : print "entra4"
				Tokens.append("< %s , %s >"%("cr", "-"))
				ListaTokens.append("cr")
				if salida == 1 : print "< %s , %s >\n"%("cr","-")
				#if salida == 1 : print ">>> NUEVO ELEMETO [CR]\n"
				#if salida == 1 : print ListaTokens

			#Comentariom de linea
			elif len(elemt) > 1 and elemt[-2:] == "//":
				if entra == 1 : print "entra5"
				if len (elemt) > 2:
					if elemt[:-2] in config :
						Tokens.append("< %s , %s >"%(str(config[elemt[:-2]]), str(elemt[:-2])))
						ListaTokens.append(elemt[:-2])
						if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-2]]), str(elemt[:-2]))
					else:
						try:
							int(elemt[:-2])
							if int(elemt[:-2]) > 32767:
								Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- numero superior a 32767"))
								ListaTokens.append("ERROR")
								print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(ListaTokens.count("cr")+1))
							 	break
							else:
								Tokens.append("< %s , %s >"%("entero",str(elemt[:-2])))
								ListaTokens.append("entero")
								if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-2]))
								#if salida == 1 : print ">>> NUEVO ELEMETO [ENTERO]\n"
						except:
							if str(elemt[:-2]).isalnum() and str(elemt[:-2][:1]).isalpha() :
								Tokens.append("< %s , %s >"%("id",str(elemt[:-2]))) # deberia ser  pos en  TS
								ListaTokens.append("id")
								TSaux.append(str(elemt[:-2]))
								if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-2]))
								#if salida == 1 : print ">>> NUEVO ELEMETO [ID]\n"
							else:
								Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- identificador mal formado"))
								ListaTokens.append("ERROR")
								print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(ListaTokens.count("cr")+1))
							 	break

					elemt = ""
					#if salida == 1 : print ListaTokens
					if salida == 1 : print ">>> NUEVO Comentario //\n"

				coment= "\n"
				elemt = ""

			#Acaba en fin de parentesis
			elif elemt[-1:] == ")":
				if entra == 1 : print "entra6"
				if len (elemt) > 1:
					if elemt[:-1] in config :
						Tokens.append("< %s , %s >"%(str(config[elemt[:-1]]), str(elemt[:-1])))
						Tokens.append("< %s , %s >"%(str(config[")"]), ")"))
						ListaTokens.append(str(elemt[:-1]))
						ListaTokens.append(")")
						if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
						if salida == 1 : print "< %s , %s >\n"%(str(config[")"]),")")
						#if salida == 1 : print ">>> NUEVO ELEMETO [CONF][CONF] 2\n"
					else:
						try:
							int(elemt[:-1])
							if int(elemt[:-1]) > 32767:
								Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- numero superior a 32767"))
								ListaTokens.append("ERROR")
								print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(ListaTokens.count("cr")+1))
							 	break
							else:
								Tokens.append("< %s , %s >"%("entero",str(elemt[:-1])))
								ListaTokens.append("entero")
								if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
								#if salida == 1 : print ">>> NUEVO ELEMETO [ENTERO][CONF] 2\n"
						except:
							if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
								Tokens.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
								ListaTokens.append("id")
								TSaux.append(str(elemt[:-1]))
								if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
								#if salida == 1 : print ">>> NUEVO ELEMETO [ID]\n"
							else:
								Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- identificador mal formado"))
								ListaTokens.append("ERROR")
								print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(ListaTokens.count("cr")+1))
							 	break

						Tokens.append("< %s , %s >"%(str(config[")"]), ")"))
						ListaTokens.append(")")
						if salida == 1 : print "< %s , %s >\n"%(str(config[")"]),")")

					elemt = ""
					#print ListaTokens
				elemt = ""

			#Empieza en igual
			elif elemt[:1] == "=" and len (elemt) > 1:
				Tokens.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
				ListaTokens.append(str(elemt[:1]))
				if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:1]]), str(elemt[:1]))
					#if salida == 1 : print ">>> NUEVO ELEMETO [CONF][CONF] 2\n"
				elemt = elemt[1:]
				if entra == 1 : print "entra7"
				if elemt[:1] == "\"":
					coment= "\""
					continue
				#print ListaTokens

			#Acaba en igual
			elif elemt[-1:] == "=" and len (elemt) > 1:
				if entra == 1 : print "entra8"
				if elemt[:-1] in config :
					Tokens.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
					ListaTokens.append(str(elemt[:1]))
					if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
					#if salida == 1 : print ">>> NUEVO ELEMETO [CONF][CONF] 2\n"
				else:
					try:
						int(elemt[:-1])
						if int(elemt[:-1]) > 32767:
							Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- numero superior a 32767"))
							ListaTokens.append("ERROR")
							print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(ListaTokens.count("cr")+1))
						 	break
						else:
							Tokens.append("< %s , %s >"%("entero",str(elemt[:-1])))
							ListaTokens.append("entero")
							if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
							#if salida == 1 : print ">>> NUEVO ELEMETO [EN111TERO][CONF] 2\n"
					except:
							if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
								Tokens.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
								ListaTokens.append("id")
								TSaux.append(str(elemt[:-1]))
								if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
								#if salida == 1 : print ">>> NUEVO ELEMETO [ID]\n"
							else:
								Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- identificador mal formado"))
								ListaTokens.append("ERROR")
								print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(ListaTokens.count("cr")+1))
							 	break

				elemt = elemt[-1:]
				continue
				#print ListaTokens

			#Empieza en mas
			elif elemt[:1] == "+" and len (elemt) > 1:
				Tokens.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
				ListaTokens.append(str(elemt[:1]))
				if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:1]]), str(elemt[:1]))
					#if salida == 1 : print ">>> NUEVO ELEMETO [CONF][CONF] 2\n"
				elemt = elemt[1:]
				if entra == 1 : print "entra7"
				if elemt[:1] == "\"":
					coment= "\""
					continue
				#print ListaTokens

			#Acaba en mas
			elif elemt[-1:] == "+" and len (elemt) > 1:
				if entra == 1 : print "entra8"
				if elemt[:-1] in config :
					Tokens.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
					ListaTokens.append(str(elemt[:1]))
					if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
					#if salida == 1 : print ">>> NUEVO ELEMETO [CONF][CONF] 2\n"
				else:
					try:
						int(elemt[:-1])
						if int(elemt[:-1]) > 32767:
							Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- numero superior a 32767"))
							ListaTokens.append("ERROR")
							print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(ListaTokens.count("cr")+1))
						 	break
						else:
							Tokens.append("< %s , %s >"%("entero",str(elemt[:-1])))
							ListaTokens.append("entero")
							if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
							#if salida == 1 : print ">>> NUEVO ELEMETO [EN111TERO][CONF] 2\n"
					except:
							if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
								Tokens.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
								ListaTokens.append("id")
								TSaux.append(str(elemt[:-1]))
								if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
								#if salida == 1 : print ">>> NUEVO ELEMETO [ID]\n"
							else:
								Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- identificador mal formado"))
								ListaTokens.append("ERROR")
								print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(ListaTokens.count("cr")+1))
							 	break

				elemt = elemt[-1:]
				continue
				#print ListaTokens

			#Empieza en mayor
			elif elemt[:1] == ">" and len (elemt) > 1:
				Tokens.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
				ListaTokens.append(str(elemt[:1]))
				if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:1]]), str(elemt[:1]))
					#if salida == 1 : print ">>> NUEVO ELEMETO [CONF][CONF] 2\n"
				elemt = elemt[1:]
				if entra == 1 : print "entra7"
				if elemt[:1] == "\"":
					coment= "\""
					continue
				#print ListaTokens

			#Acaba en mayor
			elif elemt[-1:] == ">" and len (elemt) > 1:
				if entra == 1 : print "entra8"
				if elemt[:-1] in config :
					Tokens.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
					ListaTokens.append(str(elemt[:1]))
					if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
					#if salida == 1 : print ">>> NUEVO ELEMETO [CONF][CONF] 2\n"
				else:
					try:
						int(elemt[:-1])
						if int(elemt[:-1]) > 32767:
							Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- numero superior a 32767"))
							ListaTokens.append("ERROR")
							print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(ListaTokens.count("cr")+1))
						 	break
						else:
							Tokens.append("< %s , %s >"%("entero",str(elemt[:-1])))
							ListaTokens.append("entero")
							if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
							#if salida == 1 : print ">>> NUEVO ELEMETO [EN111TERO][CONF] 2\n"
					except:
							if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
								Tokens.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
								ListaTokens.append("id")
								TSaux.append(str(elemt[:-1]))
								if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
								#if salida == 1 : print ">>> NUEVO ELEMETO [ID]\n"
							else:
								Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- identificador mal formado"))
								ListaTokens.append("ERROR")
								print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(ListaTokens.count("cr")+1))
							 	break

				elemt = elemt[-1:]
				continue
				#print ListaTokens

			#Empieza por coma
			elif elemt[:1] == "," and len (elemt) > 1:
				Tokens.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
				ListaTokens.append(str(elemt[:1]))
				if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:1]]), str(elemt[:1]))
					#if salida == 1 : print ">>> NUEVO ELEMETO [CONF][CONF] 2\n"
				elemt = elemt[1:]
				if entra == 1 : print "entra7"
				if elemt[:1] == "\"":
					coment= "\""
					continue
				#print ListaTokens

			#Acaba en coma
			elif elemt[-1:] == "," and len (elemt) > 1:
				if entra == 1 : print "entra8"
				if elemt[:-1] in config :
					Tokens.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
					ListaTokens.append(str(elemt[:1]))
					if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
					#if salida == 1 : print ">>> NUEVO ELEMETO [CONF][CONF] 2\n"
				else:
					try:
						int(elemt[:-1])
						if int(elemt[:-1]) > 32767:
							Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- numero superior a 32767"))
							ListaTokens.append("ERROR")
							print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(ListaTokens.count("cr")+1))
						 	break
						else:
							Tokens.append("< %s , %s >"%("entero",str(elemt[:-1])))
							ListaTokens.append("entero")
							if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
							#if salida == 1 : print ">>> NUEVO ELEMETO [EN111TERO][CONF] 2\n"
					except:
							if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
								Tokens.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
								ListaTokens.append("id")
								TSaux.append(str(elemt[:-1]))
								if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
								#if salida == 1 : print ">>> NUEVO ELEMETO [ID]\n"
							else:
								Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- identificador mal formado"))
								ListaTokens.append("ERROR")
								print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(ListaTokens.count("cr")+1))
							 	break

				elemt = elemt[-1:]
				continue
				#print ListaTokens

			#Empieza {
			elif elemt[:1] == "{" and len (elemt) > 1:
				Tokens.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
				ListaTokens.append(str(elemt[:1]))
				if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:1]]), str(elemt[:1]))
					#if salida == 1 : print ">>> NUEVO ELEMETO [CONF][CONF] 2\n"
				elemt = elemt[1:]
				if entra == 1 : print "entra7"
				if elemt[:1] == "\"":
					coment= "\""
					continue
				#print ListaTokens

			#Acaba  {
			elif elemt[-1:] == "{" and len (elemt) > 1:
				if entra == 1 : print "entra8"
				if elemt[:-1] in config :
					Tokens.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
					ListaTokens.append(str(elemt[:1]))
					if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
					#if salida == 1 : print ">>> NUEVO ELEMETO [CONF][CONF] 2\n"
				else:
					try:
						int(elemt[:-1])
						if int(elemt[:-1]) > 32767:
							Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- numero superior a 32767"))
							ListaTokens.append("ERROR")
							print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(ListaTokens.count("cr")+1))
						 	break
						else:
							Tokens.append("< %s , %s >"%("entero",str(elemt[:-1])))
							ListaTokens.append("entero")
							if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
							#if salida == 1 : print ">>> NUEVO ELEMETO [EN111TERO][CONF] 2\n"
					except:
							if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
								Tokens.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
								ListaTokens.append("id")
								TSaux.append(str(elemt[:-1]))
								if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
								#if salida == 1 : print ">>> NUEVO ELEMETO [ID]\n"
							else:
								Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- identificador mal formado"))
								ListaTokens.append("ERROR")
								print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(ListaTokens.count("cr")+1))
							 	break

				elemt = elemt[-1:]
				continue
				#print ListaTokens

			#Empieza }
			elif elemt[:1] == "}" and len (elemt) > 1:
				Tokens.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
				ListaTokens.append(str(elemt[:1]))
				if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:1]]), str(elemt[:1]))
					#if salida == 1 : print ">>> NUEVO ELEMETO [CONF][CONF] 2\n"
				elemt = elemt[1:]
				if entra == 1 : print "entra7"
				if elemt[:1] == "\"":
					coment= "\""
					continue
				#print ListaTokens

			#Acaba }
			elif elemt[-1:] == "}" and len (elemt) > 1:
				if entra == 1 : print "entra8"
				if elemt[:-1] in config :
					Tokens.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
					ListaTokens.append(str(elemt[:1]))
					if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
					#if salida == 1 : print ">>> NUEVO ELEMETO [CONF][CONF] 2\n"
				else:
					try:
						int(elemt[:-1])
						if int(elemt[:-1]) > 32767:
							Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- numero superior a 32767"))
							ListaTokens.append("ERROR")
							print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(ListaTokens.count("cr")+1))
						 	break
						else:
							Tokens.append("< %s , %s >"%("entero",str(elemt[:-1])))
							ListaTokens.append("entero")
							if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
							#if salida == 1 : print ">>> NUEVO ELEMETO [EN111TERO][CONF] 2\n"
					except:
							if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
								Tokens.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
								ListaTokens.append("id")
								TSaux.append(str(elemt[:-1]))
								if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
								#if salida == 1 : print ">>> NUEVO ELEMETO [ID]\n"
							else:
								Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- identificador mal formado"))
								ListaTokens.append("ERROR")
								print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(ListaTokens.count("cr")+1))
							 	break

				elemt = elemt[-1:]
				continue
				#print ListaTokens

			#Empieza (
			elif elemt[:1] == "(" and len (elemt) > 1:
				Tokens.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
				ListaTokens.append(str(elemt[:1]))
				if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:1]]), str(elemt[:1]))
					#if salida == 1 : print ">>> NUEVO ELEMETO [CONF][CONF] 2\n"
				elemt = elemt[1:]
				if entra == 1 : print "entra7"
				if elemt[:1] == "\"":
					coment= "\""
					continue
				#print ListaTokens

			#Acaba (
			elif elemt[-1:] == "(" and len (elemt) > 1:
				if entra == 1 : print "entra8"
				if elemt[:-1] in config :
					Tokens.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
					ListaTokens.append(str(elemt[:1]))
					if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
					#if salida == 1 : print ">>> NUEVO ELEMETO [CONF][CONF] 2\n"
				else:
					try:
						int(elemt[:-1])
						if int(elemt[:-1]) > 32767:
							Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- numero superior a 32767"))
							ListaTokens.append("ERROR")
							print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(ListaTokens.count("cr")+1))
						 	break
						else:
							Tokens.append("< %s , %s >"%("entero",str(elemt[:-1])))
							ListaTokens.append("entero")
							if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
							#if salida == 1 : print ">>> NUEVO ELEMETO [EN111TERO][CONF] 2\n"
					except:
							if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
								Tokens.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
								ListaTokens.append("id")
								TSaux.append(str(elemt[:-1]))
								if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
								#if salida == 1 : print ">>> NUEVO ELEMETO [ID]\n"
							else:
								Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- identificador mal formado"))
								ListaTokens.append("ERROR")
								print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(ListaTokens.count("cr")+1))
							 	break

				elemt = elemt[-1:]
				continue
				#print ListaTokens

			#Empieza )
			elif elemt[:1] == ")" and len (elemt) > 1:
				Tokens.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
				ListaTokens.append(str(elemt[:1]))
				if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:1]]), str(elemt[:1]))
					#if salida == 1 : print ">>> NUEVO ELEMETO [CONF][CONF] 2\n"
				elemt = elemt[1:]
				if entra == 1 : print "entra7"
				if elemt[:1] == "\"":
					coment= "\""
					continue
				#print ListaTokens

			#Acaba )
			elif elemt[-1:] == ")" and len (elemt) > 1:
				if entra == 1 : print "entra8"
				if elemt[:-1] in config :
					Tokens.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
					ListaTokens.append(str(elemt[:1]))
					if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
					#if salida == 1 : print ">>> NUEVO ELEMETO [CONF][CONF] 2\n"
				else:
					try:
						int(elemt[:-1])
						if int(elemt[:-1]) > 32767:
							Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- numero superior a 32767"))
							ListaTokens.append("ERROR")
							print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(ListaTokens.count("cr")+1))
						 	break
						else:
							Tokens.append("< %s , %s >"%("entero",str(elemt[:-1])))
							ListaTokens.append("entero")
							if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
							#if salida == 1 : print ">>> NUEVO ELEMETO [EN111TERO][CONF] 2\n"
					except:
							if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
								Tokens.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
								ListaTokens.append("id")
								TSaux.append(str(elemt[:-1]))
								if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
								#if salida == 1 : print ">>> NUEVO ELEMETO [ID]\n"
							else:
								Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- identificador mal formado"))
								ListaTokens.append("ERROR")
								print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(ListaTokens.count("cr")+1))
							 	break

				elemt = elemt[-1:]
				continue
				#print ListaTokens

			#Empieza por ,
			elif elemt[:1] == "," and len (elemt) > 1:
				Tokens.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
				ListaTokens.append(str(elemt[:1]))
				if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:1]]), str(elemt[:1]))
					#if salida == 1 : print ">>> NUEVO ELEMETO [CONF][CONF] 2\n"
				elemt = elemt[1:]
				if entra == 1 : print "entra7"
				if elemt[:1] == "\"":
					coment= "\""
					continue
				#print ListaTokens

			#Acaba en igual
			elif elemt[-1:] == "," and len (elemt) > 1:
				if entra == 1 : print "entra8"
				if elemt[:-1] in config :
					Tokens.append("< %s , %s >"%(str(config[elemt[:1]]), str(elemt[:1])))
					ListaTokens.append(str(elemt[:1]))
					if salida == 1 : print "< %s , %s >\n"%(str(config[elemt[:-1]]), str(elemt[:-1]))
					#if salida == 1 : print ">>> NUEVO ELEMETO [CONF][CONF] 2\n"
				else:
					try:
						int(elemt[:-1])
						if int(elemt[:-1]) > 32767:
							Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- numero superior a 32767"))
							ListaTokens.append("ERROR")
							print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(ListaTokens.count("cr")+1))
						 	break
						else:
							Tokens.append("< %s , %s >"%("entero",str(elemt[:-1])))
							ListaTokens.append("entero")
							if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt[:-1]))
							#if salida == 1 : print ">>> NUEVO ELEMETO [EN111TERO][CONF] 2\n"
					except:
							if str(elemt[:-1]).isalnum() and str(elemt[:-1][:1]).isalpha() :
								Tokens.append("< %s , %s >"%("id",str(elemt[:-1]))) # deberia ser  pos en  TS
								ListaTokens.append("id")
								TSaux.append(str(elemt[:-1]))
								if salida == 1 : print "< %s , %s >\n"%("id",str(elemt[:-1]))
								#if salida == 1 : print ">>> NUEVO ELEMETO [ID]\n"
							else:
								Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- identificador mal formado"))
								ListaTokens.append("ERROR")
								print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(ListaTokens.count("cr")+1))
							 	break

				elemt = elemt[-1:]
				continue
				#print ListaTokens

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
						Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- numero superior a 32767"))
						ListaTokens.append("ERROR")
						print "ERROR LEXICO, Linea %s- numero superior a 32767"%(str(ListaTokens.count("cr")+1))
					 	break
					else:
						Tokens.append("< %s , %s >"%("entero",str(elemt)))
						ListaTokens.append("entero")
					if salida == 1 : print "< %s , %s >\n"%("entero",str(elemt))
					#if salida == 1 : print ">>> NUEVO ELEMETO [ENTERO]\n"
				except:
					if elemt in config :
						Tokens.append("< %s , %s >"%(str(config[elemt]), str(elemt)))
						ListaTokens.append(str(elemt))
						if salida == 1 : print "< %s , %s >\n"%(str(config[elemt]), str(elemt))
					else:
							if str(elemt).isalnum() and str(elemt[:1]).isalpha() :
								Tokens.append("< %s , %s >"%("id",str(elemt))) # deberia ser  pos en  TS
								ListaTokens.append("id")
								TSaux.append(str(elemt))
								if salida == 1 : print "< %s , %s >\n"%("id",str(elemt))
								#if salida == 1 : print ">>> NUEVO ELEMETO [ID]\n"
							else:
								Tokens.append("< %s , %s >"%("ERROR LEXICO","Linea "+str(ListaTokens.count("cr")+1)+"- identificador mal formado"))
								ListaTokens.append("ERROR")
								print "ERROR LEXICO, Linea %s- identificador mal formado"%(str(ListaTokens.count("cr")+1))
							 	break
				elemt = ""
				#if salida == 1 : print ListaTokens

	contTS = 0
	if ListaTokens.count("ERROR") == 0 :
		Tokens.append("< %s , %s >"%( "FinFich", "eof" ))
		ListaTokens.append("eof")
		if salida == 1 : print "< %s , %s >\n"%("FinFich","eof")

	fichTokens = open('tokens_salida', 'a')
	for token in Tokens :
		fichTokens.write(str(token)+" \n")
	fichTokens.close()

	if ListaTokens.count("ERROR") != 0 :
		exit()

	#pprint.pprint(ListaTokens)
	#pprint.pprint(TSaux)
	#print Tokens
######################		  FIN ANALIZADOR LEXICO			######################

#print Tab*"\t"+"hola"
######################		INICIO ANALIZADOR SINTACTICO	######################
def	analizadorSintactico():
	P1()

# P' → P
def P1():
	global sal0, Tab, DicTS, ptrTS_actual, parseOrden
	parseOrden+="1 "

	#--Semantico Inicio
	ptrTS_actual = "TS_General"
	DicTS[ptrTS_actual] = [ [], 0, "null"]
	#--Semantico Fin

	#--Sintactico Inicio
	print Tab*"  "+"P’→ P" if sal0 == 0 else ""
	Tab+=1 if sal0 == 0 else 0
	P0()
	Tab-=1 if sal0 == 0 else 0
	#--Sintactico Fin

# P → B Z P | F Z P | Z P | eof
def P0():
	global contadorTokens, ListaTokens, sal0, Tab, parseOrden

	#--Sintactico Inicio
	if ListaTokens[contadorTokens] == "eof":
		print Tab*"  "+"P→ eof" if sal0 == 0 else ""
		parseOrden+="5 "
		ComprobarToken("eof")

	elif ListaTokens[contadorTokens] == "function":
		parseOrden+="3 "
		print Tab*"  "+"P→ FZP" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		F()
		Z0()
		P0()
		Tab-=1 if sal0 == 0 else 0
	elif ListaTokens[contadorTokens] == "cr":
		parseOrden+="4 "
		print Tab*"  "+"P→ ZP" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		Z0()
		P0()
		Tab-=1 if sal0 == 0 else 0
	else:
		parseOrden+="2 "
		print Tab*"  "+"P→ BZP" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		B0()
		Z0()
		P0()
		Tab-=1 if sal0 == 0 else 0
	#--Sintactico Fin

# Z → cr
def Z0():
	global contadorTokens, ListaTokens, sal0, Tab, contCr, parseOrden
	parseOrden+="6 "

	#--Sintactico Inicio
	print Tab*"  "+"Z → cr" if sal0 == 0 else ""
	ComprobarToken("cr")
	contCr+=1
	#--Sintactico Fin

# F → function H id (A) Z { Z C }
def F():
	global contadorTokens, ListaTokens, sal0, Tab, TSaux, contadorIds, DicTS, ptrTS_actual, parseOrden
	parseOrden+="7 "

	#--Sintactico Inicio
	print Tab*"  "+"F → function H id (A) Z { Z C }" if sal0 == 0 else ""
	Tab+=1 if sal0 == 0 else 0
	ComprobarToken("function")
	h=H() # h=[tipo,tamano]
	ComprobarToken("id")
	#--Sintactico Fin

	#--Semantico Inicio
	if buscarTS(TSaux[contadorIds]) != "null":
		Error_Sem("Función ya declarada")
	elif ptrTS_actual != "TS_General" :
		Error_Sin()
	else :
		insertarTS(TSaux[contadorIds], "function", DicTS[ptrTS_actual][1], ptrTS_actual)
		DicTS[ptrTS_actual][1]+=4
		ptrTS_anterior = ptrTS_actual
		ptrTS_actual = TSaux[contadorIds]
		DicTS[ptrTS_actual] = [ [], 0, ptrTS_anterior ] # Crea e inicializa la TS_nueva y Desp_nuevo
		contadorIds+=1
	#--Semantico Fin

	#--Sintactico Inicio
	ComprobarToken("(")
	a=A() # a=[tipo,numParam]
	ComprobarToken(")")
	Z0()
	ComprobarToken("{")
	#--Sintactico Fin

	#--Semantico Inicio
	insertarFunTS(ptrTS_anterior, ptrTS_actual, a[1],	a[0], h[0], ptrTS_anterior)
	#					...		,	id.ent 	, A.numParam, A.tipo, ptrTS_hijo)
	#--Semantico Fin

	#--Sintactico Inicio
	Z0()
	c=C()
	ComprobarToken("}")
	Tab-=1 if sal0 == 0 else 0
	#--Sintactico Fin

	#--Semantico Inicio
	if c[0] != h[0] and c[0] != "tipo_ok":
		Error_Sem("Funcion mal return c: "+str(c)+" h:"+str(h))
	else:
		ptrTS_actual  	= ptrTS_anterior
		ptrTS_anterior 	= "null"
	#--Semantico Fin

# H → T | 𝝺       // H tipo de retorno de la función
def H(): #h=[tipo,tamano]
	global contadorTokens, ListaTokens, sal0, Tab, parseOrden

	#--Sintactico Inicio
	la_T = str(ListaTokens[contadorTokens])
	if la_T == "int" or la_T == "bool" or la_T == "char" :
		parseOrden+="8 "
		print Tab*"  "+"H → T" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		t=T() #t=[tipo,tamano]
		Tab-=1 if sal0 == 0 else 0
	else:
		parseOrden+="9 "
		print Tab*"  "+"H → 𝝺" if sal0 == 0 else ""
		t=[ "tipo_vacio", 0 ] #t=[tipo,tamano]
	#--Sintactico Fin

	#--Semantico Inicio
	return t
	#--Semantico Fin

# T → int | bool | chars
def T(): #t=[tipo,tamano]
	global contadorTokens, ListaTokens, sal0, Tab, parseOrden

	#--Sintactico Inicio
	if ListaTokens[contadorTokens] == "int":
		parseOrden+="10 "
		print Tab*"  "+"T → int" if sal0 == 0 else ""
		ComprobarToken("int")

		#--Semantico Inicio
		return [ "entero", 2 ]
		#--Semantico Fin

	elif ListaTokens[contadorTokens] == "bool":
		parseOrden+="11 "
		print Tab*"  "+"T → bool" if sal0 == 0 else ""
		ComprobarToken("bool")

		#--Semantico Inicio
		return [ "logico", 1 ]
		#--Semantico Fin

	else:
		parseOrden+="12 "
		print Tab*"  "+"T → chars" if sal0 == 0 else ""
		ComprobarToken("chars")

		#--Semantico Inicio
		return [ "cadena", 2 ]
		#--Semantico Fin

	#--Sintactico Fin

# A → T id K | 𝝺
def A(): #A=[tipo,numParam]
	global contadorTokens, ListaTokens, sal0, Tab, TSaux, contadorIds, DicTS, ptrTS_actual, parseOrden

	#--Sintactico inicio
	la_T = str(ListaTokens[contadorTokens])
	if la_T == "int" or la_T == "bool" or la_T == "char" :
		parseOrden+="13 "
		print Tab*"  "+"A → T id K" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		t=T() #t=[tipo,tamano]
		ComprobarToken("id")
		#print ("id -->"+TSaux[contadorIds])

		#--Semantico Inicio
		if buscarId(TSaux[contadorIds], ptrTS_actual) != "null":
			Error_Sem("Identificador ya creado")
		else:
			insertarTS(TSaux[contadorIds], t[0], DicTS[ptrTS_actual][1], ptrTS_actual)
		 	DicTS[ptrTS_actual][1] += t[1]
		 	contadorIds+=1
		#--Semantico Fin

		k=K() #k=[tipo,numParam]
		Tab-=1 if sal0 == 0 else 0

		#--Semantico Inicio
		if k[0] != "tipo_vacio":
			tipo = str(t[0])+","+str(k[0])
		else:
			tipo = str(t[0])
		numParam = int(k[1]) + 1
		return [ tipo, numParam ]
		#--Semantico Fin

	else:
		parseOrden+="14 "
		print Tab*"  "+"A → 𝝺" if sal0 == 0 else ""

		#--Semantico Inicio
		tipo = "tipo_vacio"
		numParam = 0
		return [ tipo, numParam ]
		#--Semantico Fin

	#--Sintactico Fin

# K → , T id K | 𝝺
def K(): #k=[tipo,numParam]
	global contadorTokens, ListaTokens, sal0, Tab, TSaux, contadorIds, DicTS, ptrTS_actual, parseOrden

	#--Sintactico Inicio
	if ListaTokens[contadorTokens] == ",":
		parseOrden+="15 "
		print Tab*"  "+"K → , T id K" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		ComprobarToken(",")
		t=T() #t=[tipo,tamano]
		ComprobarToken("id")

		#--Semantico Inicio
		if buscarId(TSaux[contadorIds], ptrTS_actual) != "null":
			Error_Sem("Identificador ya creado")
		else:
			insertarTS(TSaux[contadorIds], t[0], DicTS[ptrTS_actual][1], ptrTS_actual)
		 	DicTS[ptrTS_actual][1] += t[1]
		 	contadorIds+=1
		#--Semantico Fin

		k=K() #k=[tipo,numParam]
		Tab-=1 if sal0 == 0 else 0

		#--Semantico Inicio
		if k[0] != "tipo_vacio":
			tipo = str(t[0])+","+str(k[0])
		else:
			tipo = str(t[0])
		numParam = int(k[1]) + 1
		return [ tipo, numParam ]
		#--Semantico Fin

	else:
		parseOrden+="16 "
		print Tab*"  "+"K → 𝝺" if sal0 == 0 else ""

		#--Semantico Inicio
		tipo = "tipo_vacio"
		numParam = 0
		return [ tipo, numParam ]
		#--Semantico Fin

	#--Sintactico Fin

# B → var T id | if (E) { Z C } Z B' | S // sentencias
def B0(): #b=[tipo]
	global contadorTokens, ListaTokens, sal0, Tab, TSaux, contadorIds, DicTS, ptrTS_actual, parseOrden

	#--Sintactico Inicio
	if ListaTokens[contadorTokens] == "var":
		parseOrden+="17 "
		print Tab*"  "+"B → var T id" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		ComprobarToken("var")
		t=T() #t=[tipo,tamano]
		ComprobarToken("id")
		Tab-=1 if sal0 == 0 else 0

		#--Semantico Inicio
		if buscarId(TSaux[contadorIds], ptrTS_actual) != "null" :
			Error_Sem("Identificador ya creado")
		else:
			insertarTS(TSaux[contadorIds], t[0], DicTS[ptrTS_actual][1], ptrTS_actual)
		 	DicTS[ptrTS_actual][1] += t[1]
		 	contadorIds+=1
		return ["tipo_ok"]
		#--Semantico Fin

	elif ListaTokens[contadorTokens] == "if":
		parseOrden+="18 "
		print Tab*"  "+"B → if (E) { Z C } B'" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		ComprobarToken("if")
		ComprobarToken("(")
		e=E0() #e=[tipo]
		ComprobarToken(")")

		#--Semantico Inicio
		if e[0] != "logico" :
			Error_Sem("condición \"if\" no logica")
		#--Semantico Fin

		ComprobarToken("{")
		Z0()
		c=C() #c=[tipo]
		ComprobarToken("}")
		b1=B1() #b1=[tipo]
		Tab-=1 if sal0 == 0 else 0

		#--Semantico Inicio
		if c[0] != "tipo_ok" and c[0] != "tipo_vacio": # b1 puede ser "tipo_vacio" o "tipo_ok"
			Error_Sem("contenido \"if\" mal formado c:" +str(c) )
		return ["tipo_ok"]
		#--Semantico Fin

	else:
		parseOrden+="19 "
		print Tab*"  "+"B → S" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		s=S0() #s=[tipo]
		Tab-=1 if sal0 == 0 else 0

		#--Semantico Inicio
		return s
		#--Semantico Fin

	#--Sintactico Fin

# B'→ else (E) { Z C } | 𝝺
def B1(): #b1=[tipo]
	global contadorTokens, ListaTokens, sal0, Tab, parseOrden

	#--Sintactico Inicio
	if ListaTokens[contadorTokens] == "else":
		parseOrden+="20 "
		print Tab*"  "+"B'→ else { Z C }" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		ComprobarToken("else")
		ComprobarToken("{")
		Z0()
		c=C() #c=[tipo]
		ComprobarToken("}")
		Tab-=1 if sal0 == 0 else 0

		#--Semantico Inicio
		if c[0] != "tipo_ok" :
			Error_Sem("contenido \"else\" mal formado")
		else :
			return ["tipo_ok"]
		#--Semantico Fin

	else:
		parseOrden+="21 "
		print Tab*"  "+"B' → 𝝺" if sal0 == 0 else ""

		#--Semantico Inicio
		return ["tipo_vacio"]
		#--Semantico Fin

	#--Sintactico Fin

# S → id S'| return X | write (E) | prompt (id)
def S0(): #s=[tipo]
	global contadorTokens, ListaTokens, sal0, Tab, TSaux, contadorIds, ptrTS_actual, parseOrden

	#--Sintactico Inicio
	if ListaTokens[contadorTokens] == "id":
		print Tab*"  "+"S → id S'" if sal0 == 0 else ""
		parseOrden+="22 "
		Tab+=1 if sal0 == 0 else 0
		ComprobarToken("id")
		auxID=TSaux[contadorIds]
		contadorIds += 1
		s1=S1() #s=[tipo]
		Tab-=1 if sal0 == 0 else 0

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

	elif ListaTokens[contadorTokens] == "return":
		parseOrden+="23 "
		print Tab*"  "+"S → return X" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		ComprobarToken("return")
		x=X() #x=[tipo]
		Tab-=1 if sal0 == 0 else 0

		#--Semantico Inicio
		return x
		#--Semantico Fin

	elif ListaTokens[contadorTokens] == "write":
		parseOrden+="24 "
		print Tab*"  "+"S → write (E)" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		ComprobarToken("write")
		ComprobarToken("(")
		e=E0() #e=[tipo]
		ComprobarToken(")")
		Tab-=1 if sal0 == 0 else 0

		#--Semantico Inicio
		return e
		#--Semantico Fin

	else:
		parseOrden+="25 "
		print Tab*"  "+"S → prompt (id)" if sal0 == 0 else ""
		ComprobarToken("prompt")
		ComprobarToken("(")
		ComprobarToken("id")
		ComprobarToken(")")

		#--Semantico Inicio
		if buscarTipoId(TSaux[contadorIds], ptrTS_actual) != "entero" or buscarTipoId(TSaux[contadorIds],ptrTS_actual) != "cadena" :
			Error_Sem("uso incorrecto de \"prompt\"")
		else :
			aux = buscarTipoId(TSaux[contadorIds], ptrTS_actual)
			contadorIds+=1
			return [ aux ]
		#--Semantico Fin

	#--Sintactico Fin

# S'→ (L) | = E
def S1(): #s1=[tipo]
	global contadorTokens, ListaTokens, sal0, Tab, parseOrden

	#--Sintactico Inicio
	if ListaTokens[contadorTokens] == "(":
		parseOrden+="26 "
		print Tab*"  "+"S'→ (L)" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		ComprobarToken("(")
		l=L() #l=[tipo]
		ComprobarToken(")")
		Tab-=1 if sal0 == 0 else 0

		#--Semantico Inicio
		return l
		#--Semantico Fin

	else:
		parseOrden+="27 "
		print Tab*"  "+"S'→ = E" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		ComprobarToken("=")
		e=E0() #e=[tipo]
		Tab-=1 if sal0 == 0 else 0

		#--Semantico Inicio
		return e
		#--Semantico Fin

	#--Sintactico Fin

# X → E | 𝝺
def X(): #x=[tipo]
	global contadorTokens, ListaTokens, sal0, Tab, parseOrden

	#--Sintactico Inicio
	la_E = str(ListaTokens[contadorTokens])
	if la_E == "id" or la_E == "(" or la_E == "entero" or la_E == "cadena" or la_E == "True" or la_E == "False":
		parseOrden+="28 "
		print Tab*"  "+"X → E" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		e=E0() #e=[tipo]
		Tab-=1 if sal0 == 0 else 0

		#--Semantico Inicio
		return e
		#--Semantico Fin

	else:
		parseOrden+="29 "
		print Tab*"  "+"X → 𝝺" if sal0 == 0 else ""

		#--Semantico Inicio
		return["tipo_vacio"]
		#--Semantico Fin

	#--Sintactico Fin

# C → B Z C | 𝝺       // cuerpo de la función
def C(): #c=[tipo]
	global contadorTokens, ListaTokens, sal0, Tab, parseOrden

	#--Sintactico Inicio
	la_B = str(ListaTokens[contadorTokens])
	if la_B == "var" or la_B == "if" or la_B == "id" or la_B == "return" or la_B == "write" or la_B == "prompt":
		parseOrden+="30 "
		print Tab*"  "+"C → B Z C" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		b=B0() #b=[tipo]
		Z0()
		c=C() #c=[tipo]
		Tab-=1 if sal0 == 0 else 0

		#--Semantico Inicio
		if c[0] != "tipo_error" and b[0] != "tipo_error":
			return ["tipo_ok"]
		else:
			Error_Sem("contenido de corchetes mal formado")
		#--Semantico Fin

	else:
		parseOrden+="31 "
		print Tab*"  "+"C → 𝝺" if sal0 == 0 else ""

		#--Semantico Inicio
		return ["tipo_vacio"]
		#--Semantico Fin

	#--Sintactico Fin

# L → E Q | 𝝺
def L(): #l=[tipo]
	global contadorTokens, ListaTokens, sal0, Tab, parseOrden

	#--Sintactico Inicio
	la_E = str(ListaTokens[contadorTokens])
	if la_E == "id" or la_E == "(" or la_E == "entero" or la_E == "cadena" or la_E == "True" or la_E == "False":
		parseOrden+="32 "
		print Tab*"  "+"L → E Q" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		e=E0() #e=[tipo]
		q=Q() #q=[tipo]
		Tab-=1 if sal0 == 0 else 0

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
		parseOrden+="33 "
		print Tab*"  "+"L → 𝝺" if sal0 == 0 else ""

		#--Semantico Inicio
		return ["tipo_vacio"]
		#--Semantico Fin

	#--Sintactico Fin

# Q → , E Q | 𝝺
def Q(): #q=[tipo]
	global contadorTokens, ListaTokens, sal0, Tab, parseOrden

	#--Sintactico Inicio
	if ListaTokens[contadorTokens] == ",":
		parseOrden+="34 "
		print Tab*"  "+"Q → , E Q" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		ComprobarToken(",")
		e=E0() #e=[tipo]
		q=Q() #q=[tipo]
		Tab-=1 if sal0 == 0 else 0

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
		parseOrden+="35 "
		print Tab*"  "+"Q → 𝝺" if sal0 == 0 else ""

		#--Semantico Inicio
		return ["tipo_vacio"]
		#--Semantico Fin

	#--Sintactico Fin

# E → R E'
def E0(): #e=[tipo]
	global contadorTokens, ListaTokens, sal0, Tab, parseOrden
	parseOrden+="36 "

	#--Sintactico Inicio
	print Tab*"  "+"E → R E'" if sal0 == 0 else ""
	Tab+=1 if sal0 == 0 else 0
	r=R0() #r=[tipo]
	e1=E1() #e1=[tipo]
	Tab-=1 if sal0 == 0 else 0
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

# E'→ && R E' | &= R E' | 𝝺
def E1(): #e1=[tipo]
	global contadorTokens, ListaTokens, sal0, Tab, parseOrden

	#--Sintactico Inicio
	if ListaTokens[contadorTokens] == "&&":
		parseOrden+="37 "
		print Tab*"  "+"E'→ && R E'" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		ComprobarToken("&&")
		r=R0() #r=[tipo]
		e1=E1() #e1=[tipo]
		Tab-=1 if sal0 == 0 else 0

		#--Semantico Inicio
		if e1[0] != "tipo_vacio" and e1[0] != r[0] != "logico":
			Error_Sem("Comparacion de elementos de tipo no logico")
		else :
			return r
		#--Semantico Fin

	elif ListaTokens[contadorTokens] == "&=":
		parseOrden+="38 "
		print Tab*"  "+"E'→ &= R E'" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		ComprobarToken("&=")
		r=R0() #r=[tipo]
		e1=E1() #e1=[tipo]
		Tab-=1 if sal0 == 0 else 0

		#--Semantico Inicio
		if e1[0] != "tipo_vacio" and e1[0] != r[0] != "logico":
			Error_Sem("Comparacion de elementos de tipo no logico")
		else :
			return r
		#--Semantico Fin

	else:
		parseOrden+="39 "
		print Tab*"  "+"E' → 𝝺" if sal0 == 0 else ""

		#--Semantico Inicio
		return["tipo_vacio"]
		#--Semantico Fin

	#--Sintactico Fin

# R → U R'
def R0(): #r=[tipo]
	global contadorTokens, ListaTokens, sal0, Tab, parseOrden
	parseOrden+="40 "

	#--Sintactico Inicio
	print Tab*"  "+"R → U R'" if sal0 == 0 else ""
	Tab+=1 if sal0 == 0 else 0
	u=U0() #u=[tipo]
	r1=R1()	#r1=[tipo]
	Tab-=1 if sal0 == 0 else 0
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
	global contadorTokens, ListaTokens, sal0, Tab, parseOrden

	#--Sintactico Inicio
	if ListaTokens[contadorTokens] == ">":
		parseOrden+="41 "
		print Tab*"  "+"R'→ > U R'" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		ComprobarToken(">")
		u=U0() #u=[tipo]
		r1=R1()	#r1=[tipo]
		Tab-=1 if sal0 == 0 else 0

		#--Semantico Inicio
		if r1[0] != "tipo_vacio" and r1[0] != u[0] != "entero" :
			Error_Sem("Comparacion de elementos de tipo no entero")
		else :
			return u
		#--Semantico Fin

	else:
		parseOrden+="42 "
		print Tab*"  "+"R' → 𝝺" if sal0 == 0 else ""

		#--Semantico Inicio
		return ["tipo_vacio"]
		#--Semantico Fin

	#--Sintactico Fin

# U → V U'
def U0(): #u=[tipo]
	global contadorTokens, ListaTokens, sal0, Tab, parseOrden
	parseOrden+="43 "

	#--Sintactico Inicio
	print Tab*"  "+"U → V U'" if sal0 == 0 else ""
	Tab+=1 if sal0 == 0 else 0
	v=V0() #v=[tipo]
	u1=U1()	#ui=[tipo]
	Tab-=1 if sal0 == 0 else 0
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
	global contadorTokens, ListaTokens, sal0, Tab, parseOrden

	#--Sintactico Inicio
	if ListaTokens[contadorTokens] == "+" :
		parseOrden+="44 "
		print Tab*"  "+"U'→ + V U'" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		ComprobarToken("+")
		v=V0() #v=[tipo]
		u1=U1()	#ui=[tipo]
		Tab-=1 if sal0 == 0 else 0

		#--Semantico Inicio
		if v[0] != "entero" :
			Error_Sem("Suma de elementos de tipo no entero")
		else :
			return v
		#--Semantico Fin

	else:
		print Tab*"  "+"U' → 𝝺" if sal0 == 0 else ""
		parseOrden+="45 "

		#--Semantico Inicio
		return ["tipo_vacio"]
		#--Semantico Fin

	#--Sintactico Fin

# V → id V' | (E) | entero | cadena | True | False
def V0(): #v=[tipo] or v=[tipo, numParam]
	global contadorTokens, ListaTokens, sal0, Tab, TSaux, contadorIds, parseOrden

	#--Sintactico Inicio
	if ListaTokens[contadorTokens] == "id" :
		parseOrden+="46 "
		print Tab*"  "+"V → id V'" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		ComprobarToken("id")
		auxID=TSaux[contadorIds]
		contadorIds+=1
		v1=V1() #v1=[tipo]
		Tab-=1 if sal0 == 0 else 0

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

	elif ListaTokens[contadorTokens] == "(" :
		parseOrden+="47 "
		print Tab*"  "+"V → (E)" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		ComprobarToken("(")
		e=E0() #e=[tipo]
		ComprobarToken(")")
		Tab-=1 if sal0 == 0 else 0

		#--Semantico Inicio
		return e
		#--Semantico Fin

	elif ListaTokens[contadorTokens] == "entero" :
		parseOrden+="48 "
		print Tab*"  "+"V → entero" if sal0 == 0 else ""
		ComprobarToken("entero")

		#--Semantico Inicio
		return["entero"]
		#--Semantico Fin

	elif ListaTokens[contadorTokens] == "cadena" :
		parseOrden+="49 "
		print Tab*"  "+"V → cadena" if sal0 == 0 else ""
		ComprobarToken("cadena")

		#--Semantico Inicio
		return["cadena"]
		#--Semantico Fin

	elif ListaTokens[contadorTokens] == "True" :
		parseOrden+="50 "
		print Tab*"  "+"V → True" if sal0 == 0 else ""
		ComprobarToken("True")

		#--Semantico Inicio
		return ["logico"]
		#--Semantico Fin

	else:
		parseOrden+="51 "
		print Tab*"  "+"V → False" if sal0 == 0 else ""
		ComprobarToken("False")

		#--Semantico Inicio
		return ["logico"]
		#--Semantico Fin

	#--Sintactico Fin

# V'→ (L) | 𝝺
def V1(): #v1=[tipo] o v1=[tipo,numParam]
	global contadorTokens, ListaTokens, sal0, Tab, parseOrden

	#--Sintactico Inicio
	if ListaTokens[contadorTokens] == "(" :
		parseOrden+="52 "
		print Tab*"  "+"V'→ (L)" if sal0 == 0 else ""
		Tab+=1 if sal0 == 0 else 0
		ComprobarToken("(")
		l=L() #l=[tipo]
		ComprobarToken(")")
		Tab-=1 if sal0 == 0 else 0

		#--Semantico Inicio
		return l
		#--Semantico Fin

	else:
		parseOrden+="53 "
		print Tab*"  "+"V'→ 𝝺" if sal0 == 0 else ""

		#--Semantico Inicio
		return ["tipo_vacio"]
		#--Semantico Fin

	#--Sintactico Fin

def Error_Sin():
	global contadorTokens, ListaTokens, contCr
	print "ERROR Sintactico --> Token_Actual : "+ str(ListaTokens[contadorTokens])+ " en linea :" +str(contCr)
	imprimirTS()
	parse()
	exit()

def ComprobarToken(T):
	global contadorTokens, ListaTokens, sal1, TSaux, contadorIds
	if ListaTokens[contadorTokens] == str(T):
		print "TERMINAL --> "+str(ListaTokens[contadorTokens]) if sal1 == 0 else ""
		if str(T) == "id" :
			print " ID --> "+TSaux[contadorIds] if sal1 == 0 else ""
		contadorTokens += 1
	else:
		Error_Sin()

def Error_Sem(txt):
	global contCr
	print str("ERROR Semantico --> "+txt +", en linea: "+ str(contCr))
	imprimirTS()
	parse()
	exit()

def imprimirTS():
	global DicTS
	salidaTS = ""
	for i in DicTS:
		salidaTS+="CONTENIDO DE LA TABLA # "+str(i)+" :\n\n"
		for n in DicTS[i][0]:
			salidaTS+= "* LEXEMA : "+ n[1]+ "\n"
	  		salidaTS+= "  ATRIBUTOS :\n"
	  		salidaTS+= "  + tipo : "+ n[2]+ "\n"
	  		salidaTS+= "  + desplazamiento : "+ n[3]+ "\n"
	  		salidaTS+= "  + Tam_parametros : "+ n[4]+ "\n"
	  		salidaTS+= "  + Tipo_parametro : "+ n[5]+ "\n"
	  		salidaTS+= "  + Retorno_funcion : "+ n[6]+ "\n"
	  		salidaTS+= "  + ptrTS_padre : "+ n[7]+ "\n"
	  		salidaTS+= "--------- ----------\n"
	  	salidaTS+="================================================\n"
	fichTokens = open('Tabla_de_Simbolo', 'a')
	fichTokens.write(str(salidaTS))
	fichTokens.close()

def parse():
	global parseOrden
	fichTokens = open('Parse_Descendente', 'a')
	fichTokens.write("Des "+str(parseOrden))
	fichTokens.close()

######################		  FIN ANALIZADOR SINTACTICO		######################

def main():
	print (50*"-")+"\n"
	analizadorLexico ()
	analizadorSintactico()
	imprimirTS()
	parse()
	print (50*"-")+"\n"

if __name__ == "__main__":
    main()

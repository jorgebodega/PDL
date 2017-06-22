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
#    config = yaml.load(f)


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

######################        INICIO ANALIZADOR LEXICO        ######################
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
######################          FIN ANALIZADOR LEXICO            ######################

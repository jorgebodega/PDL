#Proyecto PDL en Python (PL-51)

Nuestro grupo, el grupo PL-51 tiene asignadas: la sentencia condicional compuesta if, if-else, 
el operador especial asignación con y lógico (&=) y la técnica de Análisis Sintáctico Descendente Recursivo.

## Descripción del diseño del Procesador

### El contenido del lenguaje, se divide en varias partes

+ __Comentarios__: Tenemos dos tipos de comentarios, /* ... */ y // ... . En nuestro
caso, hemos implementado ambos.

+ __Constantes__: Enteros, cadenas de caracteres y lógicas. En el caso de los enteros,
son los números enteros naturales comprendidos entre 0 y 32767. Las cadenas de
caracteres vienen delimitadas por “...”. Para las constantes lógicas, se han
implementado las palabras reservadas True y False.

+ __Operadores__: Aritméticos, de relación, lógicos, y de asignación. En nuestro caso,
hemos implementado la suma (A + B) para el operador aritmético, mayor (A > B)
para el operador de relación, operación AND (A && B) para el operador lógico,
operación AND con asignación (A &= B), como operador asignado; y la
asignación (=) como operador de asignación.

+ __Identificadores__: Los identificadores están formados por cualquier cantidad de
letras, dígitos, siendo siempre el primero una letra.

+ __Declaraciones__: El lenguaje utilizado, JavaScript-PL no exige que todas las
variables estén declaradas. Si se usa una variable que no ha sido declarada
anteriormente, se considera que esa variable es global y entera. Si se declara una
variable, tendrá que ser de la forma “var T id”, siendo T el tipo de variable (entera,
lógica o cadena). 

+ __Tipos de Datos__: Para la realización de la práctica ha considerado sólo la
existencia de tres tipos de datos: entero (int), cadena (chars) y lógico (bool). El
lenguaje no tiene conversiones automáticas entre tipos, es decir, no podemos
hacer castings.

+ __Instrucciones de Entrada/Salida__: La sentencia write (expresión) evalúa la
expresión e imprime el resultado por la pantalla. La sentencia prompt (var) lee un
número o una cadena del teclado y lo almacena en la variable var, que tiene que
ser de tipo entero o cadena.

+ __Sentencias__: Hay distintos tipos de sentencias en nuestra práctica, sentencia de
asignación, sentencia de llamada a una función, sentencia de retorno de una
función, sentencia condicional compuesta y simple, sentencia de selección
múltiple, sentencia de asignación, etc. A nuestro grupo nos fue asignado la
sentencia condicional compuesta, además de la de asignación con condición
lógica (&=).

+ __Funciones__: Se define indicando la palabra “function”, el tipo de retorno (en el
caso de que devuelve algo), el nombre de la función y los argumentos con sus
tipos entre paréntesis en el caso que haya argumentos. El cuerpo de la función va
delimitado entre llaves.


## Diseño del Analizador Léxico

### Tokens

El formato de los tokens será del* < código del* , del* [atributo] del* > del* RE, donde
del* será cualquier cantidad de espacios en blanco, tabuladores o vacío. El código indica
el código del token correspondiente, con el siguientes formato: (l|d) , que son los
caracteres alfanuméricos, habiendo al menos uno. El atributo es el atributo opcional del
token que corresponde, que puede tener un formato cualquiera de los siguientes: un
nombre, (l|d) caracteres alfanuméricos, habiendo al menos uno; un número: [+|-]d que
implica un número entero con signo opcional, o una cadena "c " que es una cadena de
caracteres no vacía. RE puede implicar un salto de línea (CR - Carriage Return) o un fin
de fichero (EOF - End Of File).

Los tokens que reconoce nuestro analizador léxico son:

	"< IniPar, ( >"		: Inicio de paréntesis
	"< FinPar, ) >"		: Fin de paréntesis
	"< IniLla, { >"		: Inicio de llaves
	"< FinLla, } >"		: Fin de llaves
	"< cr, - >"		: Salto de línea
	"< id, lexema >"	: Identificador
	"< PalRes, bool >"	: Palabra reservada bool
	"< PalRes, chars >"	: Palabra reservada chars
	"< PalRes, function >"	: Palabra reservada function
	"< PalRes, if >" 	: Palabra reservada if
	"< PalRes, else >" 	: Palabra reservada else
	"< PalRes, int >"	: Palabra reservada int
	"< PalRes, prompt >"	: Palabra reservada prompt
	"< PalRes, return >"	: Palabra reservada return
	"< PalRes, write >"	: Palabra reservada write
	"< PalRes, True >"	: Palabra reservada true
	"< PalRes, False >"	: Palabra reservada false
	"< PalRes, var >"	: Palabra reservada var
	"< Coma, “,” >"		: Coma
	"< OpAsi, “=” >"	: Operador asignación
	"< OpLogico, “&&” >"	: Operador lógico AND
	"< OpEspcial, “&=” >"	: Operador especial asignación con y lógico
	"< OpNum, “>” >"	: Operador relacional MAYOR
	"< Sum, "+" >"		: Suma
	"< FinFich, eof >"	: Fin de fichero
	"< entero, valor >"	: Número con un valor
	"< cadena, texto >"	: Cadena con un texto

### Gramática

A continuación, encontramos la gramática:

coc: Cualquier otro carácter.
l: Letra.
d:Dígito.

	S → del S | ( | ) | { | } | , | = | &A | > | + | “B | cr | eof | dC | lD | /E
	A → & | =
	B → cocB | “
	C → dC | λ
	D → lD | dD | λ
	E → *F | /I
	F → coc F | *H
	H → coc F | /
	I → coc I | cr


## Diseño del Analizador Sintáctico

### Gramática

Para que la gramática sea válida para nuestro Analizador Sintáctico Descendente
Recursivo Predictivo, deberemos comprobar que no es recursiva por la izquierda, y
deberá estar factorizada. Una vez que cumpla dichos requisitos, procederemos a
comprobar los conflictos.
La gramática en cuestión es la siguiente:

	P' → P
	P → B Z P | F Z P | Z P | eof
	Z → cr
	F → function H id (A) Z { Z C }
	H → T | λ
	T → int | bool | chars
	A → T id K | λ
	K → , T id K | λ
	B → var T id | if (E) { Z C } B' | S // sentencias
	B'→ else { Z C } | λ
	S → id S'| return X | write (E) | prompt (id)
	S'→ (L) | = E
	X → E | λ
	C → B Z C | λ // cuerpo de la función
	L → E Q | λ
	Q → , E Q | λ
	E → R E'
	E'→ && R E' | &= R E' | λ
	R → U R'
	R'→ > U R'| λ
	U → V U'
	U'→ + V U' | λ
	V → id V' | (E) | entero | cadena | True | False
	V'→ (L) | λ

Para la resolución de nuestro ejercicio hemos diseñado la siguiente gramática que
contempla todos los casos posibles. Hemos encontrado recursividad por la izquierda en
los siguientes casos:

	E → E && R | E &= R | R
	R → R > U | U
	U → U + V | V

Al eliminar la recursividad por la izquierda, quedaría de la siguiente forma:

	E → R E'
	E'→ && R E' | &= R E' | λ
	R → U R'
	R'→ > U R'| λ
	U → V U'
	U'→ + V U' | λ

### First

A continuación, indicamos los Firsts de la gramática:

	First (P’) = {var, if, return, write, prompt, id, function, cr, eof}
	First (P) = {var, if, return, write, prompt, id, function, cr, eof}
	First (Z) = {cr}
	First (F) = {function}
	First (H) = {int, bool, chars, λ}
	First (T) = {int, bool, chars}
	First (A) = {int, bool, chars, λ}
	First (K) = {“,”, λ}
	First (B) = {var, if, return, write, prompt, id}
	First (B’) = {else, λ}
	First (S) = {return, write, prompt, id}
	First (S’) = {(, =}
	First (X) = {(, id, entero, cadena, True, False, λ}
	First (C) = { var, if, return, write, prompt, id, λ}
	First (L) = {(, id, entero, cadena, True, False, λ}
	First (Q) = {“,”, λ}
	First (E) = {(, id, entero, cadena, True, False}
	First (E’) = {&&, &=, λ}
	First (R) = {(, id, entero, cadena, True, False}
	First (R’) = {>, λ}
	First (U) = {(, id, entero, cadena, True, False}
	First (U’) = {+, λ}
	First (V) = {(, id, entero, cadena, True, False}
	First (V’) = {(, λ}

### Follow

A continuación, indicamos los Follow de la gramática:

	Follow (P’) = {$}
	Follow (P) = {$}
	Follow (Z) = {var, if, id, return, write, prompt, function, cr, eof, “}”, else }
	Follow (F) = {cr}
	Follow (H) = {id}
	Follow (T) = {id}
	Follow (A) = {“)”}
	Follow (K) = {“)”}
	Follow (B) = {cr}
	Follow (B’) = {cr}
	Follow (S) = {cr}
	Follow (S’) = {cr}	
	Follow (X) = {cr}
	Follow (C) = {cr}
	Follow (L) = {cr}
	Follow (Q) = {cr}
	Follow (E) = {“)”, cr, “,”}
	Follow (E’) = {“)”, cr, “,”}
	Follow (R) = {&&, &=, “)”, cr, “,”}
	Follow (R’) = {&&, &=, “)”, cr, “,”}
	Follow (U) = {>, &&, &=, “)”, cr, “,”}
	Follow (U’) = {>, &&, &=, “)”, cr, “,”}
	Follow (V) = {+, >, &&, &=, “)”, cr, “,”}
	Follow (V’) = {+, >, &&, &=, “)”, cr, “,”}

### Conflictos

Estudiaremos si existen conflictos en la gramática descrita en al inicio de este apartado:

	P → First (B) ∩ First (F) ∩ First (Z) ∩ eof =
	= {var, if, return, write, prompt, id} ∩ {function} ∩ {cr} ∩ eof = ø

	H → First (T) ∩ Follow (H) = {int, bool, chars} ∩ {id} = ø
	A → First (T) ∩ Follow (A) = {int, bool, chars} ∩ {“)”} = ø
	K → “,” ∩ Follow (K) = “,” ∩ {“)”} = ø
	B → var ∩ if ∩ First (S) = var ∩ if ∩ {return, write, prompt, id} = ø
	B’ → else ∩ Follow (B’) = else ∩ {cr} = ø
	S → id ∩ return ∩ write ∩ prompt = ø
	S’ → “(“ ∩ “=“ = ø
	T → int ∩ chars ∩ bool = ø
	X → First (E) ∩ Follow (X) = {(, id, entero, cadena, True, False} ∩ {cr} = ø
	C → First (B) ∩ Follow (C) = {var, if, return, write, prompt, id} ∩ {cr} = ø
	L → First (E) ∩ Follow (L) = {(, id, entero, cadena, True, False} ∩ {cr} = ø
	Q → “,” ∩ Follow (Q) = “,” ∩ {cr} = ø
	E’→ && ∩ &= ∩ Follow (E’) = && ∩ &= ∩ {“)”, cr, “,”} = ø
	R’→ > ∩ Follow (R’) = > ∩ {&&, &=, “)”, cr, “,”} = ø
	U’→ + ∩ Follow (U’) = + ∩ {>, &&, &=, “)”, cr, “,”} = ø
	V→ id ∩ “(“ ∩ entero ∩ cadena ∩ True ∩ False = ø
	V’→ “(“ ∩ Follow (V’) = “(“ ∩ {+, >, &&, &=, “)”, cr, “,”} = ø

## Diseño del Analizador Semántico

buscarTS => busca si existe TS en DicTS, si no devuelve null

buscarId => busca si exixte el id en la TS actual, en caso contrario devuelve null

buscarTipoId => busca si existe el id en la TS actual y devuelve su tipo, si no existe
devuelve null

buscarTipoFuncion => busca si existe el id en la TS actual y es de tipo "function" y
devuelve la salida de la funcion, si no existe, o no es funcion, devuelve null

buscarTipoParametrosFuncion => busca si existe el id en la TS actual y es de tipo
"function" y devuelve el tipo de parametros que se le pasa, si no existe, o no es funcion,
devuelve null

insertarTS => inserta un id en la TS actual

insertarFunTs => inserta los parametros de una funcion dado un ptrTS valido

	P' →
	{{
	ptrTS_actual = "TS_General"
	DicTS[ptrTS_actual] = [ [], 0, "null"] // (TS,Desp,TS_padre)
	}}
	P
	{{
	TS_actual = "null"
	}}

	P → B Z P ( No hace nada)

	P → F Z P ( No hace nada)

	P → Z P ( No hace nada)

	P → eof ( No hace nada)

	Z → cr ( No hace nada)

	F → function H id
	{{
	if buscarTS(id.ent) ≠ null
		Then Error (“Función ya declarada”)
	else
		insertarTS(id.ent, "function", Desp_actual, ptrTS_actual)
		DicTS[ptrTS_actual] := (TS_actual,Desp_actual) // guarda la TS actual
		con el desplazamiento
		crearTS TS_nueva
		TS_actual := TS_nueva
		Desp_actual := 0
		ptrTS_anterior := ptrTS_actual
		ptrTS_actual := id.ent
	}}
	(A) Z {
	{{
	insertarFunTS(ptrTS_anterio, id.ent, A.numParam, A.tipo, id.ent)
	}}
	Z C }
	{{
	if C.tipo ≠ H.tipo or C.tipo ≠ tipo_ok
		Then Error (“Funcion mal return”)
	else
		Then
		DicTS[ptrTS_actual] := (TS_actual,Desp_actual) // guarda la TS actual con el desplazamiento
		DicTS[ptrTS_anterior] := (TS_anterior,Desp_anterior) // recuperamos la tabla de simbolos anterior 
		TS_actual := TS_anterior
		Desp_actual := Desp_anterior
		ptrTS_actual := ptrTS_anterio
		ptrTS_anterio := null
	}}

	H → T
	 {{ H.tipo = T.tipo , H.tamano = T.tamano }}

	H → λ
	{{ H.tipo = tipo_vacio , H.tamano = 0 }}

	T → int
	{{ T.tipo = entero , T.tamano = 2 }}	

	T → bool
	{{ T.tipo = logico , T.tamano = 1 }}

	T → chars
	{{ T.tipo = cadena , T.tamano = 2 }}

	A → T id
	{{
	if buscarId(id.ent) ≠ null
		Then Error (“Identificador ya creado”)
	else
		Then
		insertarTS(id.ent, T.tipo, Desp_actual, ptrTS_actual)
		Desp_actual += T.tamano
	}}
	K
	{{
	if K.tipo == “tipo_vacio”
		Then A.tipo := T.tipo
	else
		Then
		A.tipo := f(T.tipo, K.tipo)
		A.numParam := K.numParam + 1
	}}
	
	A → λ
	{{
	A.tipo = tipo_vacio
	A.numParam := 0
	}}

	K0 → , T id
	{{
	if buscarId(id.ent) ≠ null
		Then Error (“Identificador ya creado”)
	else
		Then
		insertarTS(id.ent, T.tipo, Desp_actual, ptrTS_actual)
		Desp_actual += T.tamano
	}}
	K1
	{{
	if K1.tipo == “tipo_vacio”
		Then K0.tipo := T.tipo
	else
		Then
		K0.tipo := f(T.tipo, K1.tipo)
		K0.numParam := K1.numParam + 1
	}}

	K → λ
	{{
	K.tipo = tipo_vacio
	K.numParam := 0
	}}

	B → var T id
	{{
	if buscarId(id.ent) ≠ null
		Then Error (“Identificador ya creado”)
	else
		Then
		insertarTS(id.ent, T.tipo, Desp_actual, ptrTS_actual)
		Desp_actual += T.tamano
		B.tipo := tipo_ok
	}}

	B → if (E)
	{{
	if E.tipo == logico
		Then B.tipo := tipo_ok
	else
		Then Error (“condición "if" no logica”)
	}}
	{ Z C } B'
	{{
	if C.tipo ≠ tipo_ok and C.tipo ≠ tipo_vacio
		Then Error (“contenido "if" mal formado”)
	}}

	B → S
	{{
	B.tipo := S.tipo
	}}

	B'→ else { Z C }
	{{
	if C.tipo ≠ tipo_ok
		Then Error (“contenido "else" mal formado”)
	else
		Then B'.tipo := tipo_ok
	}}

	B'→ λ
	{{
	B'.tipo := tipo_vacio
	}}

	S → id S'
	{{
	if buscarTipoId(id.ent) ≠ null
		Then 
		if buscarTipoFuncion(id.ent, ptrTS_actual) ≠ null
			Then 
			if buscarTipoParametrosFuncion(id.ent, ptrTS_actual) == S’.tipo:
				Then S.tipo := buscarTipoFuncion(id.ent, ptrTS_actual)
			else:
			Then Error_Sem()
		else:
			Then
			if buscarTipoId(id.ent, ptrTS_actual) == S’.tipo :
				Then S.tipo := tipo_ok
			else:
				Then Error_Sem()
	else:
		Then
		insertarTS( id.ent, "entero" , DicTS["TS_General"][1], "TS_General") 
		DicTS["TS_General"][1] += 2
		if "entero" == S’.tipo :
			S.tipo:= tipo_ok
		else:
			Error_Sem()
	}}

	S → return X
	{{
	S.tipo := X.tipo
	}}

	S → write (E)
	{{
	S.tipo := E.tipo
	}}

	S → prompt (id)
	{{
	if buscarTipoId(id.ent) ≠ "entero" or buscarTipoId(id.ent) ≠ "cadena"
		Then Error (“uso incorrecto de "prompt" ”)
	else
		Then S.tipo:= buscarTipoId(id.ent)
	}}

	S'→ (L)
	{{
	S'.tipo:= L.tipo
	}}

	S'→ = E
	{{
	S'.tipo := E.tipo
	}}


	X → E
	{{
	X.tipo := E.tipo
	}}

	X → λ
	{{
	X.tipo := tipo_vacio
	}}

	C0 → B Z C1
	{{
	if C1.tipo ≠ tipo_error and B.tipo ≠ tipo_error
		Then C0.tipo := tipo_ok
	else
		Then Error (“contenido de corchetes mal formado”)
	}}

	C → λ
	{{
	C.tipo := tipo_vacio
	}}

	L → E Q
	{{
	if E.tipo ≠ tipo_error and Q.tipo ≠ tipo_error
		Then L.tipo:= f(E.tipo,Q.tipo)
	else
		Then Error (“contenido parentesis del identificador llamado mal formado”)
	}}
	
	L → λ
	{{
	L.tipo := tipo_vacio
	}}

	Q0 → , E Q1
	{{
	if E.tipo ≠ tipo_error and Q1.tipo ≠ tipo_error
		Then Q0.tipo:= f(E.tipo,Q.tipo)
	else
		Then Error (“contenido parentesis del identificador llamado mal formado”)
	}}

	Q → λ
	{{
	Q.tipo := tipo_vacio
	}}

	E → R E'
	{{
	if E'.tipo ≠ tipo_vacio and R.tipo ≠ E'.tipo
		Then Error (“Comparacion de elementos con tipos distintos”)
	else
		Then
		if E'.tipo ≠ tipo_vacio
			Then E.tipo := "logico"
		else
			Then E.tipo := R.tipo
	}}

	E'0→ && R E'1
	{{
	if E'1.tipo ≠ tipo_vacio and E'1.tipo ≠ R.tipo ≠ "logico"
		Then Error (“Comparacion de elementos de tipo no logico”)
	else
		Then E'0.tipo := R.tipo
	}}

	E'0→ &= R E'1
	{{
	if E'1.tipo ≠ tipo_vacio and E'1.tipo ≠ R.tipo ≠ "logico"
		Then Error (“Comparacion de elementos con asignacion de tipo no logico”)
	else
		Then E'0.tipo := R.tipo
	}}

	E'→ λ
	{{
	E'.tipo := tipo_vacio
	}}

	R → U R'
	{{
	if R'.tipo ≠ tipo_vacio and U.tipo ≠ R'.tipo
		Then Error (“Comparacion de elementos con tipos distintos”)
	else
		Then
		if R'.tipo ≠ tipo_vacio
			Then R.tipo := "logico"
		else
			Then R.tipo := U.tipo
	}}

	R'0→ > U R'1
	{{
	if R'1.tipo ≠ tipo_vacio and R'1.tipo ≠ U.tipo ≠ "entero"
		Then Error (“Comparacion de elementos de tipo no entero”)
	else
		Then R'0.tipo := U.tipo
	}}

	R'→ λ
	{{
	R'.tipo := tipo_vacio
	}}

	U → V U'
	{{
	if U'.tipo ≠ tipo_vacio and V.tipo ≠ U'.tipo
		Then Error (“Suma de elementos de tipo no entero”)
	else
		Then U.tipo := V.tipo
	}}

	U'0→ + V U'1
	{{
	if V.tipo ≠ "entero"
		Then Error (“Suma de elementos de tipo no entero”)
	else
		Then U'0.tipo := V.tipo
	}}

	U'→ λ
	{{
	U'.tipo := tipo_vacio
	}}


	V → id V'
	{{
	if buscarTipoId(id.ent, ptrTS_actual) ≠ null
		Then
		if buscarTipoFuncion(id.ent, ptrTS_actual) ≠ null
			Then
			if uscarTipoParametrosFuncion (id.ent, ptrTS_actual) == V'.tipo
				Then V.tipo := buscarTipoFuncion(id.ent, ptrTS_actual)
			else
				Then Error (“Parametros mal insertados”)
		else
			Then V.tipo := buscarTipoId(id.ent)
	else
		Then
		insertarTS( id.ent, "entero" , DicTS["TS_General"][1], "TS_General")
		DicTS["TS_General"][1] += 2
		V.tipo := entero
	}}

	V → (E)
	{{ V.tipo := E.tipo }}

	V → entero
	{{ V.tipo := entero }}

	V → cadena
	{{ V.tipo := cadena }}

	V → True
	{{ V.tipo := logico }}

	V → False
	{{ V.tipo := logico }}

	V'→ (L)
	{{
	V'.tipo := L.tipo
	}}

	V'→ λ
	{{
	V'.tipo := tipo_vacio
	}}

## Diseño de la Tabla de Símbolos

Ejemplo valido:

	CONTENIDO DE LA TABLA # 1 :
	* LEXEMA : 'apellidos2'
	ATRIBUTOS :
	+ tipo : (esto es de tipo cadena) 'string'
	+ desplazamiento : 16
	--------- ----------
	* LEXEMA : 'valido#'
	ATRIBUTOS :
	+ tipo : 'bool' (lógico)
	+ desplazamiento : 48
	--------- ----------
	* 'nombre'
	+ tipo : 'string'
	+ desplazamiento : 0



// Probamos algunas palabras reservadas

var String a;
var bool b;
var int c;

function String funcion1 () {
    global1 = 1;
    var String retorno;
    retorno = "Valor de prueba para el retorno";
    return retorno;
}

function bool funcion2 () {
    global2 = 2;
    var bool retorno;
    retorno = True;
    return retorno;
}

function int funcion3 () {
    global3 = 3;
    var int retorno;
    retorno = 1337;
}

a = funcion1();
b = funcion2();
c = funcion3();

if (b && (c == c)) print("True");
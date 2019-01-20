// Probamos algunas palabras reservadas
var int a;
var int resultado;

function int multibucle (int a, int n) {
    resultado = 0;
    var int i;
    var int j;
    var int z;
    for (i = 0; True && False; i++) {
        for (j = i; True; j = i + 100){
            for (z = i + j; False; z = i + j + j){
                resultado = i + j + z;
            }
        }
    }
    print(resultado);
    prompt(i);
    return resultado;
}

function int recursividad (int p) {
    var int b;
    var int suma;
    suma = p + 1;
    b = recursividad(suma);
    if (b == 10) return b;
}
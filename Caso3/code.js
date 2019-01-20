// Probamos algunas palabras reservadas
function int suma (int a, int b) {
    return a + b;
}

function bool logica () {
    return True;
    return 0;
}

function sumaSinRetorno (int a, int b) {
    var int c;
    c = a + b;
}

function int bucle (int limite) {
    var int i;
    for (i = 0; True; i++){
        print(i);
        if (i == 10) return 10;
    }
}
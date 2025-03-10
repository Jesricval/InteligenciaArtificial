UNIDAD 1

OSUNA RUSSELL ANA ISABEL
RODRIGUEZ VALERIO JESUS RICARDO

[arbol.py](https://github.com/Jesricval/InteligenciaArtificial/blob/main/Unidad%201/Arbol.py) 

En la representación de un arbol binario de búsqueda, como sabemos cada nodo puede tener hasta 2 hijos cada uno.
Donde si el número nuevo es más pequeño que el actual, se va a la izquierda. Y si es más grande, se va a la derecha.

Explicación Código:

En la -Clase Arbol- (__init__) recibe un valor inicial y crea un objeto de la clase Nodo con ese valor.
Este nodo tambien lo podemos llamar la raíz del árbol.

En el método - agregar_nodo -, recibe un valor nodo y lo convierte en un objeto Nodo.
Luego, la insertar nuevos números en el árbol llamando al método - agregar_hijo - de la raíz.

En el método - imprimir_arbol - se inicia la impresión del árbol de manera odenada llamando al método
 - imprimir_nodos - desde la raíz, comenzando en el nivel 1.

en la - Clase Nodo- se representa los nodos individuales del árbol. Donde cada nodo tiene el valor que guarda.
Dónde entra la compación de valores que determina que camino tomar; izquierda y derecha, que inicialmente son 
None porque el nodo aún no tiene hijos.

En el método - agregar_hijo - se decide dónde colocar un nuevo nodo siguiendo las reglas de un árbol binario de búsqueda:
Si el valor es menor que el valor actual, va a la izquierda y si es mayor o igual, va a la derecha.

En el método - imprimir_nodos- se imprime primero si hay un hijo izquierdo, aumentando el nivel.
Luego, imprime su propio valor con su nivel. Por último, si hay un hijo derecho, lo imprime aumentando el nivel.

[Ejecucion de arbol.py](https://github.com/Jesricval/InteligenciaArtificial/blob/main/Unidad%201/Arbol_Binario_Ejecuciones.pdf)

Agentes inteligentes:
Los agentes basados en objetivos, o agentes basados en reglas, son agentes de IA con capacidades de razonamiento más sólidas. Además de evaluar los datos del entorno, el agente compara diferentes enfoques que lo ayudan a lograr el resultado deseado.
[Investigacion Agentes](https://github.com/Jesricval/InteligenciaArtificial/blob/main/Unidad%201/Agentes%20Inteligentes%20IA.pdf)

[Agentes Inteligentes Presentacion](https://github.com/Jesricval/InteligenciaArtificial/blob/main/Unidad%201/Agentes%20IA%20presentacio%CC%81n.pdf)

[Codigo y ejecucion de solucion del Puzzle 8](https://github.com/Jesricval/InteligenciaArtificial/tree/main/Unidad%201/puzzle)

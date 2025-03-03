#Osuna Russell Ana Isabel
#Rodriguez Valerio Jesus Ricardo

#Implementacion de la lista de prioridad para el algoritmo *
import heapq 
from random import randint
import time

# Clase para representar el estado del puzzle.
# Configuracion del tablero, estado del padre, movimiento para llegar
# a ese estado, profundidad en el arbol de busqueda y costo (Profundidad + heuristica)

# en la clase se define __ls__ para definir la funcionalidad del operador < (less than)
# este se usara para priorizar estados con el menor costo en la cola de prioridad
class Estado_Puzzle:
    def __init__(self,tablero, padre, mov, profundidad, costo):
        self.tablero = tablero  
        self.padre = padre 
        self.mov = mov 
        self.profundidad = profundidad
        self.costo = costo

    def __lt__(self, other):
        return self.costo < other.costo

# Funcion para imprimir el tablero
def print_tablero(tablero):
    print("-------------")
    for fila in range(0, 9, 3):
        fila_p = "|"
        for cuadro in tablero[fila:fila + 3]:
            if cuadro == 0:  
                fila_p += "   |"
            else:
                fila_p += f" {cuadro} |"
        print(fila_p)
        print("-------------")

# Posibles movimientos del espacio
movimientos = {
    'ARRIBA': -3,  # mover arriba
    'ABAJO': 3,   # mover abajo
    'IZQUIERDA': -1,  # mover izq
    'DERECHA': 1    # mover derecha
}

# Calculo de las distancias de manhattan
 # (Que tan lejos esta cada numero de su posicion meta)
def heuristica(tablero):
    distancias = 0
    for i in range(9):
        if tablero[i] != 0:
            x1, y1 = divmod(i, 3) ## distancia vertical
            x2, y2 = divmod(tablero[i] - 1, 3) #distancia hzt
            distancias += abs(x1 - x2) + abs(y1 - y2)
    return distancias

# Funcion que regresa el nuevo estado del tablero tras mover el espacio vacio
def mov_espacio(tablero, mov, blank_pos):
    nuevo_tablero = tablero[:]
    nuevo_blanco_pos = blank_pos + movimientos[mov]
    nuevo_tablero[blank_pos], nuevo_tablero[nuevo_blanco_pos] = nuevo_tablero[nuevo_blanco_pos], nuevo_tablero[blank_pos]
    return nuevo_tablero

def movimiento_valido(mov, blank_pos):
    if mov == 'ARRIBA' and blank_pos < 3:  # No se puede mover hacia arriba
        return False
    if mov == 'ABAJO' and blank_pos > 5:  # NO se puede mover hacia abajo
        return False
    if mov == 'IZQUIERDA' and blank_pos % 3 == 0:  # No se puede mover hacia la izq
        return False
    if mov == 'DERECHA' and blank_pos % 3 == 2:  # No se puede mover a la derecha
        return False
    return True

# Funcion de mezzcla del tablero:
def mezcla(tablero):
    for x in range(50):
        movi = ['ARRIBA', 'ABAJO', 'IZQUIERDA', 'DERECHA']
        num = randint(0,3)
        mov = movi[num]
        blank_pos = tablero.index(0)

        if movimiento_valido(mov, blank_pos) is False:
            continue

        tablero = mov_espacio(tablero, mov, blank_pos)
    return tablero


# Algoritmo A*
def a_algoritmo(estado_inicial):
    open_list = []
    closed_list = set()

    heapq.heappush(open_list, Estado_Puzzle(estado_inicial, None, None, 0, heuristica(estado_inicial)))

    while open_list:
        current_estado = heapq.heappop(open_list)

        if current_estado.tablero == goal_estado:
            return current_estado

        closed_list.add(tuple(current_estado.tablero))

        blank_pos = current_estado.tablero.index(0)

        for mov in movimientos:

            if movimiento_valido(mov, blank_pos) is False:
                continue

            nuevo_tablero = mov_espacio(current_estado.tablero, mov, blank_pos)

            if tuple(nuevo_tablero) in closed_list:
                continue

            nuevo_estado = Estado_Puzzle(nuevo_tablero, current_estado, mov, current_estado.profundidad + 1, current_estado.profundidad + 1 + heuristica(nuevo_tablero))
            heapq.heappush(open_list, nuevo_estado)

    return None

# Funcion para imprimir la solucion
def print_solution(solution):
    path = []
    current = solution
    while current:
        path.append(current)
        current = current.padre
    path.reverse()

    for step in path:
        print(f"movimiento: {step.mov}")
        print(f"Paso: {step.profundidad}")
        print_tablero(step.tablero)

inicial_estado = []

for i in range(0,3):
    for j in range (0,3):
        numero = input(f"Ingresa el numero en fila {i + 1}, columna {j + 1}: ")
        inicial_estado.append(int(numero))

print ("Tu tablero inicial: ")
print_tablero(inicial_estado)

#inicial_estado = mezcla(inicial_estado)

goal_estado = []

print("Tablero meta: ")
for i in range(0,3):
    for j in range (0,3):
        numero = input(f"Ingresa el numero en fila {i + 1}, columna {j + 1}: ")
        goal_estado.append(int(numero))


print ("Tu tablero inicial: ")
print_tablero(inicial_estado)

print ("Tu tablero final: ")
print_tablero(goal_estado)


start = time.time()

solution = a_algoritmo(inicial_estado)

end = time.time()

if solution:
    print("-------------------------")
    print("Solucion:")
    print_solution(solution)
else:
    print("No tiene solucion.")

print("Tiempo de ejecucion")
print(f"{round(end - start, 4)} segundos")

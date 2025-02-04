# Osuna Russell Ana Isabel
# Rodriguez Valerio Jesus Ricardo
class Arbol:
    def __init__(self, raiz):
        self.raiz = Nodo(raiz)
    
    def agregar_nodo(self, nodo):
        self.raiz.agregar_hijo(Nodo(nodo))

    def imprimir_arbol(self):
        self.raiz.imprimir_nodos(1)

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None
    
    def agregar_hijo(self, hijo):
        if hijo.valor < self.valor:
            if self.izquierda is None:
                self.izquierda = hijo
            else:
                self.izquierda.agregar_hijo(hijo)
        else:
            if self.derecha is None:
                self.derecha = hijo
            else:
                self.derecha.agregar_hijo(hijo)

    def imprimir_nodos(self, nivel):
        if self.izquierda:
            self.izquierda.imprimir_nodos(nivel + 1)
        print("Nivel ", nivel, ": ", self.valor)
        if self.derecha:
            self.derecha.imprimir_nodos( nivel + 1)
        

#ejecucion
root = Arbol(10)
root.agregar_nodo(5)
root.agregar_nodo(15)
root.agregar_nodo(30)
root.agregar_nodo(1)
root.imprimir_arbol()
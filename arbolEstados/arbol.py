from collections import deque

class Nodo:
    def __init__(self, datos, padre = None):
        self.datos = datos  
        self.padre = padre  
        self.hijos = []     #Se guardaran todos los nodos creados
        
    
    #funcion para agregar hijos
def generar_hijos(nodo):
    hijos = []
    cartas = list(nodo.datos)
    n = len(cartas)
        
    for k in range(1, n):
        #hacemos una copia para evitar problemas de perder el original
        nuevas_cartas = cartas.copy()
        #intercambio de posiciones
        nuevas_cartas[0], nuevas_cartas[k] = nuevas_cartas[k], nuevas_cartas[0]
        #se crea el nodo hijo que apunte al antiguo nodo
        hijo = Nodo(nuevas_cartas, padre = nodo)
        hijos.append(hijo)
        
    return hijos
    
def reconstruir_camino(ultimo_nodo):
    camino = []
    actual = ultimo_nodo
    while actual is not None:
        camino.append(list(actual.datos))
        actual = actual.padre
        #se invirtio la lista, para mostrar del principio a fin
    return camino [::-1]
    
             
             

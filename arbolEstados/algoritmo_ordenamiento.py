from arbol import Nodo, generar_hijos, reconstruir_camino
from collections import deque

def ordenar_cartas_carbol(cartas_iniciales):
    #Es a donde se quiere llegar
    meta = sorted(cartas_iniciales)
    
    raiz = Nodo(cartas_iniciales)
    
    #caso de que ya este ordenada la raiz
    if raiz.datos == meta:
        return [list(raiz.datos)]
    
    #ocupamos una cola para almacenar por nivel
    cola = deque([raiz])
    
    #hacemos un lista para guardar los nodos creados
    visitados = {tuple(raiz.datos)}
    
    while cola:
        nodo_actual = cola.popleft() #sacamos de cola 
        
        #generamos las ramificaciones 
        hijos = generar_hijos(nodo_actual)
        
        for hijo in hijos:
            hijo_tuple = tuple(hijo.datos)
            #revisar que la convinación no se haya creado ya 
            if hijo_tuple not in visitados:
                visitados.add(hijo_tuple)
                nodo_actual.hijos.append(hijo)
                
                if hijo.datos == meta:
                    return reconstruir_camino(hijo)
                
                cola.append(hijo)
                
    return None



        
    
    
import networkx as nx
import matplotlib.pyplot as plt
from arbol import Nodo

def calcular_posiciones_por_niveles(nodo_raiz):
    """
    Asigna coordenadas (x, y) a cada nodo para que el árbol se dibuje 
    estrictamente ordenado por niveles (Top-Down).
    """
    pos = {}
    niveles = {}  # Guarda los nodos agrupados por profundidad: {0: [raiz], 1: [hijo1, hijo2], ...}
    
    # Cola para recorrido por anchura (BFS) guardando (nodo, nivel_actual)
    cola = [(nodo_raiz, 0)]
    visitados = set()

    while cola:
        nodo_actual, nivel = cola.pop(0)
        id_actual = id(nodo_actual)

        if id_actual in visitados:
            continue
        visitados.add(id_actual)

        if nivel not in niveles:
            niveles[nivel] = []
        niveles[nivel].append(nodo_actual)

        # Recorrer hijos en el siguiente nivel
        hijos = nodo_actual.hijos if isinstance(nodo_actual, Nodo) else []
        for hijo in hijos:
            cola.append((hijo, nivel + 1))

    # Asignar coordenadas (x, y) en el plano cartesiano
    # y = -nivel (para que el nivel 0 quede arriba y los demás bajen)
    # x = centrado horizontalmente para cada grupo de nodos del mismo nivel
    for nivel, nodos_del_nivel in niveles.items():
        total_nodos = len(nodos_del_nivel)
        for i, nodo in enumerate(nodos_del_nivel):
            id_nodo = id(nodo)
            # Calcular x para distribuir los nodos de forma simétrica
            if total_nodos == 1:
                x = 0.5
            else:
                x = i / (total_nodos - 1)
            
            y = -nivel  # Profundidad hacia abajo
            pos[id_nodo] = (x, y)

    return pos


def mostrar_arbol(nodo_raiz, camino_solucion=None):
    """
    Dibuja el árbol de estados organizado formalmente por NIVELES en Spyder.
    """
    if nodo_raiz is None:
        print("No hay nodo raíz para graficar.")
        return

    G = nx.DiGraph()
    labels = {}
    colores = []

    # Preparar el conjunto de combinaciones que forman el camino más corto
    conjunto_camino = set()
    if camino_solucion:
        conjunto_camino = {
            tuple(estado) if isinstance(estado, (list, tuple)) else estado 
            for estado in camino_solucion
        }

    # Recorrer el árbol para armar la estructura del grafo
    cola = [nodo_raiz]
    visitados = set()

    while cola:
        nodo_actual = cola.pop(0)
        id_actual = id(nodo_actual)

        if id_actual in visitados:
            continue
        visitados.add(id_actual)

        # Extraer datos e hijos manejando tipo Nodo
        if isinstance(nodo_actual, Nodo):
            datos_nodo = nodo_actual.datos
            hijos_nodo = nodo_actual.hijos
        else:
            datos_nodo = nodo_actual
            hijos_nodo = []

        labels[id_actual] = str(list(datos_nodo))

        for hijo in hijos_nodo:
            id_hijo = id(hijo)
            G.add_edge(id_actual, id_hijo)
            cola.append(hijo)

    # Resaltar en verde claro la solución óptima y en azul los demás
    for node_id in G.nodes():
        es_solucion = False
        for nodo_v in visitados:
            if id(nodo_v) == node_id:
                datos = nodo_v.datos if isinstance(nodo_v, Nodo) else nodo_v
                if tuple(datos) in conjunto_camino:
                    es_solucion = True
                    break

        if es_solucion:
            colores.append('lightgreen')
        else:
            colores.append('skyblue')

    # Calcular posiciones ordenadas por jerarquía vertical (Nivel 0, Nivel 1, Nivel 2...)
    posiciones = calcular_posiciones_por_niveles(nodo_raiz)

    # Dibujar la figura
    plt.figure(figsize=(12, 8))
    nx.draw(
        G, posiciones, labels=labels, with_labels=True, 
        node_size=2500, node_color=colores, font_size=8, 
        font_weight='bold', edge_color='gray', arrowsize=15
    )

    plt.title("Árbol de Espacio de Estados Organizado por Niveles", fontsize=12)
    plt.show()
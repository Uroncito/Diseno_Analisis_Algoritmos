import graphviz

def generar_imagen_arbol(nodo_raiz, camino_solucion=None, nombre_archivo="arbol_estados"):
    """
    Genera una imagen PNG del árbol de estados usando Graphviz.
    
    :param nodo_raiz: Objeto Nodo que representa la raíz del árbol.
    :param camino_solucion: Lista de estados (listas) que forman el camino más corto.
    :param nombre_archivo: Nombre del archivo de salida (sin extensión).
    """
    # Convertir el camino solución a un conjunto de tuplas para resaltar los nodos óptimos en verde
    conjunto_camino = set()
    if camino_solucion:
        conjunto_camino = {tuple(estado) for estado in camino_solucion}

    # Crear el grafo dirigido con Graphviz
    dot = graphviz.Digraph(comment='Árbol de Estados de Cartas', format='png')
    dot.attr(rankdir='TB', size='10')  # TB = Top to Bottom (Arriba hacia Abajo)

    # Cola para recorrer el árbol (BFS) y evitar dibujar nodos duplicados infinitos
    cola = [nodo_raiz]
    visitados = set()

    while cola:
        nodo_actual = cola.pop(0)
        id_actual = str(id(nodo_actual))  # Identificador único en memoria de cada objeto Nodo

        if id_actual in visitados:
            continue
        visitados.add(id_actual)

        # Dar formato visual al nodo
        etiqueta = str(list(nodo_actual.datos))
        
        # Si el nodo pertenece al camino solución, se pinta verde
        if tuple(nodo_actual.datos) in conjunto_camino:
            dot.node(id_actual, label=etiqueta, style='filled', fillcolor='lightgreen', shape='box')
        else:
            dot.node(id_actual, label=etiqueta, shape='ellipse')

        # Conectar con cada uno de sus nodos hijos
        for hijo in nodo_actual.hijos:
            id_hijo = str(id(hijo))
            dot.edge(id_actual, id_hijo)
            cola.append(hijo)

    # Guardar y renderizar la imagen PNG
    dot.render(nombre_archivo, cleanup=True)
    print(f"¡Árbol visual guardado exitosamente como '{nombre_archivo}.png'!")

import networkx as nx
import matplotlib.pyplot as plt

colores_lineas = {
    'L1': '#F04E98',  # Rosa
    'L2': '#005EB8',  # Azul
    'L3': '#AF9800',  # Verde olivo
    'L4': '#6BBBAE',  # Cian
    'L5': '#FFD100',  # Amarillo
    'L6': '#DA291C',  # Rojo
    'L7': '#E87722',  # Naranja
    'L8': '#009A44',  # Verde bandera
    'L9': '#512D1D',  # Café
    'LA': '#9B26B6',  # Morado
    'LB': '#B1B3B3',  # Verde/Gris
    'L12': '#B09A5B'  # Oro
}#Color de cada linea

anclas = {
    'EL ROSARIO': (-7.5, 8.5), 'INSTITUTO DEL PETROLEO': (-3.0, 7.5), 'MARTIN CARRERA': (0.5, 7.0),
    'INDIOS VERDES': (-0.5, 8.5), 'DEPORTIVO 18 DE MARZO': (-1.0, 7.2), 'LA RAZA': (-2.0, 5.5),
    'POLITECNICO': (-3.5, 9.0), 'CONSULADO': (0.0, 4.5), 'OCEANIA': (2.5, 3.5),
    'CIUDAD AZTECA': (7.5, 11.0), 'BUENAVISTA': (-3.5, 3.5), 'GUERRERO': (-2.8, 3.5),
    'GARIBALDI': (-2.2, 3.5), 'MORELOS': (-0.5, 3.0), 'SAN LAZARO': (0.2, 1.8),
    'CUATRO CAMINOS': (-9.5, 4.5), 'TACUBA': (-6.8, 4.3), 'HIDALGO': (-3.0, 2.5),
    'BELLAS ARTES': (-2.2, 2.5), 'PINO SUAREZ': (-1.5, 1.5), 'SALTO DEL AGUA': (-2.5, 1.5),
    'BALDERAS': (-3.0, 1.5), 'TACUBAYA': (-6.5, 0.0), 'OBSERVATORIO': (-8.2, -0.5),
    'CENTRO MEDICO': (-3.2, -0.5), 'CHABACANO': (-1.8, -0.5), 'JAMAICA': (-0.2, -0.5),
    'SANTA ANITA': (-0.2, -1.2), 'PANTITLAN': (4.2, -0.2), 'LA PAZ': (8.2, -6.5),
    'BARRANCA DEL MUERTO': (-6.8, -4.5), 'MIXCOAC': (-6.5, -3.5), 'ZAPATA': (-4.2, -4.2),
    'UNIVERSIDAD': (-5.2, -8.5), 'ERMITA': (-2.2, -4.8), 'TASQUENA': (-2.5, -6.8),
    'ATLALILCO': (1.2, -5.2), 'CONSTITUCION DE 1917': (4.5, -6.5), 'TLAHUAC': (7.5, -9.5),
    'CANDELARIA': (-0.5, 1.5) #Forma de las lineas del metro
}

def posicionesDelMapa(grafo):
    pos = {}
    for linea in colores_lineas.keys():
        nodos_linea = [n for n in grafo.nodes() if n.endswith(f" {linea}")]
        subgrafo = grafo.subgraph(nodos_linea)
        
        extremos = [n for n, d in subgrafo.degree() if d == 1]
        if not extremos:
            continue
        ordenados = list(nx.dfs_preorder_nodes(subgrafo, source=extremos[0]))
        
        indices_ancla = []
        for idx, nodo in enumerate(ordenados):
            nombre_est = nodo.rsplit(' ', 1)[0]
            if nombre_est in anclas:
                indices_ancla.append((idx, anclas[nombre_est]))
                
        for k in range(len(indices_ancla) - 1):
            idx1, (x1, y1) = indices_ancla[k]
            idx2, (x2, y2) = indices_ancla[k + 1]
            pasos = idx2 - idx1
            for step in range(pasos + 1):
                t = step / pasos
                nodo_actual = ordenados[idx1 + step]
                offset = (list(colores_lineas.keys()).index(linea) - 6) * 0.025
                pos[nodo_actual] = (x1 + t * (x2 - x1) + offset, y1 + t * (y2 - y1) - offset)
                
    for nodo in grafo.nodes():
        if nodo not in pos:
            pos[nodo] = (0, 0)
    return pos

def mostrar_ruta(grafo, ruta):
    print("\nAbriendo mapa esquemático del Metro CDMX...")
    
    fig, ax = plt.subplots(figsize=(16, 11))
    fig.canvas.manager.set_window_title("Mapa Esquemático Metro CDMX - Ruta Dijkstra")
    
    pos = posicionesDelMapa(grafo)
    
   #Lineas con los colores
    for u, v in grafo.edges():
        linea_u = u.rsplit(' ', 1)[1]
        linea_v = v.rsplit(' ', 1)[1]
        if linea_u == linea_v:
            color = colores_lineas.get(linea_u, 'gray')
            nx.draw_networkx_edges(grafo, pos, edgelist=[(u, v)], width=3.5, edge_color=color, alpha=0.35, ax=ax)
        else:
            nx.draw_networkx_edges(grafo, pos, edgelist=[(u, v)], width=2, edge_color='black', style='dotted', alpha=0.4, ax=ax)

    #Etaciones no usadas
    nodos_noUsados = [n for n in grafo.nodes() if n not in ruta]
    nx.draw_networkx_nodes(grafo, pos, nodelist=nodos_noUsados, node_size=25, node_color='white', edgecolors='gray', linewidths=0.8, ax=ax)
    
    #nombre en todos los nodos
    nombreEstaciones = {n: n.rsplit(' ', 1)[0] for n in nodos_noUsados}
    nx.draw_networkx_labels(grafo, pos, labels=nombreEstaciones, font_size=5, font_color='#555555', ax=ax)
    
    #Ruta Dijkstra
    aristas_ruta = [(ruta[i], ruta[i+1]) for i in range(len(ruta)-1)]
    nx.draw_networkx_edges(grafo, pos, edgelist=aristas_ruta, width=9, edge_color='#FFEE00', alpha=0.9, ax=ax)
    nx.draw_networkx_edges(grafo, pos, edgelist=aristas_ruta, width=3.5, edge_color='#D50000', ax=ax)
    
    nx.draw_networkx_nodes(grafo, pos, nodelist=ruta, node_size=90, node_color='#FFEE00', edgecolors='#D50000', linewidths=2, ax=ax)
    nx.draw_networkx_nodes(grafo, pos, nodelist=[ruta[0], ruta[-1]], node_size=180, node_color='#00C853', edgecolors='black', linewidths=2, ax=ax)
    
    etiquetas_ruta = {n: n for n in ruta}
    nx.draw_networkx_labels(grafo, pos, labels=etiquetas_ruta, font_size=8, font_weight='bold', font_color='black', 
                            bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='#D50000', alpha=0.85), ax=ax)
    
    ax.set_title("Lineas del Metro CDMX", fontsize=15, fontweight='bold')
    ax.axis('off')
    fig.tight_layout()
    
    plt.ion()
    plt.show(block=True)
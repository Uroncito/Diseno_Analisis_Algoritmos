import networkx as nx
import matplotlib.pyplot as plt
from arbol import Nodo

def _obtener_ancho_subarbol(nodo):
    """Calcula cuántas hojas tiene la rama de este nodo para reservar su espacio horizontal."""
    hijos = nodo.hijos if isinstance(nodo, Nodo) else []
    if not hijos:
        return 1
    return sum(_obtener_ancho_subarbol(hijo) for hijo in hijos)

def _asignar_coordenadas_arbol(nodo, nivel=0, x_inicio=0.0, pos=None, info_nodos=None):
    """
    Posiciona cada nodo exactamente centrado encima de sus hijos (estilo árbol binario/n-ario).
    """
    if pos is None:
        pos = {}
    if info_nodos is None:
        info_nodos = {}

    id_nodo = id(nodo)
    info_nodos[id_nodo] = nodo
    hijos = nodo.hijos if isinstance(nodo, Nodo) else []

    if not hijos:
        # Si es hoja, ocupa 1 unidad de ancho
        pos[id_nodo] = (x_inicio + 0.5, -nivel)
        return x_inicio + 1.0, pos, info_nodos

    # Si tiene hijos, posicionamos cada subárbol de izquierda a derecha
    x_actual = x_inicio
    centros_hijos = []
    for hijo in hijos:
        x_actual, pos, info_nodos = _asignar_coordenadas_arbol(
            hijo, nivel + 1, x_actual, pos, info_nodos
        )
        centros_hijos.append(pos[id(hijo)][0])

    # El padre se coloca exactamente en el punto medio entre su primer y último hijo
    x_padre = (centros_hijos[0] + centros_hijos[-1]) / 2.0
    pos[id_nodo] = (x_padre, -nivel)

    return x_actual, pos, info_nodos


def mostrar_arbol(nodo_raiz, camino_solucion=None):
    """
    Dibuja el árbol de estados con estructura jerárquica limpia y escala dinámica
    para soportar desde pocas hasta muchas cartas sin apachurrarse.
    """
    if nodo_raiz is None:
        print("No hay nodo raíz para graficar.")
        return

    # 1. Calcular posiciones jerárquicas tipo árbol
    ancho_total, posiciones, info_nodos = _asignar_coordenadas_arbol(nodo_raiz)
    total_nodos = len(info_nodos)
    profundidad_max = max(abs(y) for _, y in posiciones.values())
    num_cartas = len(nodo_raiz.datos) if isinstance(nodo_raiz, Nodo) else len(nodo_raiz)

    # Aviso preventivo si con 10 cartas se generó un árbol gigantesco
    if total_nodos > 400:
        print(f"Aviso: El árbol tiene {total_nodos} nodos. La ventana será muy ancha; usa la lupa para hacer zoom.")

    # 2. Construir el grafo dirigido
    G = nx.DiGraph()
    labels = {}

    for id_nodo, nodo in info_nodos.items():
        datos = nodo.datos if isinstance(nodo, Nodo) else nodo
        # Si son muchas cartas (ej. 10), formato compacto sin espacios para ahorrar ancho
        if num_cartas >= 7:
            labels[id_nodo] = "[" + ",".join(map(str, datos)) + "]"
        else:
            labels[id_nodo] = str(list(datos))

        G.add_node(id_nodo)
        hijos = nodo.hijos if isinstance(nodo, Nodo) else []
        for hijo in hijos:
            G.add_edge(id_nodo, id(hijo))

    # 3. Escalar dinámicamente el lienzo y la letra según cantidad de nodos y cartas
    factor_ancho = max(1.1, num_cartas * 0.28)
    fig_ancho = min(60, max(12, ancho_total * factor_ancho))
    fig_alto = min(35, max(7, (profundidad_max + 1) * 1.8))

    if total_nodos > 120 or num_cartas >= 8:
        tam_fuente = 6
    elif total_nodos > 40 or num_cartas >= 6:
        tam_fuente = 7
    else:
        tam_fuente = 9

    fig, ax = plt.subplots(figsize=(fig_ancho, fig_alto))
    fig.canvas.manager.set_window_title("Árbol de Espacio de Estados")

    # 4. Dibujar primero las flechas (aristas)
    nx.draw_networkx_edges(
        G, posiciones, ax=ax,
        edge_color='#7f8c8d', arrows=True, arrowsize=12,
        width=1.2, node_size=800
    )

    # 5. Dibujar cada nodo como una caja rectangular adaptable al texto
    conjunto_camino = set()
    if camino_solucion:
        conjunto_camino = {
            tuple(estado) if isinstance(estado, (list, tuple)) else estado
            for estado in camino_solucion
        }

    for id_nodo, (x, y) in posiciones.items():
        nodo = info_nodos[id_nodo]
        datos = nodo.datos if isinstance(nodo, Nodo) else nodo
        es_raiz = (id_nodo == id(nodo_raiz))
        es_solucion = tuple(datos) in conjunto_camino

        # Colores diferenciados: Dorado para la raíz, Verde para el camino más corto, Azul para el resto
        if es_raiz:
            color_fondo = '#ffe082'  # Amarillo suave (Raíz)
            color_borde = '#f57f17'
        elif es_solucion:
            color_fondo = '#a5d6a7'  # Verde claro (Ruta óptima)
            color_borde = '#2e7d32'
        else:
            color_fondo = '#b3e5fc'  # Azul claro (Explorados)
            color_borde = '#0277bd'

        ax.text(
            x, y, labels[id_nodo],
            ha='center', va='center',
            fontsize=tam_fuente, fontweight='bold', color='#1a1a1a',
            bbox=dict(
                boxstyle='round,pad=0.35',
                facecolor=color_fondo,
                edgecolor=color_borde,
                linewidth=1.5
            ),
            zorder=3
        )

    # 6. Etiquetas laterales indicando Nivel 0, Nivel 1, Nivel 2...
    x_min = min(x for x, _ in posiciones.values()) - 0.8
    x_max = max(x for x, _ in posiciones.values()) + 0.8
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-profundidad_max - 0.7, 0.7)

    for nivel in range(profundidad_max + 1):
        ax.text(
            x_min + 0.1, -nivel, f"Nivel {nivel}",
            fontsize=tam_fuente, color='#555555', style='italic', va='center'
        )

    ax.set_title(
        f"Árbol de Espacio de Estados ({total_nodos} nodos | {profundidad_max} niveles)",
        fontsize=12, fontweight='bold', pad=15
    )
    ax.axis('off')
    plt.tight_layout()
    plt.show(block=True)
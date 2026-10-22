import matplotlib.pyplot as plt

def graficar_puntos_dominancia(puntos, min_x=0, max_x=500, min_y=0, max_y=500):
    """
    Paso 3: Graficación visual de los puntos, la línea divisoria L 
    y el número de dominancia al lado de cada punto.
    """
    if not puntos:
        print("No hay puntos para graficar.")
        return

    # Extraer coordenadas para matplotlib
    x_coords = [p['x'] for p in puntos]
    y_coords = [p['y'] for p in puntos]

    plt.figure(figsize=(9, 7))

    # Dibujar los puntos en el plano cartesiano
    plt.scatter(x_coords, y_coords, color='blue', alpha=0.7, edgecolors='black', label='Puntos (x,y)')

    # Colocar la etiqueta visual de dominancia (ej. "Dom: 3") a lado de cada punto
    for p in puntos:
        texto_etiqueta = p['dom']
        plt.annotate(
            texto_etiqueta, 
            (p['x'], p['y']), 
            textcoords="offset points", 
            xytext=(6, 6), 
            fontsize=8, 
            fontweight='bold', 
            color='darkred'
        )

    # Trazar la línea divisoria L si tenemos más de un punto
    if len(puntos) > 1:
        puntos_ord_x = sorted(puntos, key=lambda p: p['x'])
        medio = len(puntos_ord_x) // 2
        
        # Posición en X de la línea de corte L (promedio entre el límite de A y B)
        x_corte = (puntos_ord_x[medio - 1]['x'] + puntos_ord_x[medio]['x']) / 2
        
        # Dibujar línea vertical azul L
        plt.axvline(x=x_corte, color='blue', linestyle='--', linewidth=2, label=f'Línea divisoria L (x={x_corte:.2f})')

    # Configuración de límites y títulos
    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)
    plt.title("Algoritmo de Dominancia y Rango (Divide y Vencerás)", fontsize=12)
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper left')
    plt.show()
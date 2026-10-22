from leer_csv import leer_csv
from dominancia import ordenar_por_x
from dominancia import dominancia
from graficar_puntos_dominados import graficar_puntos_dominancia


if __name__ == "__main__":
    puntos_raw = leer_csv("puntos_prueba.csv")  # Retorna tuplas [(x1, y1), (x2, y2), ...]
    
    #Convertir tuplas a una estructura con diccionario para llevar el contador 'dom'
    puntos = [{'x': p[0], 'y': p[1], 'dom': 0} for p in puntos_raw]

    # 3. Pre-procesamiento: Ordenar por coordenada X
    puntos_ordenados_x = ordenar_por_x(puntos)

    # 4. Calcular el rango de dominancia con Divide y Vencerás
    puntos_procesados = dominancia(puntos_ordenados_x)

    # 5. Desplegar resultados por consola
    print("\n--- RESULTADOS DE DOMINANCIA ---")
    for p in sorted(puntos_procesados, key=lambda item: item['x']):
        print(f"Punto ({p['x']}, {p['y']}) -> Domina a: {p['dom']} puntos.")

    # 6. Mostrar la gráfica con la línea divisoria L y los contadores
    graficar_puntos_dominancia(puntos_procesados, min_x=0, max_x=100, min_y=0, max_y=100)
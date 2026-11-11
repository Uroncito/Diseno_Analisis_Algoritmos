#algoritmos de combinaciones
#segun la formula esta nos va a dar la variedad de poder crear una cantidad r 
#de elementos para hacer todas las combinaciones que se puedan hacer de una 
#cantidad de elementos de un arreglo, sin que se repitan las combinaaciones

import csv

def obtener_combinaciones(arreglo, r):
    """
    Función principal que prepara la lista de resultados e inicia la recursividad.
    """
    resultados = []
    _backtracking_combinaciones(arreglo, r, [], 0, resultados)
    return resultados

def _backtracking_combinaciones(arreglo, r, combinacion_actual, start, resultados):
    """
    Lógica matemática: Avanza el índice 'start' para matar ramas duplicadas.
    """
    if len(combinacion_actual) == r:
        resultados.append(list(combinacion_actual))
        return

    for i in range(start, len(arreglo)):
        combinacion_actual.append(arreglo[i])
        _backtracking_combinaciones(arreglo, r, combinacion_actual, i + 1, resultados)
        combinacion_actual.pop()

def leer_elementos_csv(ruta_archivo):
    """
    Lee un archivo CSV donde los elementos estén en la primera fila o columna.
    """
    elementos = []
    with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            for dato in fila:
                if dato.strip():
                    elementos.append(dato.strip())
    return elementos

# --- Interacción por Consola (Solo se ejecuta si corres este archivo) ---
if __name__ == "__main__":
    print("--- ALGORITMO DE COMBINACIONES (CONSOLA) ---")
    entrada = input("Ingresa los elementos separados por coma (ej. A,B,C,D): ")
    arreglo_base = [x.strip() for x in entrada.split(",")]
    
    tamano = int(input("¿De qué tamaño quieres las combinaciones? (r): "))
    
    combinaciones_generadas = obtener_combinaciones(arreglo_base, tamano)
    print(f"\nSe encontraron {len(combinaciones_generadas)} combinaciones:")
    for combo in combinaciones_generadas:
        print(combo)
"""
algoritmos de combinaciones
segun la formula esta nos va a dar la variedad de poder crear una cantidad r 
de elementos para hacer todas las combinaciones que se puedan hacer de una 
cantidad de elementos de un arreglo, sin que se repitan las combinaaciones
"""
    #Funcion principail
def obtener_combinaciones(arreglo, r):
    resultados = []
    _backtracking_combinaciones(arreglo, r, [], 0, resultados)
    return resultados

    #Lógica matemática: Avanza el índice 'start' para matar ramas duplicadas.
def _backtracking_combinaciones(arreglo, r, combinacion_actual, start, resultados):
    if len(combinacion_actual) == r:
        resultados.append(list(combinacion_actual))
        return

    for i in range(start, len(arreglo)):
        combinacion_actual.append(arreglo[i])
        _backtracking_combinaciones(arreglo, r, combinacion_actual, i + 1, resultados)
        combinacion_actual.pop()

#Interacción por Consola
if __name__ == "__main__":
    print("Algoritmo de Combinaciones")
    entrada = input("Ingresa los elementos separados por coma: ")
    
    arreglo_base = [x.strip() for x in entrada.split(",")]
    tamano = int(input("¿De qué tamaño quieres las combinaciones? (r): "))
    
    combinaciones_generadas = obtener_combinaciones(arreglo_base, tamano)
    
    print(f"\nSe encontraron {len(combinaciones_generadas)} combinaciones:")
    for combinacion in combinaciones_generadas:
        print(combinacion)
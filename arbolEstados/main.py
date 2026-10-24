import random as rd
from algoritmo_ordenamiento import ordenar_cartas_carbol

def guardar_num_ingresados(entrada):
    try:
        #eliminar esapcios en la entrada y el principio
        #entrada  = entrada.strip()
        
        #caso 1: si no hay espacios entre los numeros
        if " " not in entrada:
            numeros = [int(x) for x in entrada]
        
        #caso 2: cuando haya espacios 
        else: 
            numeros = [int(x) for x in entrada.split()]
        
        if not numeros:
            raise ValueError("No hay numeros a guardar")
        
        return numeros

    except ValueError:
        print("No escribas en letras los numeros y separalos con espacios")
        return[]
    

if __name__ == "__main__":
    entrada_usuario = input("Introduce los numeros de un digito: ")
    numeros = guardar_num_ingresados(entrada_usuario)
    print("Los numeros son: ", numeros)
    
    if numeros:
        rd.shuffle(numeros)
        cartas = numeros
        
        print(f"Estado inicial: {cartas}")
    
        pasos = ordenar_cartas_carbol(cartas)
    
        if pasos:    
            print(f"\n¡Solución encontrada en {len(pasos) - 1} movimientos!")
            print("Camino más corto:")
            for i, paso in enumerate(pasos):
                print(f"Paso {i}: {paso}")  
        else:
            print("No se encontró solución")
            
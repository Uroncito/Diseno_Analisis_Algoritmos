from leer_csv import leer_csv
#llamamos nuestro funcion que habiamos creado

#Primero debemos de ordenar los puntos segun x, para evitarnos comparaciones
#asi ya solo comparamos las y para ver cuales domina
def ordenar_por_x(puntos):
    #usamos la función de python sorted que es el metodo de mezcla 
    #como el metodo de ordenamiento es mezcla el algoritmos sigue siendo O(nlogn)
    return sorted(puntos, key=lambda p: p['x'])

def dominancia(puntos_ordenados):
    #como el algoritmo es parecido a mezcla, necesitamos dividir
    n = len(puntos_ordenados)
    
    #caso 1: si hay solo 1 o 0 puntos
    if n <= 1:
        return puntos_ordenados
    
    #caso 2: lista larga, hay que encontrrar el punto medio
    medio = n//2
    izquierda = puntos_ordenados[:medio]
    derecha = puntos_ordenados[medio:]
    
    #llamadas recursiva para los subproblemas
    izq_dominada_y = dominancia(izquierda)
    der_dominada_y = dominancia(derecha)
    
    #COMBINAR Y MEZCLAR por la ordenada y
    puntos_dominados = []
    i = 0   #puntero para izquierda
    j = 0   #puntero para derecha
    
    contador_puntos_dominados = 0
    
    #Hacer las comparaciones en y
    while i < len(izq_dominada_y) and j < len(der_dominada_y):
        if izq_dominada_y[i]['y'] <= der_dominada_y [j]['y']:
            puntos_dominados.append(izq_dominada_y[i])
            contador_puntos_dominados += 1
            i+=1
        else:
            der_dominada_y[j]['dom'] += contador_puntos_dominados
            puntos_dominados.append(der_dominada_y[j])
            j += 1
            
    #Vacia los elementos que se quedaron a la izquierda
    while i < len(izq_dominada_y):
        puntos_dominados.append(izq_dominada_y[i])
        i += 1
        
    #Vaciar los elemnetos de la derecha y sumar los puntos dominados
    while j < len(der_dominada_y):
        der_dominada_y[j]['dom'] += contador_puntos_dominados
        puntos_dominados.append(der_dominada_y[j])
        j += 1
    
    return puntos_dominados


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    



def estado_valido(estado):
    #Estado es la lista de [Campesino, Gallina, Lobo, Maiz]
    #False = lado izquierdo donde inicia y True = lado de rio derecho
   
    granjero, gallina, lobo, maiz = estado
    
    # Si la gallina y el lobo estan sin el granjerp
    #El lobo se come a la gallina
    if lobo == gallina and granjero != lobo:
        return False
        
    # Si la gallina y el maiz están juntos sin el granjero
    #La gallina se come el maiz
    if gallina == maiz and granjero != gallina:
        return False
        
    return True #Si no pasa ninguno, entonces es true

def generar_movimientos(estado_actual):
    #Posibles estados
    granjero, gallina, lobo, maiz = estado_actual
    posibles = []
    
    # El granjero puede cruzar solo 
    posibles.append(([not granjero, gallina, lobo, maiz], 'Granjero solo'))
    
    # El granjero puede llevar a la gallina
    if granjero == gallina:
        posibles.append(([not granjero, not gallina, lobo, maiz], 'Granjero con Gallina'))
        
    #El granjero puede llevar al lobo
    if granjero == lobo:
        posibles.append(([not granjero, gallina, not lobo, maiz], 'Granjero con Lobo'))
        
    #El grandejo lleva al maiz
    if granjero == maiz:
        posibles.append(([not granjero, gallina, lobo, not maiz], 'Granjero con Maiz'))
        
    return posibles

def resolver_problema():
    #Estado inicial: Todos al inicio (False)
    inicio = [False, False, False, False]
    #Final: Todos al otro lado (True)
    final = [True, True, True, True]
    
    #Lista como pila para ir explorando los caminos.
    #Se guardan tuplas con (estado_actual, ruta_de_estados, ruta_de_granjero)
    pila = [(inicio, [inicio], [])]
    visto = []
    
    # Bucle de búsqueda (Motor de inferencia simplificado)
    while pila:
        estado_actual, ruta, letras = pila.pop()
        
        # Si llegamos a al final, es igual a las rutas finales
        if estado_actual == final:
            return ruta, letras
            
        visto.append(estado_actual)
        
        #Siguientes movimientos válidos
        for nuevo_estado, letra in generar_movimientos(estado_actual):
            if estado_valido(nuevo_estado) and nuevo_estado not in visto:
                #Nueva ruta a la pila para seguir explorando
                pila.append((nuevo_estado, ruta + [nuevo_estado], letras + [letra]))
                
    return None, None # Si no hay solución

if __name__ == "__main__":   
    ruta_estados, ruta_letras = resolver_problema()
    
    if ruta_estados:
        #Recorrido de estados
        for estado in ruta_estados:
            texto = " ".join(str(item).lower() for item in estado)
            print(texto)
            
        print("-------")
        
        estado_final = ruta_estados[-1]
        
        #transformacion a texto
        texto_final = " ".join(str(item).lower() for item in estado_final)
        
        #Imprime estado final
        print(f"{texto_final}")
        
        #acciones
        for letra in ruta_letras:
            print(letra)
        print("Exito") 
    else:
        print("No se encontró una solución válida.")
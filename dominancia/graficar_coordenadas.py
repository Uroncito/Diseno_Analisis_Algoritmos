import matplotlib.pyplot as plt
from leer_csv import leer_csv #Para leer el archivo

def graficar_puntos(listaPuntos, min_x=0, max_x=100, min_y=0, max_y=100, limitadorEjes = True):
    if not listaPuntos:
        print("No hay coordenadas para graficar")
        return
    #Separa la lista de duplas leida de leer en dos listas
    x_coordenadas = [p[0] for p in listaPuntos]
    y_coordenadas = [p[1] for p in listaPuntos]
    #Crear la figura o punto en este caso
    plt.figure(figsize = (8,6))
    #Dibujar los puntos en el plano
    plt.scatter(x_coordenadas, y_coordenadas, color='blue', alpha=0.7, edgecolors='black', label='Puntos')
    
    #Mostar las coordenadas en texto al lado de cada punto
    #Despues lo ocuparemos para marcar la dominancia aqui 
    #for i, (x, y) in enumerate(listaPuntos):
     #   plt.annotate(f"({x}, {y})", (x, y), textcoords="offset points", xytext=(5, 5), fontsize=8)
    
    #Poner titulo de grafica y etiquetas de los ejes
    plt.title("Algoritmo de Dominancia")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True, linestyle='--', alpha=0.5)
    
    #Si limitador = true, da el rango predeterminado
    #Si es false, da del punto mayor encontrado, es decir apretada
    if limitadorEjes:
        plt.xlim(min_x, max_x)
        plt.ylim(min_y, max_y)
        
    plt.legend()
    plt.show()
    
if __name__ == "__main__":
    puntos= leer_csv("puntos_prueba.csv")
    graficar_puntos(puntos)
    
#%matplotlib qt
#Ponerlo en la consola para que al ejecutar lo habra en otra ventana 

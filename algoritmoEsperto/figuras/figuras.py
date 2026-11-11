import matplotlib.pyplot as plt
import matplotlib.patches as patches

#plt.subplots() crea graficos organizados en cuadriculas en una venta o imagen
#genera dos elementos: la fig que es el lienzo
#ax que es donde se pintan cada uno de los gráficos individuales

# Crea una cuadrícula de 1 fila y 2 columnas
#fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))

# Primer gráfico
#ax1.plot([1, 2, 3], [10, 20, 25])
#ax1.set_title("Gráfico 1")

# Segundo gráfico
#ax2.bar(["A", "B", "C"], [3, 7, 5])
#ax2.set_title("Gráfico 2")

#plt.show()

def circulo():
    #Asignamos las variables 
    #fig es para el lienzo o contenerdor que representa la venta, 
    #porlo que figsize es el tamaño de la ventana 
    #ax es para el área interna del plano cartesiano dentro de la ventana 
    #ahi avitan las figuras y dibujos 
    #todas las figuras se agregan al objeto ax 
    #para crear la figura y los ejes de la pantalla
    fig, ax = plt.subplots(figsize = (6,6))
    
    #Definir el circulo
    #ubicacion, radio por unidades, relleno de color, borde, grosor del borde
    circulo = patches.Circle((5,5),radius = 2, color = 'skyblue', ec = 'gray', lw=1)
    
    #con ass_patch se agregan las figuras, es xplicita
    ax.add_patch(circulo)
    
    #El tamaño del plano cartesiano en xlim y ylim va del (min,max)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    
    #OBLIGATORIO, necesitamos mantener la proporción para no deformar la figura
    #Esto por si la ventana es modificada
    ax.set_aspect('equal')
    
    #plt.axis('off') es para ocular los numeros y marcas de graduacion de los ejes
    #plt.show() son las instruccion para renderizar y desplegar la ventana
    
    #Mostrar la cuadricula de referencia para ver las coordenadas
    #plt.grid(True, linestyle = '--', alpha = 0.5)
    #plt.title("Circulo")
    
    
def cuadrado():
    fig, ax = plt.subplots(figsize = (6,6))
    

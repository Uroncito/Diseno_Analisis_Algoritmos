import csv
import random

def generar_csv_puntos(nombre_archivo, cantidad_puntos, min_x=0, max_x=100, min_y=0, max_y=100):
    
    try:
        with open(nombre_archivo, mode = 'w', newline = '', encoding = 'utf-8') as archivo:
            escritor_csv = csv.writer(archivo)
            #Cabezeras
            escritor_csv.writerow(['x', 'y'])
            #Generar datos
            for i in range(1, cantidad_puntos + 1):
                x = round(random.uniform(min_x,max_x), 2)
                y = round(random.uniform(min_y,max_y), 2)
                escritor_csv.writerow([x,y])
            print(f"Archivo creado {nombre_archivo} con un total de: {cantidad_puntos} de¨({min_x},{min_y}) hasta ({max_x},{max_y})")
    except Exception as e:
        print("Error. Archivo no generado.{e}")

#Llamada para generar los numeros random
if __name__ == "__main__":
    generar_csv_puntos("puntos_prueva.csv",20)
    
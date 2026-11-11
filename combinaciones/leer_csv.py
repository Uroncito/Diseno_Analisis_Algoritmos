import csv

def leer_elementos_csv(ruta_archivo):
    elementos = []
    with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            for dato in fila:
                if dato.strip():
                    elementos.append(dato.strip())
    return elementos
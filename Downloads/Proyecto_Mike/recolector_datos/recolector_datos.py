import time
import serial
import csv
import os

PUERTO_SERIAL = 'COM4'
BAUDIOS = 9600
NOMBRE_ARCHIVO = 'dataset_frutas.csv'

print("Iniciando conexión con el Arduino...")
arduino = serial.Serial(PUERTO_SERIAL, BAUDIOS, timeout=1)
time.sleep(2) 
print("¡Conexión establecida!\n")

archivo_existe = os.path.isfile(NOMBRE_ARCHIVO)

with open(NOMBRE_ARCHIVO, mode='a', newline='') as f:
    writer = csv.writer(f)
    
    if not archivo_existe:
        writer.writerow(['Rojo', 'Verde', 'Azul', 'Fruta'])

    while True:
        fruta = input("Escribe el nombre de la categoría/fruta (o 'salir'): ").strip().lower()
        
        if fruta == 'salir':
            print("Finalizando recolección. ¡Buen trabajo!")
            break
            
        num_muestras = int(input(f"¿Cuántas muestras de '{fruta}' deseas capturar?: "))
        print(f"\nColoca el objeto. Capturando {num_muestras} muestras (¡ve moviéndolo despacio!)...")
        
        capturadas = 0
        while capturadas < num_muestras:
            linea = arduino.readline().decode('utf-8').strip()
            if linea:
                partes = linea.split(',')
                if len(partes) == 3:
                    r, g, b = partes
                    writer.writerow([r, g, b, fruta])
                    print(f"[{capturadas+1}/{num_muestras}] Guardado -> R:{r}, G:{g}, B:{b} | Etiqueta: {fruta}")
                    capturadas += 1
                    time.sleep(0.2)  # Pausa de 0.2 segundos para dar tiempo a mover el objeto
                    
        print(f"\n¡Listo! Se guardaron {num_muestras} muestras en {NOMBRE_ARCHIVO}.\n")

arduino.close()


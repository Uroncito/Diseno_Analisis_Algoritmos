import csv

def leer_csv(nombre_archivo):
    puntos = []
    try:
        with open(nombre_archivo, mode='r', encoding='utf-8') as archivo:
            lector_csv = csv.DictReader(archivo)
            for row in lector_csv:
                #los convertimos en decimales por si llegan a ser enteros y no haya problema
                x = float(row['x'])
                y = float(row['y'])
                #redondear a dos decimales en caso de que haya mas de uno
                x_redondeada = round(x, 2)
                y_redondeada = round(y, 2)
                puntos.append((x_redondeada, y_redondeada))
                
            print(f"Lectura exitosa. Se leyeron {len(puntos)} puntos del archivo {nombre_archivo}")
            return puntos
      
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no existe o no se encuentra.")
    except KeyError as e:
        print(f"Error la columna {e} no se encuentra en el archivo")
    except ValueError as e:
        print(f"Error de formato, al convertir o no son numeros: {e}")
    except Exception as e:
        print(f"Error inespetado al leer el archivo {e}")
        

if __name__ == "__main__":
    lista_puntos = leer_csv("puntos_prueba.csv")        
    print(lista_puntos)
        
        
        
        
        
        
        
        
        
        
        
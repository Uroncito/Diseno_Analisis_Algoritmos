import csv
import math
import time
import serial

# --- CONFIGURACIÓN DE HARDWARE ---
PUERTO_SERIAL = 'COM4'  # Asegúrate de que sea tu puerto correcto
BAUDIOS = 9600
NOMBRE_ARCHIVO = 'dataset_frutas.csv'

# --- FUNCIONES MATEMÁTICAS ---
def sigmoide(x):
    if x < -500: return 0.0
    if x > 500: return 1.0
    return 1.0 / (1.0 + math.exp(-x))

# --- CLASE DE LA RED NEURONAL ---
class RedNeuralPura:
    def __init__(self, num_entradas, num_ocultas, num_salidas):
        self.num_entradas = num_entradas
        self.num_ocultas = num_ocultas
        self.num_salidas = num_salidas
        
        # Estructura de matrices de pesos y bias
        self.W1 = [[0.0 for _ in range(num_entradas)] for _ in range(num_ocultas)]
        self.b1 = [0.0 for _ in range(num_ocultas)]
        self.W2 = [[0.0 for _ in range(num_ocultas)] for _ in range(num_salidas)]
        self.b2 = [0.0 for _ in range(num_salidas)]

    def propagacion_adelante(self, X):
        # Capa Oculta
        a_oculta = []
        for i in range(self.num_ocultas):
            suma = sum(self.W1[i][j] * X[j] for j in range(self.num_entradas)) + self.b1[i]
            a_oculta.append(sigmoide(suma))
            
        # Capa de Salida
        a_salida = []
        for i in range(self.num_salidas):
            suma = sum(self.W2[i][j] * a_oculta[j] for j in range(self.num_ocultas)) + self.b2[i]
            a_salida.append(sigmoide(suma))
            
        return a_salida

    def entrenar(self, X_train, y_train, tasa_aprendizaje=0.5, epochs=1500):
        # Entrenamiento rápido en memoria al arrancar el script usando tu CSV
        for epoch in range(epochs):
            for x, objetivo in zip(X_train, y_train):
                # Forward
                a_oculta = []
                for i in range(self.num_ocultas):
                    suma = sum(self.W1[i][j] * x[j] for j in range(self.num_entradas)) + self.b1[i]
                    a_oculta.append(sigmoide(suma))
                
                prediccion = []
                for i in range(self.num_salidas):
                    suma = sum(self.W2[i][j] * a_oculta[j] for j in range(self.num_ocultas)) + self.b2[i]
                    prediccion.append(sigmoide(suma))
                
                # Errores y gradientes
                error_salida = [objetivo[i] - prediccion[i] for i in range(self.num_salidas)]
                delta_salida = [error_salida[i] * prediccion[i] * (1.0 - prediccion[i]) for i in range(self.num_salidas)]
                
                delta_oculta = []
                for i in range(self.num_ocultas):
                    error_oculto = sum(delta_salida[j] * self.W2[j][i] for j in range(self.num_salidas))
                    delta_oculta.append(error_oculto * a_oculta[i] * (1.0 - a_oculta[i]))
                
                # Actualizar W2, b2
                for i in range(self.num_salidas):
                    for j in range(self.num_ocultas):
                        self.W2[i][j] += tasa_aprendizaje * delta_salida[i] * a_oculta[j]
                    self.b2[i] += tasa_aprendizaje * delta_salida[i]
                
                # Actualizar W1, b1
                for i in range(self.num_ocultas):
                    for j in range(self.num_entradas):
                        self.W1[i][j] += tasa_aprendizaje * delta_oculta[i] * x[j]
                    self.b1[i] += tasa_aprendizaje * delta_oculta[i]

# --- CARGAR DATASET Y PREPARAR EL MODELO ---
def preparar_modelo():
    X = []
    y_textos = []
    
    try:
        with open(NOMBRE_ARCHIVO, mode='r') as f:
            lector = csv.reader(f)
            next(lector) # Saltar encabezado
            for fila in lector:
                if not fila: continue
                X.append([float(fila[0])/255.0, float(fila[1])/255.0, float(fila[2])/255.0])
                y_textos.append(fila[3].strip().lower())
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{NOMBRE_ARCHIVO}'. Asegúrate de haber recolectado datos primero.")
        exit()

    clases_unicas = sorted(list(set(y_textos)))
    
    y_train = []
    for fruta in y_textos:
        vector = [1.0 if c == fruta else 0.0 for c in clases_unicas]
        y_train.append(vector)
        
    # Inicializar pesos aleatorios fijos para que el entrenamiento sea reproducible
    import random
    random.seed(42)
    
    red = RedNeuralPura(num_entradas=3, num_ocultas=4, num_salidas=len(clases_unicas))
    print("Entrenando la red neuronal con los datos del CSV en memoria...")
    red.entrenar(X, y_train, tasa_aprendizaje=0.5, epochs=1500)
    print("¡Modelo listo y entrenado!\n")
    
    return red, clases_unicas

# --- EJECUCIÓN EN TIEMPO REAL ---
if __name__ == "__main__":
    red, clases_unicas = preparar_modelo()
    
    print(f"Conectando al puerto serial {PUERTO_SERIAL}...")
    try:
        arduino = serial.Serial(PUERTO_SERIAL, BAUDIOS, timeout=1)
        time.sleep(2)
        print("¡Conexión establecida con el Arduino! Acércala una fruta al sensor (Presiona Ctrl+C para salir).\n")
        
        while True:
            linea = arduino.readline().decode('utf-8').strip()
            if linea:
                partes = linea.split(',')
                if len(partes) == 3:
                    # Convertir a flotantes y normalizar igual que en el entrenamiento
                    r_raw, g_raw, b_raw = map(float, partes)
                    r_norm = r_raw / 255.0
                    g_norm = g_raw / 255.0
                    b_norm = b_raw / 255.0
                    
                    # Hacer la predicción con la red neuronal
                    prediccion = red.propagacion_adelante([r_norm, g_norm, b_norm])
                    
                    # Encontrar la clase con mayor probabilidad
                    max_prob = max(prediccion)
                    indice_ganador = prediccion.index(max_prob)
                    fruta_detectada = clases_unicas[indice_ganador]
                    
                    # Imprimir resultado en tiempo real
                    print(f"RGB: ({int(r_raw)}, {int(g_raw)}, {int(b_raw)}) -> Predicción: ** {fruta_detectada.upper()} ** (Confianza: {max_prob * 100:.1f}%)")
                    
            time.sleep(0.3) # Pausa ligera para lectura fluida en consola

    except KeyboardInterrupt:
        print("\nFinalizando predicción")
    except Exception as e:
        print(f"\nOcurrió un error en el puerto serial: {e}")
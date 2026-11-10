import csv
import math
import random

# --- 1. CARGAR Y NORMALIZAR EL DATASET ---
def cargar_dataset(nombre_archivo):
    X = []
    y_textos = []
    
    with open(nombre_archivo, mode='r') as f:
        lector = csv.reader(f)
        encabezado = next(lector) # Saltar encabezado [Rojo, Verde, Azul, Fruta]
        
        for fila in lector:
            if not fila: continue
            # Convertimos RGB a flotantes y los normalizamos dividiendo entre 255
            r = float(fila[0]) / 255.0
            g = float(fila[1]) / 255.0
            b = float(fila[2]) / 255.0
            fruta = fila[3].strip().lower()
            
            X.append([r, g, b])
            y_textos.append(fruta)
            
    return X, y_textos

# --- 2. FUNCIONES MATEMÁTICAS DE LA RED ---
def sigmoide(x):
    # Evitamos desbordamientos numéricos con exponenciales muy grandes
    if x < -500: return 0.0
    if x > 500: return 1.0
    return 1.0 / (1.0 + math.exp(-x))

def derivada_sigmoide(s):
    return s * (1.0 - s)

# --- 3. CLASE DE LA RED NEURONAL DESDE CERO ---
class RedNeuralPura:
    def __init__(self, num_entradas, num_ocultas, num_salidas):
        self.num_entradas = num_entradas
        self.num_ocultas = num_ocultas
        self.num_salidas = num_salidas
        
        # Inicializamos pesos y bias con números aleatorios pequeños
        # Pesos de Capa Entrada -> Capa Oculta
        self.W1 = [[random.uniform(-0.5, 0.5) for _ in range(num_entradas)] for _ in range(num_ocultas)]
        self.b1 = [random.uniform(-0.5, 0.5) for _ in range(num_ocultas)]
        
        # Pesos de Capa Oculta -> Capa Salida
        self.W2 = [[random.uniform(-0.5, 0.5) for _ in range(num_ocultas)] for _ in range(num_salidas)]
        self.b2 = [random.uniform(-0.5, 0.5) for _ in range(num_salidas)]

    def propagacion_adelante(self, X):
        # Capa Oculta
        self.z_oculta = []
        self.a_oculta = []
        for i in range(self.num_ocultas):
            suma = sum(self.W1[i][j] * X[j] for j in range(self.num_entradas)) + self.b1[i]
            self.z_oculta.append(suma)
            self.a_oculta.append(sigmoide(suma))
            
        # Capa de Salida
        self.z_salida = []
        self.a_salida = []
        for i in range(self.num_salidas):
            suma = sum(self.W2[i][j] * self.a_oculta[j] for j in range(self.num_ocultas)) + self.b2[i]
            self.z_salida.append(suma)
            self.a_salida.append(sigmoide(suma))
            
        return self.a_salida

    def entrenar(self, X_train, y_train, tasa_aprendizaje=0.1, epochs=1000):
        for epoch in range(epochs):
            error_total = 0
            
            for x, objetivo in zip(X_train, y_train):
                # 1. Forward Pass
                prediccion = self.propagacion_adelante(x)
                
                # 2. Calcular errores en la salida (Objetivo - Predicción)
                error_salida = [objetivo[i] - prediccion[i] for i in range(self.num_salidas)]
                error_total += sum(e**2 for e in error_salida)
                
                # Gradientes de la capa de salida
                delta_salida = [error_salida[i] * derivada_sigmoide(prediccion[i]) for i in range(self.num_salidas)]
                
                # 3. Backpropagation hacia la capa oculta
                delta_oculta = []
                for i in range(self.num_ocultas):
                    error_oculto = sum(delta_salida[j] * self.W2[j][i] for j in range(self.num_salidas))
                    delta_oculta.append(error_oculto * derivada_sigmoide(self.a_oculta[i]))
                    
                # 4. Actualizar Pesos y Bias (W2 y b2)
                for i in range(self.num_salidas):
                    for j in range(self.num_ocultas):
                        self.W2[i][j] += tasa_aprendizaje * delta_salida[i] * self.a_oculta[j]
                    self.b2[i] += tasa_aprendizaje * delta_salida[i]
                    
                # Actualizar Pesos y Bias (W1 y b1)
                for i in range(self.num_ocultas):
                    for j in range(self.num_entradas):
                        self.W1[i][j] += tasa_aprendizaje * delta_oculta[i] * x[j]
                    self.b1[i] += tasa_aprendizaje * delta_oculta[i]
                    
            if (epoch + 1) % 200 == 0:
                print(f"Epoch {epoch+1}/{epochs} - Error cuadrático: {error_total:.4f}")

# --- 4. FLUJO PRINCIPAL DE EJECUCIÓN ---
if __name__ == "__main__":
    archivo = 'dataset_frutas.csv'
    
    print("Cargando dataset...")
    X, y_textos = cargar_dataset(archivo)
    
    # Mapear etiquetas de texto a índices y vectores binarios
    clases_unicas = sorted(list(set(y_textos)))
    print(f"Clases detectadas en el CSV: {clases_unicas}")
    
    # Convertir etiquetas categóricas a One-Hot Encoding (ej. [1, 0] o [0, 1])
    y_train = []
    for fruta in y_textos:
        vector = [1.0 if c == fruta else 0.0 for c in clases_unicas]
        y_train.append(vector)
        
    # Inicializar la Red Neuronal: 3 entradas (RGB), 4 neuronas ocultas, N salidas (según tus frutas)
    red = RedNeuralPura(num_entradas=3, num_ocultas=4, num_salidas=len(clases_unicas))
    
    print("\nEntrenando la red neuronal desde cero...")
    red.entrenar(X, y_train, tasa_aprendizaje=0.5, epochs=1500)
    print("\n¡Entrenamiento finalizado con éxito!")
    
    # Prueba de predicción rápida con la primera muestra del dataset
    muestra_prueba = X[0]
    resultado = red.propagacion_adelante(muestra_prueba)
    indice_ganador = resultado.index(max(resultado))
    print(f"\nPrueba con la primera muestra RGB ({muestra_prueba}):")
    print(f"La red predice que es: {clases_unicas[indice_ganador]} (Confianza: {max(resultado)*100:.2f}%)")
import csv
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN ---
NOMBRE_ARCHIVO = 'dataset_frutas.csv'

# --- 1. CARGAR Y PREPARAR DATOS ---
X_raw = []
y_textos = []

with open(NOMBRE_ARCHIVO, mode='r', encoding='utf-8') as f:
    lector = csv.reader(f)
    next(lector) # Saltar encabezado
    for fila in lector:
        if not fila: continue
        fruta = fila[3].strip().lower()
        if fruta not in ['manzana_verde', 'manzana_amarilla']:
            continue
        X_raw.append([float(fila[0]), float(fila[1]), float(fila[2])])
        y_textos.append(fruta)

X_raw = np.array(X_raw)
y = np.array([0 if f == 'manzana_verde' else 1 for f in y_textos])

# Normalización Min-Max
min_vals = X_raw.min(axis=0)
max_vals = X_raw.max(axis=0)
rango = max_vals - min_vals
rango[rango == 0] = 1.0
X_norm = (X_raw - min_vals) / rango

# --- 2. ENTRENAMIENTO DEL PERCEPTRÓN ---
np.random.seed(42)
w = np.zeros(3)  # [w_rojo, w_verde, w_azul]
b = 0.0
lr = 0.05
epochs = 300

def step(z):
    return 1 if z >= 0 else 0

for epoch in range(epochs):
    for xi, yi in zip(X_norm, y):
        z = np.dot(xi, w) + b
        y_pred = step(z)
        error = yi - y_pred
        if error != 0:
            w += lr * error * xi
            b += lr * error

print("--- RESULTADOS DEL ENTRENAMIENTO ---")
print(f"Pesos [w_R, w_G, w_B]: {w}")
print(f"Bias [b]: {b}")

# --- CÁLCULO DE LA ECUACIÓN DE LA RECTA EN 2D ---
# Hiperplano: w_R*R + w_G*G + w_B*B + b = 0
# Despejando G: G = (-w_R / w_G)*R + (-(w_B * B_prom + b) / w_G)
b_prom = np.mean(X_norm[:, 2])

if w[1] != 0:
    pendiente = -w[0] / w[1]
    ordenada = -(w[2] * b_prom + b) / w[1]
    
    ecuacion_texto = f"G = ({pendiente:.3f}) * R + ({ordenada:.3f})"
    print(f"\nEcuación de la recta de decisión (asumiendo B promedio):")
    print(f"  {ecuacion_texto}")
else:
    ecuacion_texto = "Recta vertical (w_G = 0)"
    print(f"\nEcuación: {ecuacion_texto}")

# --- 3. GENERACIÓN DE LA GRÁFICA 2D ---
plt.figure(figsize=(9, 7))

mask_verde = (y == 0)
mask_amarilla = (y == 1)

plt.scatter(X_norm[mask_verde, 0], X_norm[mask_verde, 1], 
            color='forestgreen', label='Manzana Verde (Clase 0)', s=50, alpha=0.8, edgecolors='k')
plt.scatter(X_norm[mask_amarilla, 0], X_norm[mask_amarilla, 1], 
            color='gold', label='Manzana Amarilla (Clase 1)', s=50, alpha=0.8, edgecolors='k')

# Trazar la recta
r_vals = np.linspace(0, 1, 200)
if w[1] != 0:
    g_vals = pendiente * r_vals + ordenada
    plt.plot(r_vals, g_vals, color='red', linewidth=2.5, label='Frontera de Decisión')

plt.title('Frontera de Decisión Lineal - Clasificación de Manzanas', fontsize=12, fontweight='bold')
plt.xlabel('Intensidad Canal Rojo Normalizado (R)', fontsize=10)
plt.ylabel('Intensidad Canal Verde Normalizado (G)', fontsize=10)
plt.xlim(-0.05, 1.05)
plt.ylim(-0.05, 1.05)

# Poner la ecuación impresa directamente dentro de la gráfica como caja de texto
plt.text(0.05, 0.90, f"Ecuación:\n{ecuacion_texto}", fontsize=10, fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='red'))

plt.axhline(0, color='grey', linewidth=0.8, linestyle='--')
plt.axvline(0, color='grey', linewidth=0.8, linestyle='--')
plt.legend(loc='lower right', frameon=True)
plt.grid(True, linestyle=':', alpha=0.6)

plt.savefig('grafica_frontera_decision.png', dpi=300)
print("\n¡Gráfica actualizada y guardada con éxito como 'grafica_frontera_decision.png'!")

plt.show()
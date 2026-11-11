import matplotlib
matplotlib.use('Qt5Agg')

import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Importamos tu algoritmo desde el otro archivo (asegúrate de que el archivo se llame algoritmo_combinaciones.py)
from algoritmo import obtener_combinaciones
from leer_csv import leer_elementos_csv

def pintar_lienzo_combinaciones(combinaciones):
    """
    Crea un lienzo con matplotlib y pinta cada combinación dentro de un rectángulo.
    """
    if not combinaciones:
        messagebox.showwarning("Aviso", "No hay combinaciones para graficar.")
        return

    fig, ax = plt.subploxts(figsize=(10, 6))
    fig.canvas.manager.set_window_title("Lienzo de Combinaciones")

    # Configuración de la cuadrícula visual
    columnas = 5
    ancho_caja = 2
    alto_caja = 1
    espacio_x = 2.5
    espacio_y = 1.5

    x_actual = 1
    y_actual = 10

    for i, combo in enumerate(combinaciones):
        # Dibujar rectángulo estándar
        caja = patches.Rectangle((x_actual, y_actual), ancho_caja, alto_caja, 
                                 facecolor='skyblue', edgecolor='black', lw=1.5)
        ax.add_patch(caja)
        
        # Insertar el texto de la combinación en el centro del rectángulo
        texto = ", ".join(map(str, combo))
        ax.text(x_actual + ancho_caja/2, y_actual + alto_caja/2, f"[{texto}]", 
                color='black', fontsize=9, weight='bold', ha='center', va='center')

        # Controlar el salto de línea en la cuadrícula
        x_actual += espacio_x
        if (i + 1) % columnas == 0:
            x_actual = 1
            y_actual -= espacio_y

    # Ajustar los límites del lienzo
    ax.set_xlim(0, columnas * espacio_x + 1)
    ax.set_ylim(y_actual - 1, 12)
    ax.axis('off')  # Ocultar los ejes numéricos
    plt.title(f"Se generaron {len(combinaciones)} combinaciones", fontsize=14, pad=20)
    plt.show()

def cargar_archivo():
    """Abre el explorador de archivos para cargar el CSV."""
    ruta = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    if ruta:
        global elementos_cargados
        try:
            elementos_cargados = leer_elementos_csv(ruta)
            etiqueta_archivo.config(text=f"Cargado: {len(elementos_cargados)} elementos")
        except Exception as e:
            messagebox.showerror("Error de lectura", f"No se pudo leer el archivo: {e}")

def procesar_interfaz():
    """Toma los datos de la ventana, ejecuta el algoritmo y llama al lienzo."""
    try:
        entrada_elementos = entrada_datos.get()
        if entrada_elementos:
            arreglo = [x.strip() for x in entrada_elementos.split(",")]
        else:
            arreglo = elementos_cargados
            
        if not arreglo:
            messagebox.showwarning("Faltan datos", "Debes ingresar elementos manuales o cargar un CSV.")
            return

        texto_r = entrada_r.get()
        if not texto_r.isdigit():
            messagebox.showwarning("Error de entrada", "Por favor ingresa un número entero válido para el tamaño (r).")
            return
            
        r = int(texto_r)
        
        if r > len(arreglo) or r <= 0:
            messagebox.showwarning("Rango inválido", f"El tamaño 'r' debe estar entre 1 y el total de elementos ({len(arreglo)}).")
            return

        # Llamada al algoritmo matemático
        combinaciones = obtener_combinaciones(arreglo, r)
        
        # Llamada al lienzo visual
        pintar_lienzo_combinaciones(combinaciones)
        
    except Exception as e:
        messagebox.showerror("Error Interno", f"Ocurrió un problema en la ejecución:\n{str(e)}")

# --- Creación de la Ventana Principal (Tkinter) ---
elementos_cargados = []

ventana = tk.Tk()
ventana.title("Generador Visual de Combinaciones")
ventana.geometry("450x300")
ventana.config(padx=20, pady=20)

# Apartado 1: Entrada manual
tk.Label(ventana, text="1. Ingresa elementos separados por coma:").pack(anchor="w")
entrada_datos = tk.Entry(ventana, width=50)
entrada_datos.pack(pady=5)

tk.Label(ventana, text="- O -").pack()

# Apartado 2: Cargar CSV
boton_csv = tk.Button(ventana, text="2. Cargar archivo CSV", command=cargar_archivo)
boton_csv.pack(pady=5)
etiqueta_archivo = tk.Label(ventana, text="Ningún archivo cargado", fg="gray")
etiqueta_archivo.pack()

# Apartado 3: Tamaño de combinaciones (r)
tk.Label(ventana, text="3. ¿Cuántos elementos por combinación? (r):").pack(anchor="w", pady=(10, 0))
entrada_r = tk.Entry(ventana, width=10)
entrada_r.pack(pady=5)

# Botón Final
boton_generar = tk.Button(ventana, text="Generar Combinaciones", bg="lightgreen", font=("Arial", 10, "bold"), command=procesar_interfaz)
boton_generar.pack(pady=15)

ventana.mainloop()
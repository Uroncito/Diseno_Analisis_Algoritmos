import tkinter as tk
from tkinter import ttk, messagebox
import builtins
import runpy
import os

#Líneas del metro
lineas_metro = {
    'L1': ['PANTITLAN', 'ZARAGOZA', 'GOMEZ FARIAS', 'BOULEVARD PUERTO AEREO', 'BALBUENA', 'MOCTEZUMA', 'SAN LAZARO', 'CANDELARIA', 'MERCED', 'PINO SUAREZ', 'ISABEL LA CATOLICA', 'SALTO DEL AGUA', 'BALDERAS', 'CUAUHTEMOC', 'INSURGENTES', 'SEVILLA', 'CHAPULTEPEC', 'JUANACATLAN', 'TACUBAYA', 'OBSERVATORIO'],
    'L2': ['CUATRO CAMINOS', 'PANTEONES', 'TACUBA', 'CUITLAHUAC', 'POPOTLA', 'COLEGIO MILITAR', 'NORMAL', 'SAN COSME', 'REVOLUCION', 'HIDALGO', 'BELLAS ARTES', 'ALLENDE', 'ZOCALO', 'PINO SUAREZ', 'SAN ANTONIO ABAD', 'CHABACANO', 'VIADUCTO', 'XOLA', 'VILLA DE CORTES', 'NATIVITAS', 'PORTALES', 'ERMITA', 'GENERAL ANAYA', 'TASQUENA'],
    'L3': ['INDIOS VERDES', 'DEPORTIVO 18 DE MARZO', 'POTRERO', 'LA RAZA', 'TLATELOLCO', 'GUERRERO', 'HIDALGO', 'JUAREZ', 'BALDERAS', 'NINOS HEROES', 'HOSPITAL GENERAL', 'CENTRO MEDICO', 'ETIOPIA', 'EUGENIA', 'DIVISION DEL NORTE', 'ZAPATA', 'COYOACAN', 'VIVEROS', 'MIGUEL ANGEL DE QUEVEDO', 'COPILCO', 'UNIVERSIDAD'],
    'L4': ['MARTIN CARRERA', 'TALISMAN', 'BONDOJITO', 'CONSULADO', 'CANAL DEL NORTE', 'MORELOS', 'CANDELARIA', 'FRAY SERVANDO', 'JAMAICA', 'SANTA ANITA'],
    'L5': ['POLITECNICO', 'INSTITUTO DEL PETROLEO', 'AUTOBUSES DEL NORTE', 'LA RAZA', 'MISTERIOS', 'VALLE GOMEZ', 'CONSULADO', 'EDUARDO MOLINA', 'ARAGON', 'OCEANIA', 'TERMINAL AEREA', 'HANGARES', 'PANTITLAN'],
    'L6': ['EL ROSARIO', 'TEZOZOMOC', 'UAM AZCAPOTZALCO', 'FERRERIA', 'NORTE 45', 'VALLEJO', 'INSTITUTO DEL PETROLEO', 'LINDAVISTA', 'DEPORTIVO 18 DE MARZO', 'LA VILLA-BASILICA', 'MARTIN CARRERA'],
    'L7': ['EL ROSARIO', 'AQUILES SERDAN', 'CAMARONES', 'REFINERIA', 'TACUBA', 'SAN JOAQUIN', 'POLANCO', 'AUDITORIO', 'CONSTITUYENTES', 'TACUBAYA', 'SAN PEDRO DE LOS PINOS', 'SAN ANTONIO', 'MIXCOAC', 'BARRANCA DEL MUERTO'],
    'L8': ['GARIBALDI', 'BELLAS ARTES', 'SAN JUAN DE LETRAN', 'SALTO DEL AGUA', 'DOCTORES', 'OBRERA', 'CHABACANO', 'LA VIGA', 'SANTA ANITA', 'COYUYA', 'IZTACALCO', 'APATLACO', 'ACULCO', 'ESCUADRON 201', 'ATLALILCO', 'IZTAPALAPA', 'CERRO DE LA ESTRELLA', 'UAM-I', 'CONSTITUCION DE 1917'],
    'L9': ['PANTITLAN', 'PUEBLA', 'CIUDAD DEPORTIVA', 'VELODROMO', 'MIXIUHCA', 'JAMAICA', 'CHABACANO', 'LAZARO CARDENAS', 'CENTRO MEDICO', 'CHILPANCINGO', 'PATRIOTISMO', 'TACUBAYA'],
    'LA': ['PANTITLAN', 'AGRICOLA ORIENTAL', 'CANAL DE SAN JUAN', 'TEPALCATES', 'GUELATAO', 'PENON VIEJO', 'ACATITLA', 'SANTA MARTA', 'LOS REYES', 'LA PAZ'],
    'LB': ['BUENAVISTA', 'GUERRERO', 'GARIBALDI', 'LAGUNILLA', 'TEPITO', 'MORELOS', 'SAN LAZARO', 'RICARDO FLORES MAGON', 'ROMERO RUBIO', 'OCEANIA', 'DEPORTIVO OCEANIA', 'BOSQUE DE ARAGON', 'VILLA DE ARAGON', 'NEZAHUALCOYOTL', 'IMPULSORA', 'RIO DE LOS REMEDIOS', 'MUZQUIZ', 'ECATEPEC', 'OLIMPICA', 'PLAZA ARAGON', 'CIUDAD AZTECA'],
    'L12': ['MIXCOAC', 'INSURGENTES SUR', 'HOSPITAL 20 DE NOVIEMBRE', 'ZAPATA', 'PARQUE DE LOS VENADOS', 'EJE CENTRAL', 'ERMITA', 'MEXICALTZINGO', 'ATLALILCO', 'CULHUACAN', 'SAN ANDRES TOMATLAN', 'LOMAS ESTRELLA', 'CALLE 11', 'PERIFERICO ORIENTE', 'TEZONCO', 'OLIVOS', 'NOPALERA', 'ZAPOTITLAN', 'TLALTENCO', 'TLAHUAC']
}

origen_elegido = ""
destino_elegido = "" #Eleccion del usuario

def abrir_ventana():
    
    ventana = tk.Tk()
    ventana.title("Metro de la CDMX")
    ventana.geometry("350x400")#Ventana
    
    tk.Label(ventana, text="Metro CDMX", font=("Arial", 14, "bold")).pack(pady=15)
    
    tk.Label(ventana, text="Línea de Inicio:").pack()
    combo_linea_o = ttk.Combobox(ventana, values=list(lineas_metro.keys()), state="readonly")
    combo_linea_o.pack() #inicio del viaje
    
    tk.Label(ventana, text="Estación de Inicio:").pack()
    combo_est_o = ttk.Combobox(ventana, state="readonly")
    combo_est_o.pack(pady=5)
    
    def actualizar_origen(event):
        linea = combo_linea_o.get()
        combo_est_o["values"] = lineas_metro[linea]
        combo_est_o.set("")
        
    combo_linea_o.bind("<<ComboboxSelected>>", actualizar_origen)

    #Fin
    tk.Label(ventana, text="Línea de Destino:").pack(pady=(15, 0))
    combo_linea_d = ttk.Combobox(ventana, values=list(lineas_metro.keys()), state="readonly")
    combo_linea_d.pack()
    
    tk.Label(ventana, text="Estación de Destino:").pack()
    combo_est_d = ttk.Combobox(ventana, state="readonly")
    combo_est_d.pack(pady=5)
    
    def actualizar_destino(event):
        linea = combo_linea_d.get()
        combo_est_d["values"] = lineas_metro[linea]
        combo_est_d.set("")
        
    combo_linea_d.bind("<<ComboboxSelected>>", actualizar_destino)
    
    #Boton de buscar
    def guardar_datos():
        global origen_elegido, destino_elegido
        
        lo = combo_linea_o.get()
        eo = combo_est_o.get()
        ld = combo_linea_d.get()
        ed = combo_est_d.get()
        
        if lo == "" or eo == "" or ld == "" or ed == "":
            messagebox.showerror("Error", "Por favor selecciona todas las líneas y estaciones")
        else:
            origen_elegido = f"{eo} {lo}"
            destino_elegido = f"{ed} {ld}"
            ventana.destroy()
            
    btn_buscar = tk.Button(ventana, text="Buscar Ruta", command=guardar_datos, bg="lightblue", font=("Arial", 10, "bold"))
    btn_buscar.pack(pady=20)
    
    ventana.mainloop()


if __name__ == "__main__": #el main
    abrir_ventana()
    
    if origen_elegido != "" and destino_elegido != "":
        carpeta_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_m2 = os.path.join(carpeta_actual, "m2.py")
        
        respuestas = iter([origen_elegido, destino_elegido])
        input_original = builtins.input
        
        try:
            builtins.input = lambda prompt="": next(respuestas)
            runpy.run_path(ruta_m2, run_name="__main__")
        finally:
            builtins.input = input_original
import networkx as nx
import ventana2

#Lineas del metro
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

#Grafo
LineaM = nx.Graph()
estaciones_por_nombre = {}

for linea, estaciones in lineas_metro.items():
    for i in range(len(estaciones)):
        est = estaciones[i]
        nodo_actual = f"{est} {linea}"
        
        #Linea de cada estacion
        if est not in estaciones_por_nombre:
            estaciones_por_nombre[est] = []
        estaciones_por_nombre[est].append(linea)
        
        #2 minutos por estacion
        if i < len(estaciones) - 1:
            nodo_siguiente = f"{estaciones[i+1]} {linea}"
            LineaM.add_edge(nodo_actual, nodo_siguiente, peso=2)

#Transbordo
for est, lineas in estaciones_por_nombre.items():
    if len(lineas) > 1: # Si la estacion esta 2 veces, es transbordo
        for i in range(len(lineas)):
            for j in range(i + 1, len(lineas)):
                nodo_A = f"{est} {lineas[i]}"
                nodo_B = f"{est} {lineas[j]}"
                LineaM.add_edge(nodo_A, nodo_B, peso=5) #5 minutos por transbordo

print("Rutas del Metro de la CDMX")
print("Ingresa las Estaciones, por ejemplo: \nZapata L3, Copilco L3, Ecatepec LB, Oceanía L5\n")

origen = input("Ingresa la estación de donde inicio: ").strip()
destino = input("Ingresa la estación de destino: ").strip()

i = 1
try:
    # Dijkstra
    ruta = nx.dijkstra_path(LineaM, source=origen, target=destino, weight='peso')
    tiempo = nx.dijkstra_path_length(LineaM, source=origen, target=destino, weight='peso')
    
    print(f"\nRuta (Tiempo estimado: {tiempo} minutos):")
    for estacion in ruta:
        print(f"{i}.- {estacion}")
        i += 1
        
    #Llama a la ventana
    ventana2.mostrar_ruta(LineaM, ruta)
        
except nx.NodeNotFound:
    print("\nEscribiste mal la estación, SONSO, hazlo de otra vez.")
    print("Checa las mayúsculas, acentos, y recuerda incluir la 'L' con el número (ej. 'Ecatepec LB').")
except nx.NetworkXNoPath:
    print("\nNo existe un camino.")
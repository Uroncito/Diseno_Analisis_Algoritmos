import pygame
import sys
from figuras import dibujar_bote, dibujar_lobo, dibujar_gallina, dibujar_granjero, dibujar_maiz
from algoritmo import estado_valido, generar_movimientos, resolver_problema
import pygame
import sys
from figuras import dibujar_bote, dibujar_lobo, dibujar_gallina, dibujar_maiz, dibujar_granjero

# Importamos tanto la validación como el solucionador de tu amigo
from algoritmo import estado_valido, resolver_problema

pygame.init()

ANCHO = 900
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Algoritmo Experto: ")

# Colores
VERDE_PASTO  = (106, 190, 48)
AZUL_RIO     = (65, 166, 246)
CAFE_BORDE   = (115, 62, 57)
BLANCO       = (255, 255, 255)
NEGRO        = (20, 20, 20)
ROJO_ALERTA  = (220, 60, 60)
VERDE_GANA   = (50, 205, 50)
NARANJA_BTN  = (255, 152, 0)
NARANJA_HOV  = (255, 183, 77)

# Fuentes
fuente = pygame.font.SysFont("Arial", 20, bold=True)
fuente_btn = pygame.font.SysFont("Arial", 16, bold=True)

reloj = pygame.time.Clock()

# --- ESTADO DEL JUEGO ---
# [0: Granjero, 1: Gallina, 2: Lobo, 3: Maíz]
estado = [False, False, False, False]
mensaje_estado = "Haz clic en un personaje para cruzar, o en el bote para ir solo."
color_mensaje = BLANCO
juego_terminado = False

# Coordenadas en las orillas (False = Izquierda, True = Derecha)
POSICIONES = {
    "granjero": {False: (220, 270), True: (670, 270)},
    "gallina":  {False: (120, 280), True: (760, 280)},
    "lobo":     {False: (100, 120), True: (730, 120)},
    "maiz":     {False: (110, 420), True: (750, 420)},
    "bote":     {False: (310, 280), True: (450, 280)}
}

# --- VARIABLES DE ANIMACIÓN ---
animando = False
progreso = 0.0
velocidad = 0.025
pasajero_actual = None
estado_siguiente = None

# --- VARIABLES PARA AUTO-RESOLUCIÓN (ALGORITMO EXPERTO) ---
modo_experto_activo = False
cola_estados_experto = []
cola_textos_experto = []
espera_entre_pasos = 0

# Rectángulo del Botón en la barra superior derecha
rect_boton_experto = pygame.Rect(ANCHO - 235, 7, 220, 31)

def iniciar_cruce(indice_pasajero):
    """animación de ir a la otra orilla."""
    global animando, progreso, pasajero_actual, estado_siguiente
    
    nuevo = list(estado)
    nuevo[0] = not nuevo[0]
    
    if indice_pasajero is not None:
        nuevo[indice_pasajero] = not nuevo[indice_pasajero]
        
    estado_siguiente = nuevo
    pasajero_actual = indice_pasajero
    progreso = 0.0
    animando = True

def activar_algoritmo_experto():
    """Consulta resolver_problema()"""
    global estado, animando, juego_terminado, modo_experto_activo
    global cola_estados_experto, cola_textos_experto, mensaje_estado, color_mensaje, espera_entre_pasos

    ruta_estados, ruta_letras = resolver_problema()
    if ruta_estados:
        # Reiniciamos al inicio para mostrar la solución completa paso a paso
        estado = [False, False, False, False]
        animando = False
        juego_terminado = False
        modo_experto_activo = True
        
        # Guardamos todos los estados siguientes (saltando el estado 0 que es el inicial)
        cola_estados_experto = list(ruta_estados[1:])
        cola_textos_experto = list(ruta_letras)
        espera_entre_pasos = 30 # Pequeña pausa de medio segundo antes de arrancar
        color_mensaje = NARANJA_HOV
        mensaje_estado = "Algoritmo Experto activado: Calculando ruta..."

ejecutando = True
while ejecutando:
    # 1. Posiciones base actuales
    x_bote, y_bote         = POSICIONES["bote"][estado[0]]
    x_granjero, y_granjero = POSICIONES["granjero"][estado[0]]
    x_gallina, y_gallina   = POSICIONES["gallina"][estado[1]]
    x_lobo, y_lobo         = POSICIONES["lobo"][estado[2]]
    x_maiz, y_maiz         = POSICIONES["maiz"][estado[3]]

    # 2. Cajas invisibles (Hitboxes)
    rect_bote    = pygame.Rect(x_bote, y_bote - 10, 140, 60)
    rect_gallina = pygame.Rect(x_gallina - 30, y_gallina - 35, 70, 70)
    rect_lobo    = pygame.Rect(x_lobo - 15, y_lobo - 20, 105, 75)
    rect_maiz    = pygame.Rect(x_maiz - 10, y_maiz - 5, 50, 55)

    # --- CAPTURA DE EVENTOS ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        # Reiniciar con 'R'
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
            estado = [False, False, False, False]
            animando = False
            juego_terminado = False
            modo_experto_activo = False
            mensaje_estado = "Juego reiniciado. Haz clic para cruzar."
            color_mensaje = BLANCO

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos_clic = evento.pos

            # 1. Verificar clic en el BOTÓN DEL ALGORITMO EXPERTO
            if rect_boton_experto.collidepoint(pos_clic):
                activar_algoritmo_experto()

            # 2. Clics manuales del jugador (solo si no está animando ni en modo experto)
            elif not animando and not juego_terminado and not modo_experto_activo:
                if rect_gallina.collidepoint(pos_clic):
                    if estado[0] == estado[1]:
                        iniciar_cruce(1)
                    else:
                        mensaje_estado = "¡El granjero está en la otra orilla!"

                elif rect_lobo.collidepoint(pos_clic):
                    if estado[0] == estado[2]:
                        iniciar_cruce(2)
                    else:
                        mensaje_estado = "¡El granjero está en la otra orilla!"

                elif rect_maiz.collidepoint(pos_clic):
                    if estado[0] == estado[3]:
                        iniciar_cruce(3)
                    else:
                        mensaje_estado = "¡El granjero está en la otra orilla!"

                elif rect_bote.collidepoint(pos_clic):
                    iniciar_cruce(None)

    # --- CONTROLADOR DE PASOS AUTOMÁTICOS DEL ALGORITMO EXPERTO ---
    if modo_experto_activo and not animando:
        if espera_entre_pasos > 0:
            espera_entre_pasos -= 1
        elif cola_estados_experto:
            # Sacamos el siguiente estado y texto de la solución de tu amigo
            sig_estado = cola_estados_experto.pop(0)
            accion_texto = cola_textos_experto.pop(0)
            
            mensaje_estado = f"Experto: {accion_texto}"
            color_mensaje = NARANJA_HOV
            
            # Detectamos quién cambió de orilla junto con el granjero (índices 1, 2 o 3)
            acompanante = None
            for idx in [1, 2, 3]:
                if estado[idx] != sig_estado[idx]:
                    acompanante = idx
                    break
                    
            iniciar_cruce(acompanante)
        else:
            modo_experto_activo = False

    # --- LÓGICA DE ANIMACIÓN ---
    if animando:
        progreso += velocidad
        if progreso >= 1.0:
            progreso = 1.0
            animando = False
            estado = estado_siguiente
            
            if not estado_valido(estado):
                juego_terminado = True
                color_mensaje = ROJO_ALERTA
                if estado[1] == estado[2] and estado[0] != estado[1]:
                    mensaje_estado = "¡PERDISTE! El lobo se comió a la gallina. (Presiona R)"
                else:
                    mensaje_estado = "¡PERDISTE! La gallina se comió el maíz. (Presiona R)"
            elif estado == [True, True, True, True]:
                juego_terminado = True
                modo_experto_activo = False
                color_mensaje = VERDE_GANA
                mensaje_estado = "¡ÉXITO! Todos cruzaron a salvo. (Presiona R)"
            else:
                if modo_experto_activo:
                    espera_entre_pasos = 25 # Pausa breve antes del siguiente viaje automático
                else:
                    color_mensaje = BLANCO
                    mensaje_estado = "Turno válido. Elige el siguiente movimiento."
        else:
            x_ini, y_ini = POSICIONES["bote"][estado[0]]
            x_fin, y_fin = POSICIONES["bote"][estado_siguiente[0]]
            
            x_bote = x_ini + (x_fin - x_ini) * progreso
            y_bote = y_ini
            
            x_granjero = x_bote + 40
            y_granjero = y_bote - 45
            
            if pasajero_actual == 1:
                x_gallina = x_bote + 95
                y_gallina = y_bote - 10
            elif pasajero_actual == 2:
                x_lobo = x_bote + 65
                y_lobo = y_bote - 25
            elif pasajero_actual == 3:
                x_maiz = x_bote + 90
                y_maiz = y_bote - 25

    # --- DIBUJAR ESCENARIO Y PERSONAJES ---
    pygame.draw.rect(pantalla, VERDE_PASTO, (0, 0, 300, ALTO))
    pygame.draw.rect(pantalla, AZUL_RIO, (300, 0, 300, ALTO))
    pygame.draw.rect(pantalla, VERDE_PASTO, (600, 0, 300, ALTO))
    pygame.draw.rect(pantalla, CAFE_BORDE, (290, 0, 10, ALTO))
    pygame.draw.rect(pantalla, CAFE_BORDE, (600, 0, 10, ALTO))

    dibujar_bote(pantalla, x_bote, y_bote)
    dibujar_granjero(pantalla, x_granjero, y_granjero)
    dibujar_gallina(pantalla, x_gallina, y_gallina)
    dibujar_lobo(pantalla, x_lobo, y_lobo)
    dibujar_maiz(pantalla, x_maiz, y_maiz)

    # --- BARRA SUPERIOR Y BOTÓN ---
    pygame.draw.rect(pantalla, NEGRO, (0, 0, ANCHO, 45))
    texto_render = fuente.render(mensaje_estado, True, color_mensaje)
    pantalla.blit(texto_render, (15, 11))

    # Efecto visual al pasar el mouse por encima del botón
    mouse_pos = pygame.mouse.get_pos()
    color_actual_btn = NARANJA_HOV if rect_boton_experto.collidepoint(mouse_pos) else NARANJA_BTN
    
    pygame.draw.rect(pantalla, color_actual_btn, rect_boton_experto, border_radius=6)
    pygame.draw.rect(pantalla, BLANCO, rect_boton_experto, 2, border_radius=6)
    
    texto_btn = fuente_btn.render("Resolver (Algoritmo Experto)", True, NEGRO)
    texto_rect = texto_btn.get_rect(center=rect_boton_experto.center)
    pantalla.blit(texto_btn, texto_rect)

    pygame.display.flip()
    reloj.tick(60)

for evento in pygame.event.get():
    if evento.type == pygame.QUIT:
        ejecutando = False
    # Salida inmediata con la tecla ESC
    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
        ejecutando = False
            
pygame.display.quit()  
pygame.quit()
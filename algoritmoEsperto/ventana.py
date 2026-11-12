import pygame
import sys
from figuras import dibujar_bote, dibujar_lobo, dibujar_gallina, dibujar_granjero, dibujar_maiz
from algoritmo import estado_valido, generar_movimientos, resolver_problema

# 1. INICIALIZAR PYGAME
# Arranca todos los módulos internos de Pygame (video, eventos, etc.)
pygame.init()

# 2. CONFIGURACIÓN DE LA VENTANA
ANCHO = 900
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Acertijo: Granjero, Lobo, Gallina y Maíz")

# Colores
VERDE_PASTO = (106, 190, 48)
AZUL_RIO    = (65, 166, 246)
CAFE_BORDE  = (115, 62, 57)
BLANCO      = (255, 255, 255)
NEGRO       = (20, 20, 20)
ROJO_ALERTA = (200, 40, 40)
VERDE_GANA  = (34, 139, 34)

# Fuente para mensajes en pantalla
fuente = pygame.font.SysFont("Arial", 24, bold=True)
fuente_chica = pygame.font.SysFont("Arial", 16)

# 4. RELOJ PARA CONTROLAR LOS FPS (Fotogramas por segundo)
reloj = pygame.time.Clock()


# --- ESTADO DEL JUEGO (Conectado al algoritmo de tu amigo) ---
# Índices: [0: Granjero, 1: Gallina, 2: Lobo, 3: Maíz]
# False = Orilla Izquierda | True = Orilla Derecha
estado = [False, False, False, False]
mensaje_estado = "Haz clic en un personaje para cruzar, o en el bote para ir solo."
color_mensaje = BLANCO
juego_terminado = False

# --- COORDENADAS SEGÚN EL ESTADO (False = Izquierda, True = Derecha) ---
POSICIONES = {
    "granjero": {False: (220, 270), True: (670, 270)},
    "gallina":  {False: (120, 280), True: (760, 280)},
    "lobo":     {False: (100, 120), True: (730, 120)},
    "maiz":     {False: (110, 420), True: (750, 420)},
    "bote":     {False: (310, 280), True: (450, 280)} # El bote sigue al granjero
}

# --- VARIABLES DE ANIMACIÓN ---
animando = False
progreso = 0.0
velocidad = 0.025        # Controla qué tan rápido cruza el bote
pasajero_actual = None   # None = solo, 1 = Gallina, 2 = Lobo, 3 = Maíz
estado_siguiente = None

def iniciar_cruce(indice_pasajero):
    """Prepara la animación hacia la otra orilla."""
    global animando, progreso, pasajero_actual, estado_siguiente
    
    # Creamos una copia del estado actual e invertimos al granjero
    nuevo = list(estado)
    nuevo[0] = not nuevo[0]
    
    # Si lleva acompañante, también lo invertimos de orilla
    if indice_pasajero is not None:
        nuevo[indice_pasajero] = not nuevo[indice_pasajero]
        
    estado_siguiente = nuevo
    pasajero_actual = indice_pasajero
    progreso = 0.0
    animando = True


# 5. BUCLE PRINCIPAL DEL JUEGO (Game Loop)
# En videojuegos, la pantalla se dibuja y actualiza constantemente dentro de un ciclo infinito
ejecutando = True
while ejecutando:
    # 1. Posiciones base actuales
    x_bote, y_bote         = POSICIONES["bote"][estado[0]]
    x_granjero, y_granjero = POSICIONES["granjero"][estado[0]]
    x_gallina, y_gallina   = POSICIONES["gallina"][estado[1]]
    x_lobo, y_lobo         = POSICIONES["lobo"][estado[2]]
    x_maiz, y_maiz         = POSICIONES["maiz"][estado[3]]

    # 2. Cajas invisibles (Hitboxes) para detectar clics del mouse
    rect_bote    = pygame.Rect(x_bote, y_bote - 10, 140, 60)
    rect_gallina = pygame.Rect(x_gallina - 30, y_gallina - 35, 70, 70)
    rect_lobo    = pygame.Rect(x_lobo - 15, y_lobo - 20, 105, 75)
    rect_maiz    = pygame.Rect(x_maiz - 10, y_maiz - 5, 50, 55)

    # --- CAPTURA DE EVENTOS ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        # Reiniciar partida con la tecla 'R'
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
            estado = [False, False, False, False]
            animando = False
            juego_terminado = False
            mensaje_estado = "Juego reiniciado. Haz clic para cruzar."
            color_mensaje = BLANCO

        # Detectar clic izquierdo del mouse (solo si no está animando ni terminó el juego)
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if not animando and not juego_terminado:
                pos_clic = evento.pos

                # Clic en la GALLINA (índice 1)
                if rect_gallina.collidepoint(pos_clic):
                    if estado[0] == estado[1]: # Deben estar en la misma orilla
                        iniciar_cruce(1)
                    else:
                        mensaje_estado = "¡El granjero está en la otra orilla!"

                # Clic en el LOBO (índice 2)
                elif rect_lobo.collidepoint(pos_clic):
                    if estado[0] == estado[2]:
                        iniciar_cruce(2)
                    else:
                        mensaje_estado = "¡El granjero está en la otra orilla!"

                # Clic en el MAÍZ (índice 3)
                elif rect_maiz.collidepoint(pos_clic):
                    if estado[0] == estado[3]:
                        iniciar_cruce(3)
                    else:
                        mensaje_estado = "¡El granjero está en la otra orilla!"

                # Clic en el BOTE (cruza el granjero solo)
                elif rect_bote.collidepoint(pos_clic):
                    iniciar_cruce(None)

    # --- LÓGICA DE ANIMACIÓN ---
    if animando:
        progreso += velocidad
        if progreso >= 1.0:
            # Terminó de cruzar el río
            progreso = 1.0
            animando = False
            estado = estado_siguiente
            
            # Consultamos al algoritmo experto de tu amigo
            if not estado_valido(estado):
                juego_terminado = True
                color_mensaje = ROJO_ALERTA
                if estado[1] == estado[2] and estado[0] != estado[1]:
                    mensaje_estado = "¡PERDISTE! El lobo se comió a la gallina. (Presiona R)"
                else:
                    mensaje_estado = "¡PERDISTE! La gallina se comió el maíz. (Presiona R)"
            elif estado == [True, True, True, True]:
                juego_terminado = True
                color_mensaje = VERDE_GANA
                mensaje_estado = "¡FELICIDADES! Todos cruzaron a salvo. (Presiona R)"
            else:
                color_mensaje = BLANCO
                mensaje_estado = "Turno válido. Elige el siguiente movimiento."
        else:
            # Calcular posiciones intermedias mientras navega el bote
            x_ini, y_ini = POSICIONES["bote"][estado[0]]
            x_fin, y_fin = POSICIONES["bote"][estado_siguiente[0]]
            
            x_bote = x_ini + (x_fin - x_ini) * progreso
            y_bote = y_ini
            
            # Subir al granjero encima del bote durante el viaje
            x_granjero = x_bote + 40
            y_granjero = y_bote - 45
            
            # Subir al pasajero seleccionado al bote durante el viaje
            if pasajero_actual == 1:   # Gallina
                x_gallina = x_bote + 95
                y_gallina = y_bote - 10
            elif pasajero_actual == 2: # Lobo
                x_lobo = x_bote + 65
                y_lobo = y_bote - 25
            elif pasajero_actual == 3: # Maíz
                x_maiz = x_bote + 90
                y_maiz = y_bote - 25

    # --- DIBUJAR ESCENARIO Y PERSONAJES ---
    pygame.draw.rect(pantalla, VERDE_PASTO, (0, 0, 300, ALTO))
    pygame.draw.rect(pantalla, AZUL_RIO, (300, 0, 300, ALTO))
    pygame.draw.rect(pantalla, VERDE_PASTO, (600, 0, 300, ALTO))
    pygame.draw.rect(pantalla, CAFE_BORDE, (290, 0, 10, ALTO))
    pygame.draw.rect(pantalla, CAFE_BORDE, (600, 0, 10, ALTO))

    # Dibujar personajes en sus coordenadas (fijas o animadas)
    dibujar_bote(pantalla, x_bote, y_bote)
    dibujar_granjero(pantalla, x_granjero, y_granjero)
    dibujar_gallina(pantalla, x_gallina, y_gallina)
    dibujar_lobo(pantalla, x_lobo, y_lobo)
    dibujar_maiz(pantalla, x_maiz, y_maiz)

    # Barra superior con instrucciones y estado del algoritmo experto
    pygame.draw.rect(pantalla, NEGRO, (0, 0, ANCHO, 45))
    texto_render = fuente.render(mensaje_estado, True, color_mensaje)
    pantalla.blit(texto_render, (20, 10))

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()
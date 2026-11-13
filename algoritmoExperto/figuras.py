import pygame

# Paleta de colores para nuestros personajes y objetos
CAFE_BOTE   = (139, 69, 19)
CAFE_OSCURO = (92, 46, 12)
GRIS_LOBO   = (120, 120, 130)
GRIS_CLARO  = (180, 180, 190)
NEGRO       = (20, 20, 20)
BLANCO      = (255, 255, 255)
AMARILLO_MAIZ  = (245, 208, 51)
VERDE_HOJA     = (46, 139, 87)
NARANJA_PICO   = (255, 140, 0)
ROJO_CRESTA    = (220, 38, 38)
AZUL_OVEROL    = (41, 98, 255)
PIEL_GRANJERO  = (255, 204, 153)
PAJA_SOMBRERO  = (218, 165, 32)

def dibujar_bote(pantalla, x, y):
    """
    Dibuja un bote usando un polígono (casco) y un rectángulo (asiento).
    (x, y) representa la esquina superior izquierda de referencia del bote.
    """
    # 1. Casco del bote (Polígono de 4 vértices en forma de trapecio invertido)
    puntos_casco = [
        (x, y),               # Esquina superior izquierda
        (x + 140, y),         # Esquina superior derecha
        (x + 115, y + 40),    # Esquina inferior derecha
        (x + 25, y + 40)      # Esquina inferior izquierda
    ]
    pygame.draw.polygon(pantalla, CAFE_BOTE, puntos_casco)
    # Contorno negro del casco (el último parámetro '2' indica grosor de línea)
    pygame.draw.polygon(pantalla, NEGRO, puntos_casco, 2)

    # 2. Tabla/asiento interior del bote (Rectángulo)
    pygame.draw.rect(pantalla, CAFE_OSCURO, (x + 20, y + 5, 100, 8))


def dibujar_lobo(pantalla, x, y):
    """
    Dibuja al lobo (estilo perro geométrico) usando rectángulos, círculos y triángulos.
    (x, y) es la posición base del cuerpo.
    """
    # 1. Patas (2 Rectángulos verticales)
    pygame.draw.rect(pantalla, GRIS_LOBO, (x + 10, y + 30, 10, 20))
    pygame.draw.rect(pantalla, GRIS_LOBO, (x + 40, y + 30, 10, 20))

    # 2. Cuerpo (Rectángulo principal)
    pygame.draw.rect(pantalla, GRIS_LOBO, (x, y + 10, 60, 25))
    pygame.draw.rect(pantalla, NEGRO, (x, y + 10, 60, 25), 2) # Contorno

    # 3. Cola (Triángulo / Polígono a la izquierda)
    puntos_cola = [(x, y + 15), (x - 15, y + 5), (x - 5, y + 25)]
    pygame.draw.polygon(pantalla, GRIS_LOBO, puntos_cola)

    # 4. Cabeza (Círculo a la derecha)
    pygame.draw.circle(pantalla, GRIS_CLARO, (x + 62, y + 8), 16)
    pygame.draw.circle(pantalla, NEGRO, (x + 62, y + 8), 16, 2) # Contorno

    # 5. Orejas puntiagudas (2 Triángulos)
    oreja_izq = [(x + 50, y - 4), (x + 55, y - 20), (x + 60, y - 6)]
    oreja_der = [(x + 62, y - 6), (x + 68, y - 20), (x + 73, y - 4)]
    pygame.draw.polygon(pantalla, GRIS_LOBO, oreja_izq)
    pygame.draw.polygon(pantalla, GRIS_LOBO, oreja_der)

    # 6. Hocico (Triángulo apuntando a la derecha) y Nariz (Círculo negro)
    hocico = [(x + 74, y + 5), (x + 88, y + 12), (x + 74, y + 16)]
    pygame.draw.polygon(pantalla, GRIS_CLARO, hocico)
    pygame.draw.circle(pantalla, NEGRO, (x + 88, y + 12), 3)

    # 7. Ojo (Círculo blanco con pupila negra)
    pygame.draw.circle(pantalla, BLANCO, (x + 66, y + 5), 4)
    pygame.draw.circle(pantalla, NEGRO, (x + 67, y + 5), 2)
    

def dibujar_gallina(pantalla, x, y):
    """
    Dibuja una gallina geométrica usando círculos, triángulos y líneas.
    (x, y) es el punto central de referencia del cuerpo.
    """
    # 1. Patas (2 Rectángulos delgados naranjas)
    pygame.draw.rect(pantalla, NARANJA_PICO, (x - 8, y + 15, 4, 15))
    pygame.draw.rect(pantalla, NARANJA_PICO, (x + 6, y + 15, 4, 15))

    # 2. Cuerpo (Círculo principal blanco)
    pygame.draw.circle(pantalla, BLANCO, (x, y), 20)
    pygame.draw.circle(pantalla, NEGRO, (x, y), 20, 2)

    # 3. Cola (Triángulo a la izquierda)
    cola = [(x - 16, y - 5), (x - 30, y - 15), (x - 18, y + 8)]
    pygame.draw.polygon(pantalla, BLANCO, cola)
    pygame.draw.polygon(pantalla, NEGRO, cola, 2)

    # 4. Cabeza (Círculo más pequeño arriba a la derecha)
    pygame.draw.circle(pantalla, BLANCO, (x + 15, y - 18), 11)
    pygame.draw.circle(pantalla, NEGRO, (x + 15, y - 18), 11, 2)

    # 5. Cresta roja (Triángulo en la punta de la cabeza)
    cresta = [(x + 10, y - 28), (x + 15, y - 37), (x + 20, y - 28)]
    pygame.draw.polygon(pantalla, ROJO_CRESTA, cresta)

    # 6. Pico naranja (Triángulo apuntando a la derecha)
    pico = [(x + 25, y - 20), (x + 35, y - 16), (x + 25, y - 13)]
    pygame.draw.polygon(pantalla, NARANJA_PICO, pico)

    # 7. Ojo (Punto negro)
    pygame.draw.circle(pantalla, NEGRO, (x + 18, y - 20), 2)


def dibujar_maiz(pantalla, x, y):
    """
    Dibuja un saco / mazorca de maíz geométrica.
    (x, y) representa la esquina superior izquierda de referencia.
    """
    # 1. Cuerpo del maíz / saco (Rectángulo amarillo)
    pygame.draw.rect(pantalla, AMARILLO_MAIZ, (x, y, 30, 42))
    pygame.draw.rect(pantalla, NEGRO, (x, y, 30, 42), 2)

    # 2. Hojas verdes envolviendo la base (2 Triángulos laterales)
    hoja_izq = [(x - 6, y + 42), (x + 10, y + 42), (x, y + 18)]
    hoja_der = [(x + 20, y + 42), (x + 36, y + 42), (x + 30, y + 18)]
    pygame.draw.polygon(pantalla, VERDE_HOJA, hoja_izq)
    pygame.draw.polygon(pantalla, VERDE_HOJA, hoja_der)
    pygame.draw.polygon(pantalla, NEGRO, hoja_izq, 1)
    pygame.draw.polygon(pantalla, NEGRO, hoja_der, 1)

    # 3. Detalle de granos (Líneas cruzadas internas para simular textura)
    pygame.draw.line(pantalla, CAFE_OSCURO, (x + 15, y + 2), (x + 15, y + 38), 1)
    pygame.draw.line(pantalla, CAFE_OSCURO, (x + 2, y + 14), (x + 28, y + 14), 1)
    pygame.draw.line(pantalla, CAFE_OSCURO, (x + 2, y + 26), (x + 28, y + 26), 1)


def dibujar_granjero(pantalla, x, y):
    """
    Dibuja al granjero con overol azul y sombrero de paja.
    (x, y) es el centro de su cabeza como punto de referencia.
    """
    # 1. Piernas / Pantalón (2 Rectángulos azules)
    pygame.draw.rect(pantalla, AZUL_OVEROL, (x - 12, y + 48, 10, 22))
    pygame.draw.rect(pantalla, AZUL_OVEROL, (x + 2, y + 48, 10, 22))

    # 2. Torso / Overol (Rectángulo azul)
    pygame.draw.rect(pantalla, AZUL_OVEROL, (x - 15, y + 16, 30, 34))
    pygame.draw.rect(pantalla, NEGRO, (x - 15, y + 16, 30, 34), 2)

    # 3. Brazos (2 Rectángulos laterales)
    pygame.draw.rect(pantalla, PIEL_GRANJERO, (x - 23, y + 18, 8, 22))
    pygame.draw.rect(pantalla, PIEL_GRANJERO, (x + 15, y + 18, 8, 22))

    # 4. Cabeza (Círculo)
    pygame.draw.circle(pantalla, PIEL_GRANJERO, (x, y), 15)
    pygame.draw.circle(pantalla, NEGRO, (x, y), 15, 2)

    # 5. Ojos (2 Círculos pequeños)
    pygame.draw.circle(pantalla, NEGRO, (x - 5, y - 2), 2)
    pygame.draw.circle(pantalla, NEGRO, (x + 5, y - 2), 2)

    # 6. Sombrero de paja (Ala horizontal = Rectángulo + Copa = Polígono/Trapecio)
    pygame.draw.rect(pantalla, PAJA_SOMBRERO, (x - 24, y - 14, 48, 6))
    pygame.draw.rect(pantalla, NEGRO, (x - 24, y - 14, 48, 6), 1)
    
    copa_sombrero = [(x - 14, y - 14), (x + 14, y - 14), (x + 10, y - 28), (x - 10, y - 28)]
    pygame.draw.polygon(pantalla, PAJA_SOMBRERO, copa_sombrero)
    pygame.draw.polygon(pantalla, NEGRO, copa_sombrero, 1)
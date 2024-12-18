import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import sys
from math import sin, cos, pi
import math

from networkx import draw

# Variables globales para la cámara
camera_pos = [4.0, 3.0, 8.0]  # Posición de la cámara
camera_target = [0.0, 3.0, 0.0]  # Punto al que mira
camera_up = [0.0, 1.0, 0.0]  # Vector hacia arriba

# Variables para el movimiento
camera_speed = 0.2  # Velocidad de movimiento
keys = {}  # Diccionario para controlar el estado de las teclas

def load_texture(filename):
    """Carga una textura desde un archivo de imagen"""
    img = Image.open(filename)
    img_data = img.tobytes("raw", "RGB", 0, -1)

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return texture_id

def init():
    """Configuración inicial de OpenGL"""
    glClearColor(0.5, 0.8, 1.0, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)           # Activar prueba de profundidad
    glEnable(GL_TEXTURE_2D)

    # Configuración de la perspectiva
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 1.0, 0.1, 100.0)  # Campo de visión más amplio
    glMatrixMode(GL_MODELVIEW)



def draw_ground():
    """Dibuja un plano para representar el suelo"""
    glBegin(GL_QUADS)
    glColor3f(0.364, 0.690, 0.066)  
    glVertex3f(-100, 0, 100)
    glVertex3f(100, 0, 100)
    glVertex3f(100, 0, -100)
    glVertex3f(-100, 0, -100)
    glEnd()

def draw_textured_quad(vertices, tex_coords, texture_id):
    """Dibuja un cuadrado con textura"""
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)  
    for i in range(4):
        glTexCoord2f(*tex_coords[i])
        glVertex3f(*vertices[i])
    glEnd()

def draw_house(wall_texture, roof_texture, door_texture, window_texture):
    """Dibuja una casa con texturas"""
    # Paredes de la casa 
    walls = [
        ([-3.0, 0, 3.0], [3.0, 0, 3.0], [3.0, 3, 3.0], [-3.0, 3, 3.0]),  # Frente
        ([-3.0, 0, -3.0], [3.0, 0, -3.0], [3.0, 3, -3.0], [-3.0, 3, -3.0]),  # Atrás
        ([-3.0, 0, -3.0], [-3.0, 0, 3.0], [-3.0, 3, 3.0], [-3.0, 3, -3.0]),  # Izquierda
        ([3.0, 0, -3.0], [3.0, 0, 3.0], [3.0, 3, 3.0], [3.0, 3, -3.0])   # Derecha
    ]
    tex_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]

    for wall in walls:
        draw_textured_quad(wall, tex_coords, wall_texture)

    # Techo (ajustado para coincidir con el ancho y largo)
    roof = [
        ([-3.5, 3, 3.5], [3.5, 3, 3.5], [0, 5, 0]),  # Frente
        ([-3.5, 3, -3.5], [3.5, 3, -3.5], [0, 5, 0]),  # Atrás
        ([-3.5, 3, -3.5], [-3.5, 3, 3.5], [0, 5, 0]),  # Izquierda
        ([3.5, 3, -3.5], [3.5, 3, 3.5], [0, 5, 0])   # Derecha
    ]
    glBindTexture(GL_TEXTURE_2D, roof_texture)
    glBegin(GL_TRIANGLES)
    for tri in roof:
        for vertex in tri:
            glTexCoord2f((vertex[0] + 3.5) / 7, (vertex[2] + 3.5) / 7)
            glVertex3f(*vertex)
    glEnd()

    # Puerta (sin cambios)
    door = [(-0.5, 0, 3.01), (0.4, 0, 3.01), (0.4, 1.5, 3.01), (-0.5, 1.5, 3.01)]
    draw_textured_quad(door, tex_coords, door_texture)

    # Ventanas (ajustadas a la nueva profundidad)
    windows = [
        [(-1.8, 1.5, 3.01), (-0.9, 1.5, 3.01), (-0.9, 2.5, 3.01), (-1.8, 2.5, 3.01)],  # Izquierda
        [(0.9, 1.5, 3.01), (1.8, 1.5, 3.01), (1.8, 2.5, 3.01), (0.9, 2.5, 3.01)]   # Derecha
    ]
    for window in windows:
        draw_textured_quad(window, tex_coords, window_texture)

def draw_cobertizo(textura_pared, textura_techo, textura_puerta):
    """Dibuja una casa cuadrada más pequeña con paredes, techo plano y puerta"""
    coord_texturas = [(0, 0), (1, 0), (1, 1), (0, 1)]  # Coordenadas de textura

    # Paredes de la casa
    paredes = [
        ([-1.8, 0, 1.8], [1.8, 0, 1.8], [1.8, 1.8, 1.8], [-1.8, 1.8, 1.8]),  # Frente
        ([-1.8, 0, -1.8], [1.8, 0, -1.8], [1.8, 1.8, -1.8], [-1.8, 1.8, -1.8]),  # Atrás
        ([-1.8, 0, -1.8], [-1.8, 0, 1.8], [-1.8, 1.8, 1.8], [-1.8, 1.8, -1.8]),  # Izquierda
        ([1.8, 0, -1.8], [1.8, 0, 1.8], [1.8, 1.8, 1.8], [1.8, 1.8, -1.8])  # Derecha
    ]
    for pared in paredes:
        draw_textured_quad(pared, coord_texturas, textura_pared)

    # Techo plano
    techo = [
        [-2.0, 1.8, -2.0],  # Esquina trasera izquierda
        [-2.0, 1.8, 2.0],   # Esquina frontal izquierda
        [2.0, 1.8, 2.0],    # Esquina frontal derecha
        [2.0, 1.8, -2.0]    # Esquina trasera derecha
    ]
    draw_textured_quad(techo, coord_texturas, textura_techo)

    # Puerta
    puerta = [(-0.4, 0, 1.81), (0.4, 0, 1.81), (0.4, 1.2, 1.81), (-0.4, 1.2, 1.81)]  # Puerta
    draw_textured_quad(puerta, coord_texturas, textura_puerta)        
        
def valla_horizontal(texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)  
        # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-4, 0.3, 4)
    glTexCoord2f(1.0, 0.0); glVertex3f(4, 0.3, 4)
    glTexCoord2f(1.0, 1.0); glVertex3f(4, 0.7, 4)
    glTexCoord2f(0.0, 1.0); glVertex3f(-4, 0.7, 4)
        
    glEnd()
    
def poste_valla(texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)    

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.2, 0, 0.2)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.2, 0, 0.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.2, 2.5, 0.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.2, 2.5, 0.2)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.2, 0, -0.2)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.2, 0, -0.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.2, 2.5, -0.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.2, 2.5, -0.2)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.2, 0, -0.2)
    glTexCoord2f(1.0, 0.0); glVertex3f(-0.2, 0, 0.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(-0.2, 2.5, 0.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.2, 2.5, -0.2)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(0.2, 0, -0.2)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.2, 0, 0.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.2, 2.5, 0.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.2, 2.5, -0.2)

    # Arriba  
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.2, 2.5, -0.2)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.2, 2.5, -0.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.2, 2.5, 0.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.2, 2.5, 0.2)

    # Abajo
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.2, 0, -0.2)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.2, 0, -0.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.2, 0, 0.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.2, 0, 0.2)
    glEnd()
    
    
def draw_corral_oveja(tierra_pasto_texture, madera_valla_texture):
    positionsH = [
        (0, 0.3, 0),
        (0, 0.8, 0),
        (0, 1.3, 0),
        (0, 0.3, -8),
        (0, 0.8, -8),
        (0, 1.3, -8)
    ]
    for pos in positionsH:
        glPushMatrix()
        glTranslatef(*pos)
        valla_horizontal(madera_valla_texture)
        glPopMatrix()

    positionsV = [
        (0, 0.3, 0),
        (0, 0.8, 0),
        (0, 1.3, 0),
        (-8, 0.3, 0),
        (-8, 0.8, 0),
        (-8, 1.3, 0)
    ]
    for pos in positionsV:
        glPushMatrix()
        glTranslatef(*pos)
        glRotatef(90, 0.0, 1.0, 0.0)
        valla_horizontal(madera_valla_texture)
        glPopMatrix()
        
    positionP = [
        (3.8, 0,  0),
        (3.8, 0,  4),
        (3.8, 0,  -4),
        (-3.8, 0,  0),
        (-3.8, 0,  4),
        (-3.8, 0,  -4),
        (0, 0,  -4)
    ]
    for pos in positionP:
        glPushMatrix()
        glTranslatef(*pos)   
        poste_valla(madera_valla_texture)
        glPopMatrix()
        
    
def draw_lodo(texture):
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1) 

    glTexCoord2f(0.0, 0.0); glVertex3f(-2, 0.01, 2)
    glTexCoord2f(1.0, 0.0); glVertex3f(2, 0.01, 2)
    glTexCoord2f(1.0, 1.0); glVertex3f(2, 0.01, -2)
    glTexCoord2f(0.0, 1.0); glVertex3f(-2, 0.01, -2)
    glEnd()

    
def draw_corral_cerdo(tierra_pasto_texture, madera_valla_texture, lodo_texture):
    positionsH = [
        (0, 0.3, 0),
        (0, 0.8, 0),
        (0, 1.3, 0),
        (0, 0.3, -8),
        (0, 0.8, -8),
        (0, 1.3, -8)
    ]
    for pos in positionsH:
        glPushMatrix()
        glTranslatef(*pos)
        valla_horizontal(madera_valla_texture)
        glPopMatrix()

    positionsV = [
        (0, 0.3, 0),
        (0, 0.8, 0),
        (0, 1.3, 0),
        (-8, 0.3, 0),
        (-8, 0.8, 0),
        (-8, 1.3, 0)
    ]
    for pos in positionsV:
        glPushMatrix()
        glTranslatef(*pos)
        glRotatef(90, 0.0, 1.0, 0.0)
        valla_horizontal(madera_valla_texture)
        glPopMatrix()
        
    positionP = [
        (3.8, 0,  0),
        (3.8, 0,  4),
        (3.8, 0,  -4),
        (-3.8, 0,  0),
        (-3.8, 0,  4),
        (-3.8, 0,  -4),
        (0, 0,  -4)
    ]
    for pos in positionP:
        glPushMatrix()
        glTranslatef(*pos)   
        poste_valla(madera_valla_texture)
        glPopMatrix()
    
    glTranslatef(0.6, 0.03,  0)   
    draw_lodo(lodo_texture)
    
    
def draw_base(texture):
    """Dibuja el cubo (base de la casa)"""
    glBindTexture(GL_TEXTURE_2D, texture)  # Vincula la textura

    glBegin(GL_QUADS)
    glColor3f(0.717, 0.011, 0.011)  

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-4, 0, 4)
    glTexCoord2f(1.0, 0.0); glVertex3f(4, 0, 4)
    glTexCoord2f(1.0, 1.0); glVertex3f(4, 4, 4)
    glTexCoord2f(0.0, 1.0); glVertex3f(-4, 4, 4)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-4, 0, -4)
    glTexCoord2f(1.0, 0.0); glVertex3f(4, 0, -4)
    glTexCoord2f(1.0, 1.0); glVertex3f(4, 4, -4)
    glTexCoord2f(0.0, 1.0); glVertex3f(-4, 4, -4)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-4, 0, -4)
    glTexCoord2f(1.0, 0.0); glVertex3f(-4, 0, 4)
    glTexCoord2f(1.0, 1.0); glVertex3f(-4, 4, 4)
    glTexCoord2f(0.0, 1.0); glVertex3f(-4, 4, -4)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(4, 0, -4)
    glTexCoord2f(1.0, 0.0); glVertex3f(4, 0, 4)
    glTexCoord2f(1.0, 1.0); glVertex3f(4, 4, 4)
    glTexCoord2f(0.0, 1.0); glVertex3f(4, 4, -4)

    # Arriba
    glColor3f(0.9, 0.6, 0.3)  # Color diferente para el techo
    glTexCoord2f(0.0, 0.0); glVertex3f(-1, 4, -1)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 4, -1)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 4, 1)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1, 4, 1)

    # Abajo
    glColor3f(0.6, 0.4, 0.2)  # Suelo más oscuro
    glTexCoord2f(0.0, 0.0); glVertex3f(-4, 0, -4)
    glTexCoord2f(1.0, 0.0); glVertex3f(4, 0, -4)
    glTexCoord2f(1.0, 1.0); glVertex3f(4, 0, 4)
    glTexCoord2f(0.0, 1.0); glVertex3f(-4, 0, 4)
    glEnd()
    
def draw_base2(texture):
    """Dibuja el cubo (base de la casa)"""
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glColor3f(0.717, 0.011, 0.011)  

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-4, 4, 4)
    glTexCoord2f(1.0, 0.0); glVertex3f(4, 4, 4)
    glTexCoord2f(1.0, 1.0); glVertex3f(3, 7, 3)
    glTexCoord2f(0.0, 1.0); glVertex3f(-3, 7, 3)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-4, 4, -4)
    glTexCoord2f(1.0, 0.0); glVertex3f(4, 4, -4)
    glTexCoord2f(1.0, 1.0); glVertex3f(3, 7, -3)
    glTexCoord2f(0.0, 1.0); glVertex3f(-3, 7, -3)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-4, 4, -4)
    glTexCoord2f(1.0, 0.0); glVertex3f(-4, 4, 4)
    glTexCoord2f(1.0, 1.0); glVertex3f(-3, 7, 3)
    glTexCoord2f(0.0, 1.0); glVertex3f(-3, 7, -3)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(4, 4, -4)
    glTexCoord2f(1.0, 0.0); glVertex3f(4, 4, 4)
    glTexCoord2f(1.0, 1.0); glVertex3f(3, 7, 3)
    glTexCoord2f(0.0, 1.0); glVertex3f(3, 7, -3)
    glEnd()

def draw_base3(texture):
    """Dibuja el cubo (base de la casa)"""
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glColor3f(0.717, 0.011, 0.011)  

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-3, 7, 3)
    glTexCoord2f(1.0, 0.0); glVertex3f(3, 7, 3)
    glTexCoord2f(1.0, 1.0); glVertex3f(0, 9, 3)
    glTexCoord2f(0.0, 1.0); glVertex3f(0, 9, 3)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-3, 7, -3)
    glTexCoord2f(1.0, 0.0); glVertex3f(3, 7, -3)
    glTexCoord2f(1.0, 1.0); glVertex3f(0, 9, -3)
    glTexCoord2f(0.0, 1.0); glVertex3f(0, 9, -3)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-3, 7, -3)
    glTexCoord2f(1.0, 0.0); glVertex3f(-3, 7, 3)
    glTexCoord2f(1.0, 1.0); glVertex3f(0, 9, 3)
    glTexCoord2f(0.0, 1.0); glVertex3f(0, 9, -3)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(3, 7, -3)
    glTexCoord2f(1.0, 0.0); glVertex3f(3, 7, 3)
    glTexCoord2f(1.0, 1.0); glVertex3f(0, 9, 3)
    glTexCoord2f(0.0, 1.0); glVertex3f(0, 9, -3)
    glEnd()
    
def draw_techo(texture):
    """Dibuja el techo (pirámide)"""
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glColor3f(0.254, 0.678, 0.823)  

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-4.01, 4.01, -4.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(-4.01, 4.01, 4.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(-3.01, 7.01, 3.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-3.01, 7.01, -3.5)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(4.01, 4.01, -4.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(4.01, 4.01, 4.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(3.01, 7.01, 3.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(3.01, 7.01, -3.5)
    glEnd()
    
def draw_techo2(texture):
    """Dibuja el techo (pirámide)"""
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glColor3f(0.254, 0.678, 0.823)  

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-3.05, 7.01, -3.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(-3.05, 7.01, 3.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.01, 9.01, 3.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.01, 9.01, -3.5)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(3.01, 7.01, -3.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(3.01, 7.01, 3.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(-0.01, 9.01, 3.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.01, 9.01, -3.5)
    glEnd()
    
def puerta_triangulo(texture2):    
    glBindTexture(GL_TEXTURE_2D, texture2)
    glBegin(GL_TRIANGLES)
    glColor3f(0.607, 0.031, 0.031)    
    
    glTexCoord2f(0.0, 0.0); glVertex3f(-2.3, 0.2, 4.15)
    glTexCoord2f(1.0, 0.0); glVertex3f(-0.2, 0.2, 4.15)
    glTexCoord2f(0.5, 1.0); glVertex3f(-1.35, 1.2, 4.15)
    glEnd()

def draw_puerta(texture1, texture2):
    glBindTexture(GL_TEXTURE_2D, texture1)
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)  
    
    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-2.7, 0, 4.1)
    glTexCoord2f(1.0, 0.0); glVertex3f(2.5, 0, 4.1)
    glTexCoord2f(1.0, 1.0); glVertex3f(2.5, 3, 4.1)
    glTexCoord2f(0.0, 1.0); glVertex3f(-2.7, 3, 4.1)
    glEnd()
    
    position = [
        (0, 0, 0),
        (2.6, 0, 0),
        (-2.7, 3, 0),
        (-0.1, 3, 0),
        (0, 2.8, 0),
        (2.5, 2.8, 0),
        (-2.7, 0.1, 0),
        (0, 0.1, 0)
    ]
    
    # abajo
    for pos in position:
        if pos == (0, 0,  0) or pos == (2.6, 0,  0):
            glPushMatrix()
            glTranslatef(*pos)   
            puerta_triangulo(texture2)
            glPopMatrix()
        # arriba
        elif pos == (-2.7, 3, 0) or pos == (-0.1, 3, 0):
            glPushMatrix()
            glTranslatef(*pos)   
            glRotatef(180, 0.0, 0.0, 1.0)
            puerta_triangulo(texture2)
            glPopMatrix()
        # derecha
        elif pos == (0, 2.8, 0) or pos == (2.5, 2.8, 0):
            glPushMatrix()
            glTranslatef(*pos)   
            glRotatef(90, 0.0, 0.0, 1.0)
            puerta_triangulo(texture2)
            glPopMatrix()
        # izquierda
        elif pos == (-2.7, 0.1, 0) or pos == (0, 0.1, 0):
            glPushMatrix()
            glTranslatef(*pos)   
            glRotatef(270, 0.0, 0.0, 1.0)
            puerta_triangulo(texture2)
            glPopMatrix()

def draw_ventana_enfrente(texture1, texture2):
    glBindTexture(GL_TEXTURE_2D, texture1)
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)
    
    glTexCoord2f(0.0, 0.0); glVertex3f(-1, 4, 4.1)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 4, 4.1)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 6, 4.1)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1, 6, 4.1)
    glEnd()
    
    glBindTexture(GL_TEXTURE_2D, texture2)
    glBegin(GL_QUADS)
    glColor3f(0.607, 0.031, 0.031)
    
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.8, 4.2, 4.12)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.8, 4.2, 4.12)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.8, 5.8, 4.12)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.8, 5.8, 4.12)
    glEnd()
    
    glBindTexture(GL_TEXTURE_2D, texture1)
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)
    
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.1, 4, 4.14)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.1, 4, 4.14)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.1, 6, 4.14)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.1, 6, 4.14)
    glEnd()

def draw_ventana(ventana, texture1):
    """Dibuja una ventana en una cara específica de la casa"""
    glBindTexture(GL_TEXTURE_2D, texture1)
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.8, 1.0)  # Color celeste para la ventana

    if ventana == 1:
        # Izquierda
        glColor3f(1, 1, 1)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.01, 1.5, 1)
        glTexCoord2f(1.0, 0.0); glVertex3f(-4.01, 1.5, 2.5)
        glTexCoord2f(1.0, 1.0); glVertex3f(-4.01, 3.5, 2.5)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.01, 3.5, 1)
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(0.156, 0.105, 0.376)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.05, 1.7, 1.2)
        glTexCoord2f(1.0, 0.0); glVertex3f(-4.05, 1.7, 2.3)
        glTexCoord2f(1.0, 1.0); glVertex3f(-4.05, 3.2, 2.3)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.05, 3.2, 1.2)

    elif ventana == 2:
        # Ventana izquierda 2
        glColor3f(1, 1, 1)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.01, 1.5, -1)
        glTexCoord2f(1.0, 0.0); glVertex3f(-4.01, 1.5, 0.5)
        glTexCoord2f(1.0, 1.0); glVertex3f(-4.01, 3.5, 0.5)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.01, 3.5, -1)
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(0.156, 0.105, 0.376)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.05, 1.7, -0.8)
        glTexCoord2f(1.0, 0.0); glVertex3f(-4.05, 1.7, 0.3)
        glTexCoord2f(1.0, 1.0); glVertex3f(-4.05, 3.2, 0.3)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.05, 3.2, -0.8)

    elif ventana == 3:
        # Ventana en la cara izquierda
        glColor3f(1, 1, 1)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.01, 1.5, -3)
        glTexCoord2f(1.0, 0.0); glVertex3f(-4.01, 1.5, -1.7)
        glTexCoord2f(1.0, 1.0); glVertex3f(-4.01, 3.5, -1.7)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.01, 3.5, -3)
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(0.156, 0.105, 0.376)
        glTexCoord2f(0.0, 0.0); glVertex3f(-4.05, 1.7, -2.8)
        glTexCoord2f(1.0, 0.0); glVertex3f(-4.05, 1.7, -1.9)
        glTexCoord2f(1.0, 1.0); glVertex3f(-4.05, 3.2, -1.9)
        glTexCoord2f(0.0, 1.0); glVertex3f(-4.05, 3.2, -2.8)

    elif ventana == 4:
        # Ventana derecha 1
        glColor3f(1, 1, 1)
        glTexCoord2f(0.0, 0.0); glVertex3f(4.01, 1.5, -1)
        glTexCoord2f(1.0, 0.0); glVertex3f(4.01, 1.5, -2.5)
        glTexCoord2f(1.0, 1.0); glVertex3f(4.01, 3.5, -2.5)
        glTexCoord2f(0.0, 1.0); glVertex3f(4.01, 3.5, -1)
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(0.156, 0.105, 0.376)
        glTexCoord2f(0.0, 0.0); glVertex3f(4.05, 1.7, -1.2)
        glTexCoord2f(1.0, 0.0); glVertex3f(4.05, 1.7, -2.3)
        glTexCoord2f(1.0, 1.0); glVertex3f(4.05, 3.2, -2.3)
        glTexCoord2f(0.0, 1.0); glVertex3f(4.05, 3.2, -1.2)
        
    elif ventana == 5:
        # Ventana en la cara izquierda
        glColor3f(1, 1, 1)
        glTexCoord2f(0.0, 0.0); glVertex3f(4.01, 1.5, 1)
        glTexCoord2f(1.0, 0.0); glVertex3f(4.01, 1.5, -0.5)
        glTexCoord2f(1.0, 1.0); glVertex3f(4.01, 3.5, -0.5)
        glTexCoord2f(0.0, 1.0); glVertex3f(4.01, 3.5, 1)
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(0.156, 0.105, 0.376)
        glTexCoord2f(0.0, 0.0); glVertex3f(4.05, 1.7, 0.8)
        glTexCoord2f(1.0, 0.0); glVertex3f(4.05, 1.7, -0.3)
        glTexCoord2f(1.0, 1.0); glVertex3f(4.05, 3.2, -0.3)
        glTexCoord2f(0.0, 1.0); glVertex3f(4.05, 3.2, 0.8)
        
    elif ventana == 6:
        # Ventana en la cara izquierda
        glColor3f(1, 1, 1)
        glTexCoord2f(0.0, 0.0); glVertex3f(4.01, 1.5, 3)
        glTexCoord2f(1.0, 0.0); glVertex3f(4.01, 1.5, 1.5)
        glTexCoord2f(1.0, 1.0); glVertex3f(4.01, 3.5, 1.5)
        glTexCoord2f(0.0, 1.0); glVertex3f(4.01, 3.5, 3)
        glEnd()
        
        glBegin(GL_QUADS)
        glColor3f(0.156, 0.105, 0.376)
        glTexCoord2f(0.0, 0.0); glVertex3f(4.05, 1.7, 2.8)
        glTexCoord2f(1.0, 0.0); glVertex3f(4.05, 1.7, 1.7)
        glTexCoord2f(1.0, 1.0); glVertex3f(4.05, 3.2, 1.7)
        glTexCoord2f(0.0, 1.0); glVertex3f(4.05, 3.2, 2.8)

    glEnd()
        
def draw_granero(madera_texture, madera_blanca_texture, techo_texture):
    draw_base(madera_texture)
    draw_base2(madera_texture)
    draw_base3(madera_texture)
    draw_techo(techo_texture)
    draw_techo2(techo_texture)
    draw_puerta(madera_blanca_texture, madera_texture)    
    draw_ventana_enfrente(madera_blanca_texture, madera_texture)
    draw_ventana(1, madera_blanca_texture)
    draw_ventana(2, madera_blanca_texture)
    draw_ventana(3, madera_blanca_texture)
    draw_ventana(4, madera_blanca_texture)
    draw_ventana(5, madera_blanca_texture)
    draw_ventana(6, madera_blanca_texture)

def draw_cylinder(texture):
    """Dibuja un cilindro usando gluCylinder"""
    glColor3f(1.0, 1.0, 1.0) 
    glBindTexture(GL_TEXTURE_2D, texture)  # Vincula la textura
    quad = gluNewQuadric()                    # Crea el objeto cuadrático
    gluQuadricTexture(quad, GL_TRUE)          # Habilita las coordenadas de textura                 # Asegura el color blanco
    gluCylinder(quad, 2, 2, 15.0, 32, 32)  # (obj, base, top, height, slices, stacks)
    gluDeleteQuadric(quad)   

    
def draw_sphere(texture):
    """Dibuja una esfera utilizando gluSphere."""
    glColor3f(1.0, 1.0, 1.0)    
    glBindTexture(GL_TEXTURE_2D, texture)  # Vincula la textura
    quad = gluNewQuadric()                   # Crea el objeto cuadrático
    gluQuadricTexture(quad, GL_TRUE)         # Habilita las coordenadas de textura             # Asegura el color blanco para mostrar la textura
    gluSphere(quad, 2.0, 32, 32)             # Dibuja la esfera
    gluDeleteQuadric(quad)  
    
def entrada_silo(texture, texture2):
    glColor3f(1.0, 1.0, 1.0) 
    glBindTexture(GL_TEXTURE_2D, texture)  # Vincula la textura
    glBegin(GL_QUADS)
    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-1, 0, -3)
    glTexCoord2f(1.0, 0.0); glVertex3f(-1, 0, 1)
    glTexCoord2f(1.0, 1.0); glVertex3f(-1, 3, 1)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1, 3, -3)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(1, 0, -3)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 0, 1)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 3, 1)
    glTexCoord2f(0.0, 1.0); glVertex3f(1, 3, -3)
    glEnd()
    
    glColor3f(1.0, 1.0, 1.0) 
    glBindTexture(GL_TEXTURE_2D, texture2)
    glBegin(GL_QUADS)
    # Arriba
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.5, 3, -3)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 3, -3)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 3, 1.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.5, 3, 1.5)
    glEnd()
    
def escalera(texture):
    glColor3f(1.0, 1.0, 1.0)  
    glBindTexture(GL_TEXTURE_2D, texture)  # Vincula la textura
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(-0, 0, -0)
    glTexCoord2f(1.0, 0.0); glVertex3f(-0, 0, 0.2)
    glTexCoord2f(1.0, 1.0); glVertex3f(-0.2, 15, 0.2)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0., 15, -0)
    glEnd()
    
def draw_silo(metal_silo_texture, metal_silo2_texture):
    
    glPushMatrix()
    glTranslatef(5.0, 15.0, -10.0)
    glRotatef(90, 1.0, 0.0, 0.0)
    draw_cylinder(metal_silo2_texture)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(5.0, 15.0, -10.0)
    glRotatef(90, 1.0, 0.0, 0.0)
    draw_sphere(metal_silo_texture)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(5.0, 0.0, -5.5)
    entrada_silo(metal_silo2_texture, metal_silo_texture)
    glPopMatrix()
    
    positions = [
        (7, 0, -8.5),
        (7, 0, -8)
    ]
    for pos in positions:
        glPushMatrix()
        glTranslatef(*pos)
        glRotatef(180, 0.0, 1.0, 0.0)
        escalera(metal_silo_texture)
        glPopMatrix()

def draw_suelo(texture_id):
    """Dibuja el campo de cultivo de vegetales con textura"""
    glBindTexture(GL_TEXTURE_2D, texture_id)  # Vincula la textura
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)  

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-1, 0, 0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 0, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 0.5, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1, 0.5, 0.5)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-1, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 0, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 0.5, -0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1, 0.5, -0.5)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-1, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(-1, 0, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(-1, 0.5, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1, 0.5, -0.5)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(1, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 0, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 0.5, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(1, 0.5, -0.5)

    # Arriba
    glTexCoord2f(0.0, 0.0); glVertex3f(-1, 0.5, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 0.5, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 0.5, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1, 0.5, 0.5)

    # Abajo
    glTexCoord2f(0.0, 0.0); glVertex3f(-1, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(1, 0, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(1, 0, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1, 0, 0.5)

    glEnd()

def draw_vegetal(texture_id):
    """Dibuja un vegetal con textura"""
    glBindTexture(GL_TEXTURE_2D, texture_id) # Vincula la textura
    glColor3f(1.0, 1.0, 1.0) # Color blanco para la textura
    # Dibujar tallo
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    glPushMatrix()
    glTranslatef(0.0, 0.25, 0.0)
    gluCylinder(quad, 0.05, 0.05, 0.5, 32, 32)
    glPopMatrix()

    # Dibujar hojas (esferas)
    glPushMatrix()
    glTranslatef(0.0, 0.75, 0.0)
    gluSphere(quad, 0.1, 32, 32)
    glTranslatef(0.1, 0.1, 0.0)
    gluSphere(quad, 0.1, 32, 32)
    glTranslatef(-0.2, 0.1, 0.0)
    gluSphere(quad, 0.1, 32, 32)
    glPopMatrix()

def draw_huerto(suelo_texture, vegetal_texture):
    """Dibuja un huerto de vegetales con campos de cultivo"""
    glPushMatrix()

    # Primera Fila
    glTranslatef(3, 0, 0)
    for i in range(3):
        draw_suelo(suelo_texture)
        glPushMatrix()
        glTranslatef(0.4, 0, 0)
        draw_vegetal(vegetal_texture)
        glPopMatrix()
        glTranslatef(-0.4, 0, 0)

    # Segunda Fila
    glTranslatef(0, 0, 1.5)
    for i in range(3):
        draw_suelo(suelo_texture)
        glPushMatrix()
        glTranslatef(0.4, 0, 0)
        draw_vegetal(vegetal_texture)
        glPopMatrix()
        glTranslatef(-0.4, 0, 0)

    glPopMatrix()
    
def draw_trunk(texture_id):
    """Dibuja el tronco del árbol como un cilindro con textura."""
    glPushMatrix()
    glColor3f(1, 1, 1)  
    glTranslatef(0.0, 0.0, 0.0)  
    glRotatef(-90, 1, 0, 0)  

    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    gluCylinder(quadric, 0.3, 0.3, 2.0, 32, 32)  
    glPopMatrix()

def draw_foliage():
    """Dibuja las hojas del árbol como una esfera."""
    glPushMatrix()
    glColor3f(0.1, 0.8, 0.1)  
    glTranslatef(0.0, 2.0, 0.0)  
    quadric = gluNewQuadric()
    gluSphere(quadric, 1.0, 32, 32)  
    glPopMatrix()

def draw_apples():
    """Dibuja pequeñas esferas rojas representando manzanas."""
    glColor3f(1.0, 0.0, 0.0)  
    quadric = gluNewQuadric()

    apple_positions = [
        (0.5, 2.5, 0.3),
        (-0.4, 2.3, -0.5),
        (0.3, 2.7, -0.2),
        (-0.2, 2.8, 0.6),
        (0.6, 2.6, -0.4),
        (-0.5, 2.4, 0.5)
    ]

    for pos in apple_positions:
        glPushMatrix()
        glTranslatef(*pos)  
        gluSphere(quadric, 0.1, 16, 16)  
        glPopMatrix()

def draw_manzano(texture_id):
    """Dibuja un manzano completo."""
    glPushMatrix()
    draw_trunk(texture_id)  
    draw_foliage()
    draw_apples()
    glPopMatrix()

def draw_tallo_fresal():
    """Dibuja el tallo de la planta"""
    glPushMatrix()
    glColor3f(0.4, 0.8, 0.2)  # Verde claro para el tallo
    glTranslatef(0.0, 0.0, 0.0)  # Posicionar el tallo
    glRotatef(-90, 1, 0, 0)  # Rota para orientar el cilindro verticalmente
    quadric = gluNewQuadric()
    gluCylinder(quadric, 0.05, 0.05, 0.5, 32, 32)  # Tallos delgados
    glPopMatrix()

def draw_hojas_fresal():
    """Dibuja las hojas de la planta como esferas pequeñas"""
    glColor3f(0.1, 0.5, 0.1)  # Verde oscuro para las hojas
    quadric = gluNewQuadric()
    
    leaf_positions = [
        (0.2, 0.5, 0.0),   # Derecha
        (-0.2, 0.5, 0.0),  # Izquierda
        (0.0, 0.5, 0.2),   # Adelante
        (0.0, 0.5, -0.2),  # Atrás
    ]
    
    for x, y, z in leaf_positions:
        glPushMatrix()
        glTranslatef(x, y, z)
        gluSphere(quadric, 0.2, 32, 32)  # Tamaño de las hojas
        glPopMatrix()

def draw_fresas():
    """Dibuja las fresas como pequeñas esferas rojas"""
    glColor3f(1.0, 0.0, 0.0)  # Rojo para las fresas
    quadric = gluNewQuadric()
    
    strawberry_positions = [
        (0.15, 0.3, 0.1),
        (-0.1, 0.35, -0.1),
        (0.05, 0.4, -0.15),
        (-0.15, 0.3, 0.05),
    ]
    
    for x, y, z in strawberry_positions:
        glPushMatrix()
        glTranslatef(x, y, z)
        gluSphere(quadric, 0.1, 32, 32)  # Tamaño de las fresas
        glPopMatrix()

def draw_fresal():
    """Dibuja una planta de fresas completa"""
    glPushMatrix()
    draw_tallo_fresal()           # Dibuja el tallo
    draw_hojas_fresal()         # Dibuja las hojas
    draw_fresas()   # Dibuja las fresas
    glPopMatrix()

def draw_textured_trunk(texture_id):
    """Dibuja el tronco del pino con textura."""
    glPushMatrix()
    glColor3f(1, 1, 1)  
    glTranslatef(0.0, 0.0, 0.0)  
    glRotatef(-90, 1, 0, 0)  

    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    gluCylinder(quadric, 0.3, 0.1, 2.0, 32, 32)  
    glPopMatrix()

def draw_foliage_pine():
    """Dibuja el follaje del pino como conos apilados"""
    glColor3f(0.1, 0.6, 0.1)  # Verde oscuro para el follaje
    quadric = gluNewQuadric()

    # Dibujar tres conos de diferentes tamaños
    foliage_levels = [
        (0.6, 1.2, 0.8),  # (Radio base, Altura, Traslación en Y)
        (0.4, 1.0, 1.6),
        (0.2, 0.8, 2.4),
    ]
    
    for base, height, y_translation in foliage_levels:
        glPushMatrix()
        glTranslatef(0.0, y_translation, 0.0)  # Elevar cada cono
        glRotatef(-90, 1, 0, 0)  # Rota para orientar el cono verticalmente
        gluCylinder(quadric, base, 0.0, height, 32, 32)  # Base más grande y punta cerrada
        glPopMatrix()

def draw_pine(texture_id):
    """Dibuja un pino completo."""
    glPushMatrix()
    draw_textured_trunk(texture_id)
    draw_foliage_pine()
    glPopMatrix()

def draw_caja_base_panal(textura_id):
    """ Dibuja las bases donde se colocaran los panales para asimilar una zona de Apicultura"""
    glBindTexture(GL_TEXTURE_2D, textura_id) #  Vincula la textura
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)  # blanco para no alterar la textura

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.4, 0, 0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4, 0, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4, 1, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.4, 1, 0.5)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.4, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4, 0, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4, 1, -0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.4, 1, -0.5)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.4, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(-0.4, 0, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(-0.4, 1, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.4, 1, -0.5)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(0.4, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4, 0, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4, 1, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.4, 1, -0.5)

    # Arriba
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.4, 1, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4, 1, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4, 1, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.4, 1, 0.5)

    # Abajo
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.4, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4, 0, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4, 0, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.4, 0, 0.5)
    glEnd()

def draw_base_inferior_panal(textura_id):
    """ Dibuja la base inferior de los panales"""
    glBindTexture(GL_TEXTURE_2D, textura_id) #  Vincula la textura
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.3, -0.15, 0.3)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.3, -0.15, 0.3)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.3, 0.15, 0.3)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.3, 0.15, 0.3)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.3, -0.15, -0.3)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.3, -0.15, -0.3)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.3, 0.15, -0.3)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.3, 0.15, -0.3)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.3, -0.15, -0.3)
    glTexCoord2f(1.0, 0.0); glVertex3f(-0.3, -0.15, 0.3)
    glTexCoord2f(1.0, 1.0); glVertex3f(-0.3, 0.15, 0.3)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.3, 0.15, -0.3)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(0.3, -0.15, -0.3)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.3, -0.15, 0.3)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.3, 0.15, 0.3)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.3, 0.15, -0.3)

    # Arriba
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.3, 0.15, -0.3)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.3, 0.15, -0.3)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.3, 0.15, 0.3)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.3, 0.15, 0.3)

    # Abajo
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.3, -0.15, -0.3)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.3, -0.15, -0.3)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.3, -0.15, 0.3)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.3, -0.15, 0.3)
    glEnd()

def draw_base_intermedia_panal(textura_id):
    """ Dibuja la base intermedia de los panales"""
    glBindTexture(GL_TEXTURE_2D, textura_id) #  Vincula la textura
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.4, 0, 0.4)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4, 0, 0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4, 0.25, 0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.4, 0.25, 0.4)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.4, 0, -0.4)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4, 0, -0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4, 0.25, -0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.4, 0.25, -0.4)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.4, 0, -0.4)
    glTexCoord2f(1.0, 0.0); glVertex3f(-0.4, 0, 0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(-0.4, 0.25, 0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.4, 0.25, -0.4)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(0.4, 0, -0.4)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4, 0, 0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4, 0.25, 0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.4, 0.25, -0.4)

    # Arriba
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.4, 0.25, -0.4)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4, 0.25, -0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4, 0.25, 0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.4, 0.25, 0.4)

    # Abajo
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.4, 0, -0.4)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.4, 0, -0.4)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.4, 0, 0.4)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.4, 0, 0.4)
    glEnd()

def draw_base_superior_panal(textura_id):
    """ Dibuja la base superior de los panales"""
    glBindTexture(GL_TEXTURE_2D, textura_id) #  Vincula la textura
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)

    # Frente
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, 0, 0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.5, 0, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.5, 0.25, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, 0.25, 0.5)

    # Atrás
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.5, 0, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.5, 0.25, -0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, 0.25, -0.5)

    # Izquierda
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(-0.5, 0, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(-0.5, 0.25, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, 0.25, -0.5)

    # Derecha
    glTexCoord2f(0.0, 0.0); glVertex3f(0.5, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.5, 0, 0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.5, 0.25, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.5, 0.25, -0.5)

    # Arriba
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, 0.25, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.5, 0.25, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.5, 0.25, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, 0.25, 0.5)

    # Abajo
    glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, 0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(0.5, 0, -0.5)
    glTexCoord2f(1.0, 1.0); glVertex3f(0.5, 0, 0.5)
    glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, 0, 0.5)
    glEnd()

def draw_panal(textura_id):
    draw_base_inferior_panal(textura_id)
    glTranslatef(0, 0.1, 0)
    draw_base_intermedia_panal(textura_id)
    glTranslatef(0, 0.2, 0)
    draw_base_superior_panal(textura_id)
    glTranslatef(0, 0.2, 0)
    draw_base_superior_panal(textura_id)
    glTranslatef(0, 0.2, 0)
    draw_base_intermedia_panal(textura_id)
    glTranslatef(0, 0.3, 0)
    draw_base_inferior_panal(textura_id)

def draw_zona_apicultura(base_panal_texturas, panal_texturas):
    """ Dibuja la zona de apicultura"""
    glPushMatrix()
    draw_caja_base_panal(base_panal_texturas)
    glTranslatef(0, 1.1, 0)
    draw_panal(panal_texturas)
    glPopMatrix()

def draw_scene(wall_texture, roof_texture, door_texture, window_texture, madera_granero_texture, madera_blanca_texture, 
                   techo_granero_texture, tierra_pasto_texture, madera_valla_texture, lodo_texture, suelo_texture, vegetal_texture,
                   texture_troncoManzano, base_panal_texturas, panal_texturas, metal_silo_texture, metal_silo2_texture, textura_pared, 
                   textura_techo, textura_puerta):
    """Dibuja la escena completa"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Configuración de la cámara
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],  # Posición de la cámara
              camera_target[0], camera_target[1], camera_target[2],  # Punto al que mira
              camera_up[0], camera_up[1], camera_up[2])  # Vector hacia arriba
    
    positions_casa = [
        (-5, 0, 25)
    ]
    for pos in positions_casa:
        glPushMatrix()
        glTranslatef(*pos)  # Mover la casa a la posición actual    
        glRotatef(90, 0.0, 1.0, 0.0)   
        draw_house(wall_texture, roof_texture, door_texture, window_texture)
        glPopMatrix()
    
    position_cobertizo = (-5, 0, 18)
    glPushMatrix()
    glTranslatef(*position_cobertizo)  # Mover la casa a la posición actual
    glRotatef(90, 0.0, 1.0, 0.0)       
    draw_cobertizo(textura_pared, textura_techo, textura_puerta)
    glPopMatrix()
    
    position_granero = (20, 0, 10)
    glPushMatrix()
    glTranslatef(*position_granero)  # Mover la casa a la posición actual       
    draw_granero(madera_granero_texture, madera_blanca_texture, techo_granero_texture)
    glPopMatrix()
    
    position_corral1 = (10, 0, 10)
    glPushMatrix()
    glTranslatef(*position_corral1)
    draw_corral_oveja(tierra_pasto_texture, madera_valla_texture)
    glPopMatrix()
    
    position_corral2 = (30, 0, 10)
    glPushMatrix()
    glTranslatef(*position_corral2)
    draw_corral_cerdo(tierra_pasto_texture, madera_valla_texture, lodo_texture)
    glPopMatrix()
    
    position_silo = (15, 0, 11)
    glPushMatrix()
    glTranslatef(*position_silo)
    draw_silo(metal_silo_texture, metal_silo2_texture)   
    glPopMatrix()


    positions_huerto = [
        (40, -0.35, 40), (40, -0.35, 44), (40, -0.35, 48), (40, -0.35, 52),
        (36, -0.35, 40), (36, -0.35, 44), (36, -0.35, 48), (36, -0.35, 52),
        (32, -0.35, 40), (32, -0.35, 44), (32, -0.35, 48), (32, -0.35, 52)
    ]            
    for pos in positions_huerto:
        glPushMatrix()
        glTranslatef(*pos)  # Mover la casa a la posición actual     
        draw_huerto(suelo_texture, vegetal_texture)
        glPopMatrix()


    positions_manzano = [
        (27, 0, 40), (27, 0, 44), (27, 0, 48), (27, 0, 52),
        (23, 0, 40), (23, 0, 44), (23, 0, 48), (23, 0, 52), 
        (19, 0, 40), (19, 0, 44), (19, 0, 48), (19, 0, 52)
    ]

    for pos in positions_manzano:
        glPushMatrix()
        glTranslatef(*pos)
        draw_manzano(texture_troncoManzano)
        glPopMatrix()

    positions_fresal = [
        (40, 0, 27), (40, 0, 25), (40, 0, 23), 
        (38, 0, 27), (38, 0, 25), (38, 0, 23),
        (36, 0, 27), (36, 0, 25), (36, 0, 23),
        (34, 0, 27), (34, 0, 25), (34, 0, 23),
        (32, 0, 27), (32, 0, 25), (32, 0, 23),
        (30, 0, 27), (30, 0, 25), (30, 0, 23),
    ]

    for pos in positions_fresal:
        glPushMatrix()
        glTranslatef(*pos)
        draw_fresal()
        glPopMatrix()

    positions_pino = [
        (-1, 0, -40),(-1, 0, -38),(-1, 0, -36),
        (-2, 0, -40),(-2, 0, -38),(-2, 0, -36),
        (-3, 0, -40),(-3, 0, -38),(-3, 0, -36),
        (-4, 0, -40),(-4, 0, -38),(-4, 0, -36),
        (-5, 0, -40),(-5, 0, -38),(-5, 0, -36),
        (-6, 0, -40),(-6, 0, -38),(-6, 0, -36),
        (-7, 0, -40),(-7, 0, -38),(-7, 0, -36),
        (-8, 0, -40),(-8, 0, -38),(-8, 0, -36),
        (-9, 0, -40),(-9, 0, -38),(-9, 0, -36),
        (-10, 0, -40),(-10, 0, -38),(-10, 0, -36),
        (-11, 0, -40),(-11, 0, -38),(-11, 0, -36),
        (-12, 0, -40),(-12, 0, -38),(-12, 0, -36),
        (-13, 0, -40),(-13, 0, -38),(-13, 0, -36),
        (-14, 0, -40),(-14, 0, -38),(-14, 0, -36),
        (-15, 0, -40),(-15, 0, -38),(-15, 0, -36),
        (-16, 0, -40),(-16, 0, -38),(-16, 0, -36)
    ]

    for pos in positions_pino:
        glPushMatrix()
        glTranslatef(*pos)
        draw_pine(texture_troncoManzano)
        glPopMatrix()

    positions_base_panal = [
        (30, 0, 40), (30, 0, 44), (30, 0, 48), (30, 0, 52)
    ]

    for pos in positions_base_panal:
        glPushMatrix()
        glTranslatef(*pos)
        draw_zona_apicultura(base_panal_texturas, panal_texturas)
        glPopMatrix()
    

    draw_ground()  # Dibuja el suelo

    glfw.swap_buffers(window)


def process_input():
    """Procesa el estado de las teclas para mover la cámara"""
    global camera_pos

    if keys.get(glfw.KEY_W, False):  # Mover hacia adelante
        camera_pos[2] -= camera_speed
    if keys.get(glfw.KEY_S, False):  # Mover hacia atrás
        camera_pos[2] += camera_speed
    if keys.get(glfw.KEY_A, False):  # Mover a la izquierda
        camera_pos[0] -= camera_speed
    if keys.get(glfw.KEY_D, False):  # Mover a la derecha
        camera_pos[0] += camera_speed
    if keys.get(glfw.KEY_UP, False):  # Subir
        camera_pos[1] += camera_speed
    if keys.get(glfw.KEY_DOWN, False):  # Bajar
        camera_pos[1] -= camera_speed


def key_callback(window, key, scancode, action, mods):
    """Actualiza el estado de las teclas"""
    if action == glfw.PRESS:
        keys[key] = True
    elif action == glfw.RELEASE:
        keys[key] = False


def main():
    global window

    # Inicializar GLFW
    if not glfw.init():
        sys.exit()
    
    # Crear ventana de GLFW
    width, height = 800, 600
    window = glfw.create_window(width, height, "Mover Escena Completa", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glViewport(0, 0, width, height)
    init()

    wall_texture = load_texture(r"pared.jpg") #paredes
    roof_texture = load_texture(r"teja_cafe.jpeg") #tejado
    door_texture = load_texture(r"puerta.jpg") #puerta
    window_texture = load_texture(r"ventanas.jpeg") #ventanas
    
    textura_pared = load_texture(r"paredes_cobertizo.jpg")
    textura_techo = load_texture(r"techo_cobertizo_metal.jpg")
    textura_puerta = load_texture(r"porton.jpg")

    madera_granero_texture = load_texture('madera_granero.jpg')
    madera_blanca_texture = load_texture('madera_blanca.jpg')
    techo_granero_texture = load_texture('techo.jpg')
    tierra_pasto_texture = load_texture('tierra_pasto.jpg')
    madera_valla_texture = load_texture('madera_valla.jpg')
    lodo_texture = load_texture('lodo.jpg')
    metal_silo_texture = load_texture('metal_silo.jpg')
    metal_silo2_texture = load_texture('metal_silo2.jpg')
    
    suelo_texture = load_texture(r"suelo-texture.jpg")   # Textura para el campo de cultivo de vegetales
    vegetal_texture = load_texture(r"vegetal-texture.jpg") 

    base_panal_texturas = load_texture(r'panal-abejas-textura.jpg') # Texturas para la base y el panal de abejas
    panal_texturas = load_texture(r'colmena-entrada-textura.jpg') # Texturas para el panal de abejas
    
    texture_troncoManzano = load_texture(r'tree-branch-512x512.png')
    
    # Configurar callback de teclado
    glfw.set_key_callback(window, key_callback)

    # Bucle principal
    while not glfw.window_should_close(window):
        process_input()  # Procesar teclas presionadas
        draw_scene(wall_texture, roof_texture, door_texture, window_texture, madera_granero_texture, madera_blanca_texture, 
                   techo_granero_texture, tierra_pasto_texture, madera_valla_texture, lodo_texture, suelo_texture, vegetal_texture,
                   texture_troncoManzano, base_panal_texturas, panal_texturas, metal_silo_texture, metal_silo2_texture, textura_pared, 
                   textura_techo, textura_puerta)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()